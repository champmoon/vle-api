from uuid import UUID, uuid4

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.settings import settings
from app.crud.base import CRUDBase, RelationshipBase
from app.crud.crud_file import file
from app.crud.crud_specialty import specialty_with_disciplines
from app.models import ComplexDiscipline, Discipline, File
from app.models.discipline_specialty import DisciplineSpecialty
from app.schemas import DisciplineCreate, DisciplineUpdate


class CRUDDiscipline(CRUDBase[Discipline, DisciplineCreate, DisciplineUpdate]):
    async def get_disciplines_for_specialty(
        self, session: AsyncSession, specialty_id: UUID
    ) -> list[Discipline] | None:
        disciplines = await session.execute(
            select(self.model)
            .join(DisciplineSpecialty)
            .where(DisciplineSpecialty.specialty_id == specialty_id)
        )
        return disciplines.scalars().all()

    async def create_with_relation(
        self, session: AsyncSession, discipline_in: DisciplineCreate, specialty_id: UUID
    ) -> None:
        discipline_id = uuid4()
        discipline_in_data = jsonable_encoder(discipline_in)

        await super().insert_flush(
            session=session,
            insert_statement={"id": discipline_id, **discipline_in_data},
        )
        await specialty_with_disciplines.relate_flush(
            session=session,
            insert_statement={
                "specialty_id": specialty_id,
                "discipline_id": discipline_id,
            },
        )
        await session.commit()

    async def attach_plan(
        self, session: AsyncSession, id: UUID, plan: UploadFile
    ) -> None:
        save_path = f"{settings.STATIC_FILES_DIR}/plans/{id}/"

        await file.save_file_in_system(save_path=save_path, file_name=plan.filename, file=plan)

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
                select(File)
                .where(File.url == full_save_path)
            )
            file_id = file_obj.scalar_one().id

        await session.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(plan=file_id)
        )
        await session.commit()


class RelationshipComplex(RelationshipBase[Discipline, ComplexDiscipline]):
    ...


class RelationshipPlan(RelationshipBase):
    ...


discipline = CRUDDiscipline(model=Discipline)

discipline_with_complexes = RelationshipComplex(
    model=Discipline,
    relationship_attr=Discipline.complexes,
    many_to_many_model=ComplexDiscipline,
)

discipline_with_plan = RelationshipPlan(
    model=Discipline,
    relationship_attr=Discipline.plan_file,
    many_to_many_model=None
)
