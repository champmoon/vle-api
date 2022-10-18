from uuid import UUID

from pydantic import BaseModel

from app.schemas.complex import Complex
from app.schemas.file import File


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
    plan_file: File | None


class DisciplineWithComplexes(DisciplineInDBBase):
    complexes: list[Complex]
