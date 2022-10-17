from uuid import UUID

from pydantic import BaseModel


class DisciplineBase(BaseModel):
    name: str
    param: str


class DisciplineCreate(DisciplineBase):
    ...


class DisciplineUpdate(DisciplineBase):
    ...


class DisciplineInDBBase(DisciplineBase):
    id: UUID

    class Config:
        orm_mode = True


class Discipline(DisciplineInDBBase):
    ...
