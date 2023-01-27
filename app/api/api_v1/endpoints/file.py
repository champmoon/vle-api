from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/{file_id}/", response_model=schemas.File)
async def read_file(
    file_id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    file = await crud.file.get(session=session, id=file_id)
    if file:
        return file
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No file with this id"
    )


@router.get("/", response_model=list[schemas.File])
async def read_files(session: AsyncSession = Depends(deps.get_session)) -> Any:
    return await crud.file.get_multi(session=session)


@router.delete("/{file_id}/", response_model=schemas.File)
async def delete_file(
    file_id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    file_out = await crud.file.get(session=session, id=file_id)
    if file_out:
        return await crud.file.remove(session=session, id=file_id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No file with this id"
    )
