from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase, RelationshipBase
from app.models import Complex, ComplexDiscipline, Discipline, ThemeComplex
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


class RelationshipForDiscipline(
    RelationshipBase[Complex, ComplexDiscipline, ComplexCreate]
):
    async def create(
        self, session: AsyncSession, complex_in: ComplexCreate, discipline_id: UUID
    ) -> None:
        await self.create_with_relation(
            session=session,
            model_in=complex_in,
            model_statement={"complex_id": uuid4()},
            related_model_statement={"discipline_id": discipline_id},
        )


class RelationshipTheme(RelationshipBase[Complex, ThemeComplex, ComplexCreate]):
    ...


complex = CRUDComplex(model=Complex)

complex_with_themes = RelationshipTheme(
    model=Complex, relationship_attr=Complex.themes, many_to_many_model=ThemeComplex
)

complex_for_discipline = RelationshipForDiscipline(
    model=Complex,
    relationship_attr=Discipline.complexes,
    many_to_many_model=ComplexDiscipline,
)
