from uuid import UUID, uuid4

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase, RelationshipBase
from app.crud.crud_complex import complex_with_themes
from app.models import FileTheme, Theme, ThemeComplex
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

    async def create_with_relation(
        self, session: AsyncSession, theme_in: ThemeCreate, complex_id: UUID
    ) -> None:
        theme_id = uuid4()
        theme_in_data = jsonable_encoder(theme_in)

        await super().insert_flush(
            session=session,
            insert_statement={"id": theme_id, **theme_in_data},
        )
        await complex_with_themes.relate_flush(
            session=session,
            insert_statement={
                "complex_id": complex_id,
                "theme_id": theme_id,
            },
        )
        await session.commit()


class RelationshipFiles(RelationshipBase[Theme, FileTheme]):
    ...


theme = CRUDTheme(model=Theme)

theme_with_files = RelationshipFiles(
    model=Theme,
    relationship_attr=Theme.files,
    many_to_many_model=FileTheme,
)
