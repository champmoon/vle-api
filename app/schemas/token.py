from app.schemas import RoleEnum
from app.schemas.base import BaseSchema


class TokenData(BaseSchema):
    user_id: str
    role: RoleEnum


class TokensOut(BaseSchema):
    access_token: str
    refresh_token: str


class OneTokenOut(BaseSchema):
    token: str
