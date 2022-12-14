from datetime import datetime
from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import role
from app.crud.base import CRUDBase
from app.crud.exceptions import RoleNotFound
from app.models import User
from app.schemas import UserCreate, UserUpdate
from app.utils import get_password_hash


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def create(self, session: AsyncSession, obj_in: UserCreate) -> User:
        obj_in_data = jsonable_encoder(obj_in)

        role_obj = await role.get_by_name(
            session=session, role_name=obj_in_data.pop("role_name")
        )
        if role_obj is None:
            raise RoleNotFound

        obj_in_data["hashed_password"] = await get_password_hash(
            obj_in_data.pop("password")
        )

        obj_in_data["is_active"] = False
        obj_in_data["created_at"] = datetime.utcnow()
        obj_in_data["role_id"] = role_obj.id

        db_obj = User(**obj_in_data)  # type: ignore

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        return db_obj

    async def update(
        self, session: AsyncSession, db_obj: User, obj_in: UserUpdate | dict[str, Any]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        password = update_data.pop("password", None)

        if password:
            hashed_password = await get_password_hash(password)
            update_data["hashed_password"] = hashed_password

        return await super().update(session=session, db_obj=db_obj, obj_in=update_data)

    async def get_by_username(
        self, session: AsyncSession, username: str
    ) -> User | None:
        user = await session.execute(
            select(self.model).where(self.model.username == username)
        )
        return user.scalars().first()

    async def get_by_email(self, session: AsyncSession, email: str) -> User | None:
        user = await session.execute(
            select(self.model).where(self.model.email == email)
        )
        return user.scalars().first()


user = CRUDUser(User)
