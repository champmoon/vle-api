from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase, RelationshipBase
from app.models import Complex, FileTheme, Theme, ThemeComplex
from app.schemas import ThemeCreate, ThemeUpdate


class CRUDTheme(CRUDBase[Theme, ThemeCreate, ThemeUpdate]):
    ...


class RelationshipFiles(RelationshipBase[Theme, FileTheme, ThemeCreate]):
    ...


class RelationshipForComplex(RelationshipBase[Theme, ThemeComplex, ThemeCreate]):
    async def get_for_complex(
        self, session: AsyncSession, complex_id: UUID
    ) -> list[Theme] | None:
        childs = await session.execute(
            select(self.model)
            .join(self.m2m_model)
            .where(ThemeComplex.complex_id == complex_id)
            .options(selectinload(Theme.files))
        )
        return childs.scalars().all()

    async def get_for_complex_with_files(
        self, session: AsyncSession, complex_id: UUID
    ) -> list[Theme] | None:
        complexes_with_files = await session.execute(
            select(self.model)
            .join(ThemeComplex)
            .where(ThemeComplex.complex_id == complex_id)
            .options(selectinload(Theme.files))
        )
        return complexes_with_files.scalars().all()

    async def create(
        self, session: AsyncSession, theme_in: ThemeCreate, complex_id: UUID
    ) -> UUID:
        theme_id = uuid4()

        await self.create_with_relation(
            session=session,
            model_in=theme_in,
            model_statement={"theme_id": theme_id},
            related_model_statement={"complex_id": complex_id},
        )

        return theme_id


theme = CRUDTheme(model=Theme)

theme_with_files = RelationshipFiles(
    model=Theme, relationship_attr=Theme.files, m2m_model=FileTheme
)

theme_for_complex = RelationshipForComplex(
    model=Theme, relationship_attr=Complex.themes, m2m_model=ThemeComplex
)
