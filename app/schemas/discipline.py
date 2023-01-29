from uuid import UUID

from app.schemas.base import BaseSchema
from app.schemas.complex import Complex
from app.schemas.file import File


class DisciplineBase(BaseSchema):
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


class DisciplineForSpecialty(DisciplineInDBBase):
    plan: UUID | None


class DisciplineWithComplexes(DisciplineInDBBase):
    complexes: list[Complex]
