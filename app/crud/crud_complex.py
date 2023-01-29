from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase, RelationshipBase
from app.models import Complex, ComplexDiscipline, Discipline, ThemeComplex
from app.schemas import ComplexCreate, ComplexUpdate


class CRUDComplex(CRUDBase[Complex, ComplexCreate, ComplexUpdate]):
    ...


class RelationshipForDiscipline(
    RelationshipBase[Complex, ComplexDiscipline, ComplexCreate]
):
    async def get_for_discipline(
        self, session: AsyncSession, discipline_id: UUID
    ) -> list[Complex] | None:
        return await self.get_for(
            session=session,
            m2m_parent_field=ComplexDiscipline.discipline_id,
            parent_uuid=discipline_id,
        )

    async def create(
        self, session: AsyncSession, complex_in: ComplexCreate, discipline_id: UUID
    ) -> UUID:
        complex_id = uuid4()

        await self.create_with_relation(
            session=session,
            model_in=complex_in,
            model_statement={"complex_id": complex_id},
            related_model_statement={"discipline_id": discipline_id},
        )

        return complex_id


class RelationshipTheme(RelationshipBase[Complex, ThemeComplex, ComplexCreate]):
    ...


complex = CRUDComplex(model=Complex)

complex_with_themes = RelationshipTheme(
    model=Complex, relationship_attr=Complex.themes, m2m_model=ThemeComplex
)

complex_for_discipline = RelationshipForDiscipline(
    model=Complex,
    relationship_attr=Discipline.complexes,
    m2m_model=ComplexDiscipline,
)
