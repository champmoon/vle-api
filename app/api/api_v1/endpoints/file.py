from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.libs import RoleScope

router = APIRouter()


@router.get("/", response_model=list[schemas.File], tags=["files"])
@deps.auth_required(roles=RoleScope.all())
async def read_files(session: AsyncSession = Depends(deps.get_session)) -> Any:
    return await crud.file.get_multi(session=session)


@router.delete("/{file_id}/", response_model=schemas.File, tags=["files"])
@deps.auth_required(roles=RoleScope.exclude("STUDENT"))
async def delete_file(
    file_id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    file_out = await crud.file.get(session=session, id=file_id)
    if file_out:
        return await crud.file.remove(session=session, id=file_id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No file with this id"
    )


@router.get("/{file_id}/", response_model=schemas.File, tags=["files"])
@deps.auth_required(roles=RoleScope.all())
async def read_file(
    file_id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    file = await crud.file.get(session=session, id=file_id)
    if file:
        return file
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No file with this id"
    )


@router.get("/themes/{theme_id}/", response_model=list[schemas.File], tags=["files"])
@deps.auth_required(roles=RoleScope.all())
async def read_files_for_theme(
    theme_id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    theme = await crud.theme.get(session=session, id=theme_id)
    if theme:
        return await crud.file_for_themes.get_for_theme(
            session=session, theme_id=theme_id
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No theme with this id"
    )


@router.get(
    "/specialties/{specialty_id}/", response_model=list[schemas.File], tags=["files"]
)
@deps.auth_required(roles=RoleScope.all())
async def read_files_for_specialty(
    specialty_id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    specialty = await crud.specialty.get(session=session, id=specialty_id)
    if specialty:
        return await crud.file_for_specialty.get_for_specialty(
            session=session, specialty_id=specialty_id
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No specialty with this id"
    )
