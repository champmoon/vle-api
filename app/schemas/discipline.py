from uuid import UUID

from pydantic import BaseModel

from app.schemas.complex import Complex


class DisciplineBase(BaseModel):
    name: str


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


class DisciplineWithComplexes(DisciplineInDBBase):
    complexes: list[Complex]
