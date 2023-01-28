from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=list[schemas.Specialty])
async def read_specialties(session: AsyncSession = Depends(deps.get_session)) -> Any:
    return await crud.specialty.get_multi(session=session)


@router.post("/", response_model=schemas.Specialty)
async def create_specialty(
    specialty_in: schemas.SpecialtyCreate,
    session: AsyncSession = Depends(deps.get_session),
) -> Any:
    return await crud.specialty.create(session=session, obj_in=specialty_in)


@router.get("/files/", response_model=list[schemas.SpecialtyWithFiles])
async def read_specialties_with_files(
    session: AsyncSession = Depends(deps.get_session),
) -> Any:
    return await crud.specialty_with_files.get_multi(session=session)


@router.get("/disciplines/", response_model=list[schemas.SpecialtyWithDisciplines])
async def read_specialties_with_disciplines(
    session: AsyncSession = Depends(deps.get_session),
) -> Any:
    return await crud.specialty_with_disciplines.get_multi(session=session)


@router.get("/{specialty_id}/", response_model=schemas.Specialty)
async def read_specialty(
    specialty_id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    specialty_out = await crud.specialty.get(session=session, id=specialty_id)
    if specialty_out:
        return specialty_out
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No specialty with this id"
    )


@router.put("/{specialty_id}/", response_model=schemas.Specialty)
async def update_specialty(
    specialty_id: UUID,
    specialty_in: schemas.SpecialtyUpdate,
    session: AsyncSession = Depends(deps.get_session),
) -> Any:
    specialty_obj = await crud.specialty.get(session=session, id=specialty_id)
    if specialty_obj:
        return await crud.specialty.update(
            session=session, db_obj=specialty_obj, obj_in=specialty_in
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No specialty with this id"
    )


@router.delete("/{specialty_id}/", response_model=schemas.Specialty)
async def delete_specialty(
    specialty_id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    specialty_out = await crud.specialty.get(session=session, id=specialty_id)
    if specialty_out:
        return await crud.specialty.remove(session=session, id=specialty_id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No specialty with this id"
    )


@router.get("/{specialty_id}/files/", response_model=schemas.SpecialtyWithFiles)
async def read_specialty_with_files(
    specialty_id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    specialty_out = await crud.specialty_with_files.get(
        session=session, id=specialty_id
    )
    if specialty_out:
        return specialty_out
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No specialty with this id"
    )


@router.post("/{specialty_id}/files/", response_model=schemas.SpecialtyWithFiles)
async def upload_files_for_specialty(
    specialty_id: UUID,
    files: list[UploadFile],
    session: AsyncSession = Depends(deps.get_session),
) -> Any:
    specialty = await crud.specialty.get(session=session, id=specialty_id)
    if specialty:
        await crud.file_for_specialty.create(
            session=session, files=files, specialty_id=specialty_id
        )
        return await crud.specialty_with_files.get(session=session, id=specialty_id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No specialty with this id"
    )


@router.get(
    "/{specialty_id}/disciplines/", response_model=schemas.SpecialtyWithDisciplines
)
async def read_specialty_with_disciplines(
    specialty_id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    specialty_out = await crud.specialty_with_disciplines.get(
        session=session, id=specialty_id
    )
    if specialty_out:
        return specialty_out
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No specialty with this id"
    )
