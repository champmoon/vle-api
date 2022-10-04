from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class RoleEnum(str, Enum):
    ADMIN = "ADMIN"


class RoleBase(BaseModel):
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
