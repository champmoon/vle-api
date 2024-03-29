from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.libs import RoleScope

router = APIRouter()


@router.get("/", response_model=list[schemas.User], tags=["users"])
@deps.auth_required(roles=RoleScope.all())
async def read_users(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    return await crud.user.get_multi(session=session, skip=skip, limit=limit)


@router.post("/", response_model=schemas.User, tags=["users"])
@deps.auth_required(roles=RoleScope.exclude("STUDENT"))
async def create_user(
    user_in: schemas.UserCreate, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    user_by_username = await crud.user.get_by_username(
        session=session, username=user_in.username
    )
    if user_by_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Already exists user with this username",
        )

    if user_in.email:
        user_by_email = await crud.user.get_by_email(
            session=session, email=user_in.email
        )
        if user_by_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Already exists user with this email",
            )

    return await crud.user.create(session=session, obj_in=user_in)


@router.put("/{user_id}/", response_model=schemas.User, tags=["users"])
@deps.auth_required(roles=RoleScope.exclude("STUDENT"))
async def update_user(
    user_id: UUID,
    user_in: schemas.UserUpdate,
    session: AsyncSession = Depends(deps.get_session),
) -> Any:
    user_obj = await crud.user.get(session=session, id=user_id)
    if user_obj:
        return await crud.user.update(session=session, db_obj=user_obj, obj_in=user_in)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No user with this id"
    )


@router.delete("/{user_id}/", response_model=schemas.User, tags=["users"])
@deps.auth_required(roles=RoleScope.exclude("STUDENT"))
async def delete_user(
    user_id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    user_out = await crud.user.get(session=session, id=user_id)
    if user_out:
        return await crud.user.remove(session=session, id=user_id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No user with this id"
    )


@router.get("/{user_id}/", response_model=schemas.User, tags=["users"])
@deps.auth_required(roles=RoleScope.all())
async def read_user(
    user_id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    user_out = await crud.user.get(session=session, id=user_id)
    if user_out:
        return user_out
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No user with this id"
    )


@router.get("/{email}/email/", response_model=schemas.User, tags=["users"])
@deps.auth_required(roles=RoleScope.all())
async def read_user_by_email(
    email: EmailStr, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    user_out = await crud.user.get_by_email(session=session, email=email)
    if user_out:
        return user_out
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No user with this email"
    )


@router.get("/{username}/username/", response_model=schemas.User, tags=["users"])
@deps.auth_required(roles=RoleScope.all())
async def read_user_by_username(
    username: str, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    user_out = await crud.user.get_by_username(session=session, username=username)
    if user_out:
        return user_out
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No user with this username"
    )
