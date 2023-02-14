from uuid import UUID

from app.schemas import RoleEnum
from app.schemas.base import BaseSchema


class EncodeTokenData(BaseSchema):
    user_id: str
    role: RoleEnum


class DecodeTokenData(BaseSchema):
    user_id: UUID
    role: RoleEnum


class TokensOut(BaseSchema):
    access_token: str
    refresh_token: str


class OneTokenOut(BaseSchema):
    token: str
