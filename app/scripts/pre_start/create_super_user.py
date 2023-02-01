import asyncio
import logging

from app import crud, schemas
from app.core.settings import settings
from app.db.session import async_session
from app.schemas.role import RoleEnum

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("pre_start/create-super-user")


async def create_super_user() -> None:
    super_user_role = RoleEnum.ADMIN

    async with async_session() as session:
        user = await crud.user.get_by_username(
            session=session, username=settings.SUPER_USER_USERNAME
        )
        if user is None:
            user_in = schemas.UserCreate(
                username=settings.SUPER_USER_USERNAME,
                name="admin",
                surname="admin",
                password=settings.SUPER_USER_PASSWORD,
                email=settings.SUPER_USER_EMAIL,  # type: ignore
                role_name=super_user_role,
            )
            await crud.user.create(session=session, obj_in=user_in)

            logger.info(f"Super user has been created, role - {super_user_role}...")
        else:
            logger.info(f"Super user already exist, role - {super_user_role}...")


if __name__ == "__main__":
    asyncio.run(create_super_user())
