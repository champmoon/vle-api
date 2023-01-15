from uuid import UUID, uuid4

from fastapi import UploadFile
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.crud.base import CRUDBase, RelationshipBase
from app.crud.crud_file import file
from app.models import ComplexDiscipline, Discipline, File, Specialty
from app.models.discipline_specialty import DisciplineSpecialty
from app.schemas import DisciplineCreate, DisciplineUpdate


class CRUDDiscipline(CRUDBase[Discipline, DisciplineCreate, DisciplineUpdate]):
    async def attach_plan(
        self, session: AsyncSession, id: UUID, plan: UploadFile
    ) -> None:
        save_path = f"{settings.STATIC_FILES_DIR}/plans/{id}/"

        await file.save_file_in_system(
            save_path=save_path, file_name=plan.filename, file=plan
        )

        full_save_path = save_path + plan.filename
        file_id = uuid4()

        try:
            await file.insert_flush(
                session=session,
                insert_statement={"id": file_id, "url": full_save_path},
            )
        except IntegrityError:
            await session.rollback()

            file_obj = await session.execute(
                select(File).where(File.url == full_save_path)
            )
            file_id = file_obj.scalar_one().id

        await session.execute(
            update(self.model).where(self.model.id == id).values(plan=file_id)
        )
        await session.commit()


class RelationshipForSpecialty(
    RelationshipBase[Discipline, DisciplineSpecialty, DisciplineCreate]
):
    async def get_for_specialty(
        self, session: AsyncSession, specialty_id: UUID
    ) -> list[Discipline] | None:
        return await self.get_for(
            session=session,
            m2m_parent_field=DisciplineSpecialty.specialty_id,
            parent_uuid=specialty_id,
        )

    async def create(
        self, session: AsyncSession, discipline_in: DisciplineCreate, specialty_id: UUID
    ) -> None:
        await self.create_with_relation(
            session=session,
            obj_in=discipline_in,
            other_model_uuid={"specialty_id": specialty_id},
            model_uuid_name="discipline_id",
        )


class RelationshipComplex(
    RelationshipBase[Discipline, ComplexDiscipline, DisciplineCreate]
):
    ...


class RelationshipPlan(RelationshipBase):
    ...


discipline = CRUDDiscipline(model=Discipline)

discipline_with_complexes = RelationshipComplex(
    model=Discipline,
    relationship_attr=Discipline.complexes,
    m2m_model=ComplexDiscipline,
)

discipline_with_plan = RelationshipPlan(
    model=Discipline, relationship_attr=Discipline.plan_file, m2m_model=None
)

discipline_for_specialty = RelationshipForSpecialty(
    model=Discipline,
    relationship_attr=Specialty.disciplines,
    m2m_model=DisciplineSpecialty,
)
