from enum import Enum
from uuid import UUID

from app.schemas.base import BaseSchema


class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"


class RoleBase(BaseSchema):
    name: RoleEnum


class RoleCreate(RoleBase):
    ...


class RoleUpdate(RoleBase):
    ...


class RoleInBDBase(RoleBase):
    id: UUID

    class Config:
        orm_mode = True


class Role(RoleInBDBase):
    ...
