from uuid import UUID, uuid4

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase, RelationshipBase
from app.lib.files import SystemFile
from app.models import File, FileTheme, Specialty, SpecialtyFile, Theme
from app.schemas import FileCreate, FileUpdate


class CRUDFile(CRUDBase[File, FileCreate, FileUpdate]):
    async def remove(self, session: AsyncSession, id: UUID) -> File:
        file_obj = await super().remove(session, id)

        SystemFile(dir_path=str(file_obj.id)).delete()

        return file_obj


class RelationshipForSpecialty(RelationshipBase[File, SpecialtyFile, FileCreate]):
    async def get_for_specialty(
        self, session: AsyncSession, specialty_id: UUID
    ) -> list[File] | None:
        return await self.get_for(
            session=session,
            m2m_parent_field=SpecialtyFile.specialty_id,
            parent_uuid=specialty_id,
        )

    async def create(
        self, session: AsyncSession, files: list[UploadFile], specialty_id: UUID
    ) -> None:
        for file in files:
            file_id = uuid4()

            system_file = SystemFile(
                bytes_buffer=file.file, dir_path=str(file_id), filename=file.filename
            )

            file_in = FileCreate(url=system_file.save(), name=file.filename)

            await self.create_with_relation(
                session=session,
                model_in=file_in,
                model_statement={"file_id": file_id},
                related_model_statement={"specialty_id": specialty_id},
            )


class RelationshipForThemes(RelationshipBase[File, FileTheme, FileCreate]):
    async def get_for_theme(
        self, session: AsyncSession, theme_id: UUID
    ) -> list[File] | None:
        return await self.get_for(
            session=session,
            m2m_parent_field=FileTheme.theme_id,
            parent_uuid=theme_id,
        )

    async def create(
        self, session: AsyncSession, files: list[UploadFile], theme_id: UUID
    ) -> None:
        for file in files:
            file_id = uuid4()

            system_file = SystemFile(
                bytes_buffer=file.file, dir_path=str(file_id), filename=file.filename
            )

            file_in = FileCreate(url=system_file.save(), name=file.filename)

            await self.create_with_relation(
                session=session,
                model_in=file_in,
                model_statement={"file_id": file_id},
                related_model_statement={"theme_id": theme_id},
            )


file = CRUDFile(model=File)

file_for_specialty = RelationshipForSpecialty(
    model=File, m2m_model=SpecialtyFile, relationship_attr=Specialty.files
)

file_for_themes = RelationshipForThemes(
    model=File, m2m_model=FileTheme, relationship_attr=Theme.files
)
