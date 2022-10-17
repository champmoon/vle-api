from uuid import UUID

from pydantic import BaseModel


class ThemeBase(BaseModel):
    name: str


class ThemeCreate(ThemeBase):
    ...


class ThemeUpdate(ThemeBase):
    ...


class ThemeInDBBase(ThemeBase):
    id: UUID

    class Config:
        orm_mode = True


class Theme(ThemeInDBBase):
    ...
