from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/{id}", response_model=schemas.Theme)
async def read_theme(
    id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    theme_out = await crud.theme.get(session=session, id=id)
    if theme_out:
        return theme_out
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No theme with this id"
    )


@router.get("/", response_model=list[schemas.Theme])
async def read_themes(session: AsyncSession = Depends(deps.get_session)) -> Any:
    return await crud.theme.get_multi(session=session)


@router.get("/complexes/{complex_id}", response_model=list[schemas.Theme])
async def read_themes_for_complex(
    complex_id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    complex_out = await crud.complex.get(session=session, id=complex_id)
    if complex_out:
        # return await crud.theme.get_themes_for_complex(
        #     session=session, complex_id=complex_id
        # )
        return await crud.theme_for_complex.get_for_complex(
            session=session, complex_id=complex_id
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No complex with this id"
    )


@router.post("/complexes/{complex_id}", response_model=schemas.ComplexWithThemes)
async def create_theme(
    complex_id: UUID,
    theme_in: schemas.ThemeCreate,
    session: AsyncSession = Depends(deps.get_session),
) -> Any:
    complex_out = await crud.complex.get(session=session, id=complex_id)
    if complex_out:
        await crud.theme_for_complex.create(
            session=session, theme_in=theme_in, complex_id=complex_id
        )
        return await crud.complex_with_themes.get(session=session, id=complex_id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No complex with this id"
    )


@router.put("/{id}", response_model=schemas.Theme)
async def update_theme(
    id: UUID,
    theme_in: schemas.ThemeUpdate,
    session: AsyncSession = Depends(deps.get_session),
) -> Any:
    theme_obj = await crud.theme.get(session=session, id=id)
    if theme_obj:
        return await crud.theme.update(
            session=session, db_obj=theme_obj, obj_in=theme_in
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No theme with this id"
    )


@router.delete("/{id}", response_model=schemas.Theme)
async def delete_theme(
    id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    theme_out = await crud.theme.get(session=session, id=id)
    if theme_out:
        return await crud.theme.remove(session=session, id=id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No theme with this id"
    )
