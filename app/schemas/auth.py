from app.schemas.base import BaseSchema


class Login(BaseSchema):
    username: str
    password: str
