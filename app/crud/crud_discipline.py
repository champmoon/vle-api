from uuid import UUID, uuid4

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase, RelationshipBase
from app.crud.crud_file import file as crud_file
from app.libs.files import SystemFile
from app.models import ComplexDiscipline, Discipline, Specialty
from app.models.discipline_specialty import DisciplineSpecialty
from app.schemas import DisciplineCreate, DisciplineUpdate, FileCreate


class CRUDDiscipline(CRUDBase[Discipline, DisciplineCreate, DisciplineUpdate]):
    async def get_disciplines_for_specialty(
        self, session: AsyncSession, specialty_id: UUID
    ) -> list[Discipline] | None:
        disciplines = await session.execute(
            select(self.model)
            .join(DisciplineSpecialty)
            .where(DisciplineSpecialty.specialty_id == specialty_id)
            .options(selectinload(Discipline.plan_file))
        )
        return disciplines.scalars().all()


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
    ) -> UUID:
        discipline_id = uuid4()

        await self.create_with_relation(
            session=session,
            model_in=discipline_in,
            model_statement={"discipline_id": discipline_id},
            related_model_statement={"specialty_id": specialty_id},
        )

        return discipline_id


class RelationshipComplex(
    RelationshipBase[Discipline, ComplexDiscipline, DisciplineCreate]
):
    ...


class RelationshipPlan(RelationshipBase):
    async def attach(self, session: AsyncSession, plan: UploadFile, id: UUID) -> None:
        file_id = uuid4()

        system_file = SystemFile(
            bytes_buffer=plan.file, dir_path=str(file_id), filename=plan.filename
        )

        file_in = FileCreate(url=system_file.save(), name=plan.filename)
        file_in_data = jsonable_encoder(file_in)

        await crud_file.insert_flush(
            session=session, insert_statement={"id": file_id, **file_in_data}
        )
        await session.execute(
            update(self.model).where(self.model.id == id).values(plan=file_id)
        )
        await session.commit()


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
