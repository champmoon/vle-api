from uuid import UUID

from app.schemas.base import BaseSchema
from app.schemas.theme import Theme


class ComplexBase(BaseSchema):
    name: str


class ComplexCreate(ComplexBase):
    ...


class ComplexUpdate(ComplexBase):
    ...


class ComplexInDBBase(ComplexBase):
    id: UUID

    class Config:
        orm_mode = True


class Complex(ComplexInDBBase):
    ...


class ComplexWithThemes(ComplexInDBBase):
    themes: list[Theme]
