from uuid import UUID

from pydantic import BaseModel

from app.schemas.file import File


class SpecialtyBase(BaseModel):
    position: str
    type: str
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
