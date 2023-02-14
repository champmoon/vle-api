from uuid import UUID

from app.schemas.base import BaseSchema


class LoginIn(BaseSchema):
    username: str
    password: str


class LoginOut(BaseSchema):
    user_id: UUID
    username: str
