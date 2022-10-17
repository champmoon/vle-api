from uuid import UUID

from pydantic import BaseModel


class ComplexBase(BaseModel):
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
