from uuid import UUID

from pydantic import BaseModel

from app.schemas.file import File


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


class ThemeWithFiles(ThemeInDBBase):
    files: list[File]
