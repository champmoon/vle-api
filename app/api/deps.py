import json
from functools import wraps
from inspect import Parameter, signature
from typing import Any, AsyncGenerator, Callable

from fastapi import Cookie, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.db.session import async_session
from app.libs import JWTTokensManager
from app.models import User


async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        yield session


async def get_token_data_from_cookie(
    response: Response,
    token: str | None = Cookie(include_in_schema=False, default=None),
) -> schemas.DecodeTokenData:
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    decoded_data = JWTTokensManager().decode_refresh_token(token)
    if decoded_data is None:
        response.delete_cookie(key="token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return schemas.DecodeTokenData(**json.loads(decoded_data["sub"]))


async def get_current_user(
    response: Response,
    token_data: schemas.DecodeTokenData = Depends(get_token_data_from_cookie),
    session: AsyncSession = Depends(get_session),
) -> User:
    user_obj = await crud.user.get(session=session, id=token_data.user_id)

    if user_obj is None:
        response.delete_cookie(key="token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user_obj


def auth_required(roles: list[schemas.RoleEnum]) -> Callable:
    def auth(fastapi_endpoint: Callable) -> Callable:
        @wraps(fastapi_endpoint)
        async def wrapper(
            *args: Any,
            token_data: schemas.DecodeTokenData = Depends(get_token_data_from_cookie),
            **kwargs: Any
        ) -> Any:
            if token_data.role in roles:
                return await fastapi_endpoint(*args, **kwargs)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        params = list(signature(fastapi_endpoint).parameters.values())
        params.append(
            Parameter(
                "token_data",
                annotation=schemas.DecodeTokenData,
                kind=Parameter.KEYWORD_ONLY,
                default=Depends(get_token_data_from_cookie),
            )
        )

        setattr(
            fastapi_endpoint,
            "__signature__",
            signature(fastapi_endpoint).replace(parameters=tuple(params)),
        )

        return wrapper

    return auth
