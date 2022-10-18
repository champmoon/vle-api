from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/{id}", response_model=schemas.Complex)
async def read_complex(
    id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    complex_out = await crud.complex.get(session=session, id=id)
    if complex_out:
        return complex_out
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No complex with this id"
    )


@router.get("{id}/themes/", response_model=schemas.ComplexWithThemes)
async def read_complex_with_themes(
    id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    complex_out = await crud.complex_with_themes.get(session=session, id=id)
    if complex_out:
        return complex_out
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No complex with this id"
    )


@router.get("/", response_model=list[schemas.Complex])
async def read_complexes(session: AsyncSession = Depends(deps.get_session)) -> Any:
    return await crud.complex.get_multi(session=session)


@router.get("/themes/", response_model=list[schemas.ComplexWithThemes])
async def read_complexes_with_themes(
    session: AsyncSession = Depends(deps.get_session),
) -> Any:
    return await crud.complex_with_themes.get_multi(session=session)


@router.get("/disciplines/{discipline_id}", response_model=list[schemas.Complex])
async def read_complexes_for_discipline(
    discipline_id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    discipline_out = await crud.discipline.get(session=session, id=discipline_id)
    if discipline_out:
        return await crud.complex.get_complexs_for_discipline(
            session=session, discipline_id=discipline_id
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No specialty with this id"
    )


@router.post(
    "/disciplines/{discipline_id}", response_model=schemas.DisciplineWithComplexes
)
async def create_complex(
    discipline_id: UUID,
    complex_in: schemas.ComplexCreate,
    session: AsyncSession = Depends(deps.get_session),
) -> Any:
    discipline_out = await crud.discipline.get(session=session, id=discipline_id)
    if discipline_out:
        await crud.complex.create_with_relation(
            session=session, complex_in=complex_in, discipline_id=discipline_id
        )
        return await crud.discipline_with_complexes.get(
            session=session, id=discipline_id
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No discipline with this id"
    )


@router.put("/{id}", response_model=schemas.Complex)
async def update_complex(
    id: UUID,
    complex_in: schemas.ComplexUpdate,
    session: AsyncSession = Depends(deps.get_session),
) -> Any:
    complex_obj = await crud.complex.get(session=session, id=id)
    if complex_obj:
        return await crud.complex.update(
            session=session, db_obj=complex_obj, obj_in=complex_in
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No complex with this id"
    )


@router.delete("/{id}", response_model=schemas.Complex)
async def delete_complex(
    id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    complex_out = await crud.complex.get(session=session, id=id)
    if complex_out:
        return await crud.complex.remove(session=session, id=id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No complex with this id"
    )
