from uuid import UUID

from pydantic import BaseModel


class FileBase(BaseModel):
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
