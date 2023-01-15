from uuid import UUID

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
    ) -> None:
        await self.create_with_relation(
            session=session,
            obj_in=complex_in,
            other_model_uuid={"discipline_id": discipline_id},
            model_uuid_name="complex_id",
        )


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
