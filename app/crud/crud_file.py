import os
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.crud.base import CRUDBase
from app.crud.crud_specialty import specialty_with_files
from app.models import File, Specialty
from app.schemas import FileCreate, FileUpdate


class CRUDFile(CRUDBase[File, FileCreate, FileUpdate]):
    async def save_file_in_system(
        self, save_path: str, file_name: str, file: UploadFile
    ) -> None:
        if not os.path.isdir(save_path):
            os.mkdir(save_path)

        with open(save_path + file_name, "wb+") as created_file:
            created_file.write(file.file.read())

    async def upload(
        self, session: AsyncSession, spec_obj: Specialty, files: list[UploadFile]
    ) -> None:
        type_spec = spec_obj.type
        save_path = f"{settings.STATIC_FILES_DIR}/{type_spec}/"

        for file in files:
            await self.save_file_in_system(
                save_path=save_path, file_name=file.filename, file=file
            )
            full_save_path = save_path + file.filename

            file_id = uuid4()

            try:
                await super().insert_flush(
                    session=session,
                    insert_statement={"id": file_id, "url": full_save_path},
                )
                await specialty_with_files.relate_flush(
                    session=session,
                    insert_statement={"specialty_id": spec_obj.id, "file_id": file_id},
                )
            except IntegrityError:
                await session.rollback()

        await session.commit()


file = CRUDFile(model=File)
