from typing import Any

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.core.settings import settings
from app.libs import Hasher, JWTTokensManager, RoleScope

router = APIRouter()


@router.post("/login/", response_model=schemas.LoginOut, tags=["auth"])
async def login(
    login_in: schemas.LoginIn,
    response: Response,
    session: AsyncSession = Depends(deps.get_session),
) -> Any:
    user_obj = await crud.user.get_by_username(
        session=session, username=login_in.username
    )

    if user_obj is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    is_correct_password = Hasher(login_in.password).verify(
        str(user_obj.hashed_password)
    )

    if not is_correct_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    role_obj = await crud.role.get(
        session=session,
        id=user_obj.role_id,  # type: ignore
    )

    if role_obj is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    token_data = schemas.EncodeTokenData(
        user_id=str(user_obj.id), role=schemas.RoleEnum(role_obj.name)
    )

    response.set_cookie(
        key="token",
        value=JWTTokensManager().create_refresh_token(data=token_data.dict()),
        expires=int(settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60),
        domain="eiee.host",
    )

    return {"user_id": user_obj.id, "username": user_obj.username}


@router.post("/logout/", tags=["auth"])
@deps.auth_required(roles=RoleScope.all())
async def logout(
    response: Response,
    token: str | None = Cookie(include_in_schema=False, default=None),
) -> Any:
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    response.delete_cookie(key="token", domain="eiee.host")
    response.status_code = status.HTTP_200_OK

    return response
