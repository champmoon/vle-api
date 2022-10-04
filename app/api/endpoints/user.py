from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.api.exceptions import details, user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{id}", response_model=schemas.User)
async def read_user(id: UUID, session: AsyncSession = Depends(deps.get_session)) -> Any:
    try:
        return await crud.user.get(session=session, id=id)
    except NoResultFound:
        raise user.GetUserIdError


@router.get("/", response_model=list[schemas.User])
async def read_users(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    return await crud.user.get_multi(session=session, skip=skip, limit=limit)


@router.post("/", response_model=schemas.User)
async def create_user(
    user_in: schemas.UserCreate, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    try:
        return await crud.user.create(session=session, obj_in=user_in)
    except IntegrityError as err:
        if details.USERNAME_DUPLICATE_KEY in str(err):
            raise user.CreateUniqueUsernameError
        raise user.CreateUniqueEmailError


@router.put("/{id}", response_model=schemas.User)
async def update_user(
    id: UUID,
    user_in: schemas.UserUpdate,
    session: AsyncSession = Depends(deps.get_session),
) -> Any:
    try:
        user_obj = await crud.user.get(session=session, id=id)
        return await crud.user.update(session=session, db_obj=user_obj, obj_in=user_in)
    except NoResultFound:
        raise user.GetUserIdError


@router.delete("/{id}", response_model=schemas.User)
async def delete_user(
    id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    try:
        return await crud.user.remove(session=session, id=id)
    except NoResultFound:
        raise user.GetUserIdError
