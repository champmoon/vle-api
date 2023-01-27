from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase, RelationshipBase
from app.models import Complex, Theme, ThemeComplex
from app.schemas import ThemeCreate, ThemeUpdate


class CRUDTheme(CRUDBase[Theme, ThemeCreate, ThemeUpdate]):
    async def get_themes_for_complex(
        self, session: AsyncSession, complex_id: UUID
    ) -> list[Theme] | None:
        themes = await session.execute(
            select(self.model)
            .join(ThemeComplex)
            .where(ThemeComplex.complex_id == complex_id)
        )
        return themes.scalars().all()


class RelationshipForComplex(RelationshipBase[Theme, ThemeComplex, ThemeCreate]):
    async def create(
        self, session: AsyncSession, theme_in: ThemeCreate, complex_id: UUID
    ) -> None:
        await self.create_with_relation(
            session=session,
            model_in=theme_in,
            model_statement={"theme_id": uuid4()},
            related_model_statement={"complex_id": complex_id},
        )


theme = CRUDTheme(model=Theme)

theme_for_complex = RelationshipForComplex(
    model=Theme, relationship_attr=Complex.themes, many_to_many_model=ThemeComplex
)
