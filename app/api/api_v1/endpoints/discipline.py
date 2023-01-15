from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/{id}", response_model=schemas.Discipline)
async def read_discipline(
    id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    discipline = await crud.discipline_with_plan.get(session=session, id=id)
    if discipline:
        return discipline
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No discipline with this id"
    )


@router.get("{id}/complexes/", response_model=schemas.DisciplineWithComplexes)
async def read_discipline_with_complexes(
    id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    discipline = await crud.discipline_with_complexes.get(session=session, id=id)
    if discipline:
        return discipline
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No discipline with this id"
    )


@router.get("/", response_model=list[schemas.Discipline])
async def read_disciplines(session: AsyncSession = Depends(deps.get_session)) -> Any:
    return await crud.discipline_with_plan.get_multi(session=session)


@router.get("/complexes/", response_model=list[schemas.DisciplineWithComplexes])
async def read_disciplines_with_complexes(
    session: AsyncSession = Depends(deps.get_session),
) -> Any:
    return await crud.discipline_with_complexes.get_multi(session=session)


@router.get("/specialies/{specialy_id}", response_model=list[schemas.Discipline])
async def read_disciplines_for_specialty(
    specialy_id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    specialty = await crud.specialty.get(session=session, id=specialy_id)
    if specialty:
        return await crud.discipline_for_specialty.get_for_specialty(
            session=session, specialty_id=specialy_id
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No specialty with this id"
    )


@router.post(
    "/specialies/{specialy_id}", response_model=schemas.SpecialtyWithDisciplines
)
async def create_discipline(
    specialy_id: UUID,
    discipline_in: schemas.DisciplineCreate,
    session: AsyncSession = Depends(deps.get_session),
) -> Any:
    specialty = await crud.specialty.get(session=session, id=specialy_id)
    if specialty:
        await crud.discipline_for_specialty.create(
            session=session, discipline_in=discipline_in, specialty_id=specialy_id
        )
        return await crud.specialty_with_disciplines.get(
            session=session, id=specialy_id
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No specialty with this id"
    )


@router.post("/plan/{id}", response_model=schemas.Discipline)
async def attach_plan(
    id: UUID,
    plan: UploadFile,
    session: AsyncSession = Depends(deps.get_session),
) -> Any:
    discipline_out = await crud.discipline.get(session=session, id=id)
    if discipline_out:
        await crud.discipline.attach_plan(session=session, id=id, plan=plan)
        return await crud.discipline_with_plan.get(session=session, id=id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No discipline with this id"
    )


@router.put("/{id}", response_model=schemas.Discipline)
async def update_discipline(
    id: UUID,
    discipline_in: schemas.DisciplineUpdate,
    session: AsyncSession = Depends(deps.get_session),
) -> Any:
    discipline_obj = await crud.discipline.get(session=session, id=id)
    if discipline_obj:
        return await crud.discipline.update(
            session=session, db_obj=discipline_obj, obj_in=discipline_in
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No discipline with this id"
    )


@router.delete("/{id}", response_model=schemas.Discipline)
async def delete_discipline(
    id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    discipline_out = await crud.discipline.get(session=session, id=id)
    if discipline_out:
        return await crud.discipline.remove(session=session, id=id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No discipline with this id"
    )
