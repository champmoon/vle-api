from uuid import UUID

from app.schemas.base import BaseSchema


class FileBase(BaseSchema):
    name: str
    url: str


class FileCreate(FileBase):
    ...


class FileUpdate(FileBase):
    ...


class FileInDBBase(FileBase):
    id: UUID

    class Config:
        orm_mode = True


class File(FileInDBBase):
    ...
