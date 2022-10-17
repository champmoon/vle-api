from uuid import UUID, uuid4

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase, RelationshipBase
from app.crud.crud_discipline import discipline_with_complexes
from app.models import Complex, ComplexDiscipline, ThemeComplex
from app.schemas import ComplexCreate, ComplexUpdate


class CRUDComplex(CRUDBase[Complex, ComplexCreate, ComplexUpdate]):
    async def get_complexs_for_discipline(
        self, session: AsyncSession, discipline_id: UUID
    ) -> list[Complex] | None:
        complexes = await session.execute(
            select(self.model)
            .join(ComplexDiscipline)
            .where(ComplexDiscipline.discipline_id == discipline_id)
        )
        return complexes.scalars().all()

    async def create_with_relation(
        self, session: AsyncSession, complex_in: ComplexCreate, discipline_id: UUID
    ) -> None:
        complex_id = uuid4()
        complex_in_data = jsonable_encoder(complex_in)

        await super().insert_flush(
            session=session,
            insert_statement={"id": complex_id, **complex_in_data},
        )
        await discipline_with_complexes.relate_flush(
            session=session,
            insert_statement={
                "discipline_id": discipline_id,
                "complex_id": complex_id,
            },
        )
        await session.commit()


class RelationshipTheme(RelationshipBase[Complex, ThemeComplex]):
    ...


complex = CRUDComplex(model=Complex)

complex_with_themes = RelationshipTheme(
    model=Complex, relationship_attr=Complex.themes, many_to_many_model=ThemeComplex
)
