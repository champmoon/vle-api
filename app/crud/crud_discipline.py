from uuid import UUID, uuid4

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.crud.crud_specialty import specialty_with_disciplines
from app.models import Discipline
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


discipline = CRUDDiscipline(model=Discipline)
