import asyncio
import logging

from app import crud, schemas
from app.db.session import async_session
from app.schemas.role import RoleEnum

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("pre_start/create-roles")


async def create_roles() -> None:
    async with async_session() as session:

        for role in RoleEnum:
            role_name = role.value

            role_obj = await crud.role.get_by_name(session=session, role_name=role_name)

            if role_obj is None:
                role_in = schemas.RoleCreate(name=RoleEnum(role_name))
                await crud.role.create(session=session, obj_in=role_in)

                logger.info(f"Role - {role_name} has been created...")
            else:
                logger.info(f"Role - {role_name} already exist...")


if __name__ == "__main__":
    asyncio.run(create_roles())
