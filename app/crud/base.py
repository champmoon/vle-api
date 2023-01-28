from typing import Any, Generic, Type, TypeVar
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, selectinload

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

    async def insert_flush(self, session: AsyncSession, insert_statement: dict) -> None:
        await session.execute(insert(self.model).values(**insert_statement))
        await session.flush()

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

    async def remove_flush(self, session: AsyncSession, id: UUID) -> None:
        obj = await session.execute(select(self.model).where(self.model.id == id))
        one_obj = obj.scalar_one()
        await session.delete(one_obj)


ManyToManyModelType = TypeVar("ManyToManyModelType", bound=Base)


class RelationshipBase(Generic[ModelType, ManyToManyModelType, CreateSchemeType]):
    def __init__(
        self,
        model: Type[ModelType],
        m2m_model: Type[ManyToManyModelType] | None,
        relationship_attr: relationship,
    ) -> None:
        self.model = model
        self.relationship_attr = relationship_attr
        self.m2m_model = m2m_model

    async def get(self, session: AsyncSession, id: UUID) -> ModelType | None:
        obj = await session.execute(
            select(self.model)
            .where(self.model.id == id)
            .options(selectinload(self.relationship_attr))
        )
        return obj.scalars().first()

    async def get_multi(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> list[ModelType] | None:
        objs = await session.execute(
            select(self.model)
            .offset(skip)
            .limit(limit)
            .options(selectinload(self.relationship_attr))
        )
        return objs.scalars().all()

    async def get_for(
        self,
        session: AsyncSession,
        m2m_parent_field: Any,
        parent_uuid: UUID,
    ) -> list[ModelType] | None:
        childs = await session.execute(
            select(self.model)
            .join(self.m2m_model)
            .where(m2m_parent_field == parent_uuid)
        )
        return childs.scalars().all()

    async def relate_flush(self, session: AsyncSession, insert_statement: dict) -> None:
        await session.execute(insert(self.m2m_model).values(**insert_statement))
        await session.flush()

    async def create_with_relation(
        self,
        session: AsyncSession,
        model_in: CreateSchemeType,
        model_statement: dict[str, UUID],
        related_model_statement: dict[str, UUID],
    ) -> None:
        obj_in_data = jsonable_encoder(model_in)

        crud_obj: CRUDBase = CRUDBase(model=self.model)

        ((_, model_uuid),) = model_statement.items()

        await crud_obj.insert_flush(
            session=session, insert_statement={"id": model_uuid, **obj_in_data}
        )
        await self.relate_flush(
            session=session,
            insert_statement=model_statement | related_model_statement,
        )
        await session.commit()
