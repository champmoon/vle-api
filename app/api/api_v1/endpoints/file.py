from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.post("/specialies/{specialy_id}", response_model=schemas.SpecialtyWithFiles)
async def upload_files(
    specialty_id: UUID,
    file: UploadFile,
    session: AsyncSession = Depends(deps.get_session),
) -> Any:
    specialty = await crud.specialty.get(session=session, id=specialty_id)
    if specialty:
        await crud.file_for_specialty.create(
            session=session, file=file, specialty_id=specialty_id
        )
        return await crud.specialty_with_files.get(session=session, id=specialty_id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No specialty with this id"
    )


@router.get("/{id}", response_model=schemas.File)
async def read_file(id: UUID, session: AsyncSession = Depends(deps.get_session)) -> Any:
    file = await crud.file.get(session=session, id=id)
    if file:
        return file
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No file with this id"
    )


@router.get("/", response_model=list[schemas.File])
async def read_files(session: AsyncSession = Depends(deps.get_session)) -> Any:
    return await crud.file.get_multi(session=session)


@router.delete("/{id}", response_model=schemas.File)
async def delete_file(
    id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    file_out = await crud.file.get(session=session, id=id)
    if file_out:
        return await crud.file.remove(session=session, id=id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No file with this id"
    )
