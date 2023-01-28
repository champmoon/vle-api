from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase, RelationshipBase
from app.models import Complex, Theme, ThemeComplex, FileTheme
from app.schemas import ThemeCreate, ThemeUpdate


class CRUDTheme(CRUDBase[Theme, ThemeCreate, ThemeUpdate]):
    ...


class RelationshipFiles(RelationshipBase[Theme, FileTheme, ThemeCreate]):
    ...


class RelationshipForComplex(RelationshipBase[Theme, ThemeComplex, ThemeCreate]):
    async def get_for_complex(
        self, session: AsyncSession, complex_id: UUID
    ) -> list[Theme] | None:
        return await self.get_for(
            session=session,
            m2m_parent_field=ThemeComplex.complex_id,
            parent_uuid=complex_id,
        )

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

theme_with_files = RelationshipFiles(
    model=Theme, relationship_attr=Theme.files, m2m_model=FileTheme
)

theme_for_complex = RelationshipForComplex(
    model=Theme, relationship_attr=Complex.themes, m2m_model=ThemeComplex
)
