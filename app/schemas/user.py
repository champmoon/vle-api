from uuid import UUID

from pydantic import EmailStr

from app.schemas import RoleEnum
from app.schemas.base import BaseSchema


class UserBase(BaseSchema):
    username: str
    name: str
    surname: str
    patronymic: str | None = None


class UserCreate(UserBase):
    username: str
    password: str
    email: EmailStr | None = None
    role_name: RoleEnum


class UserUpdate(UserBase):
    password: str | None = None


class UserInDBBase(UserBase):
    id: UUID

    class Config:
        orm_mode = True


class User(UserInDBBase):
    ...
