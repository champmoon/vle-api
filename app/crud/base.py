from typing import Any, Generic, Type, TypeVar
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemeType = TypeVar("CreateSchemeType", bound=BaseModel)
UpdateSchemeType = TypeVar("UpdateSchemeType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemeType, UpdateSchemeType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def get(self, session: AsyncSession, id: UUID) -> ModelType | None:
        obj = await session.execute(select(self.model).where(self.model.id == id))
        return obj.scalars().first()

    async def get_multi(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> list[ModelType] | None:
        objs = await session.execute(select(self.model).offset(skip).limit(limit))
        return objs.scalars().all()

    async def create(
        self, session: AsyncSession, obj_in: CreateSchemeType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        session: AsyncSession,
        db_obj: ModelType,
        obj_in: UpdateSchemeType | dict[str, Any],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, session: AsyncSession, id: UUID) -> ModelType:
        obj = await session.execute(select(self.model).where(self.model.id == id))
        one_obj = obj.scalar_one()
        await session.delete(one_obj)
        await session.commit()
        return one_obj
