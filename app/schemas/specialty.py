from uuid import UUID

from app.schemas.base import BaseSchema
from app.schemas.discipline import DisciplineForSpecialty
from app.schemas.file import File


class SpecialtyBase(BaseSchema):
    position: str
    number: str
    year: int


class SpecialtyCreate(SpecialtyBase):
    ...


class SpecialtyUpdate(SpecialtyBase):
    ...


class SpecialtyInDBBase(SpecialtyBase):
    id: UUID

    class Config:
        orm_mode = True


class Specialty(SpecialtyInDBBase):
    ...


class SpecialtyWithFiles(SpecialtyInDBBase):
    files: list[File]


class SpecialtyWithDisciplines(SpecialtyInDBBase):
    disciplines: list[DisciplineForSpecialty]
