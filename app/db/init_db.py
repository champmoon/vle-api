from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.core.settings import settings
from app.schemas.role import RoleEnum


async def create_admin_role(session: AsyncSession) -> None:
    role_in = schemas.RoleCreate(name=RoleEnum.ADMIN)
    await crud.role.create(session=session, obj_in=role_in)


async def create_first_admin(session: AsyncSession) -> None:
    user_in = schemas.UserCreate(
        username=settings.FIRST_ADMIN_USERNAME,
        name="admin",
        surname="admin",
        password=settings.FIRST_ADMIN_PASSWORD,
        role_name=RoleEnum.ADMIN,
    )
    await crud.user.create(session=session, obj_in=user_in)


async def init_db(session: AsyncSession) -> None:
    user = await crud.user.get_by_username(
        session=session, username=settings.FIRST_ADMIN_USERNAME
    )
    if not user:
        await create_admin_role(session=session)
        await create_first_admin(session=session)
