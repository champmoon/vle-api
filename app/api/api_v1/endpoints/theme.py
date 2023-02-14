from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.libs import RoleScope

router = APIRouter()


@router.get("/", response_model=list[schemas.Theme], tags=["themes"])
@deps.auth_required(roles=RoleScope.all())
async def read_themes(session: AsyncSession = Depends(deps.get_session)) -> Any:
    return await crud.theme.get_multi(session=session)


@router.get(
    "/files/", response_model=list[schemas.ThemeWithFiles], tags=["themes with files"]
)
@deps.auth_required(roles=RoleScope.all())
async def read_themes_with_files(
    session: AsyncSession = Depends(deps.get_session),
) -> Any:
    return await crud.theme_with_files.get_multi(session=session)


@router.put("/{theme_id}/", response_model=schemas.Theme, tags=["themes"])
@deps.auth_required(roles=RoleScope.exclude("STUDENT"))
async def update_theme(
    theme_id: UUID,
    theme_in: schemas.ThemeUpdate,
    session: AsyncSession = Depends(deps.get_session),
) -> Any:
    theme_obj = await crud.theme.get(session=session, id=theme_id)
    if theme_obj:
        return await crud.theme.update(
            session=session, db_obj=theme_obj, obj_in=theme_in
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No theme with this id"
    )


@router.delete("/{theme_id}/", response_model=schemas.Theme, tags=["themes"])
@deps.auth_required(roles=RoleScope.exclude("STUDENT"))
async def delete_theme(
    theme_id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    theme_out = await crud.theme.get(session=session, id=theme_id)
    if theme_out:
        return await crud.theme.remove(session=session, id=theme_id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No theme with this id"
    )


@router.get("/{theme_id}/", response_model=schemas.Theme, tags=["themes"])
@deps.auth_required(roles=RoleScope.all())
async def read_theme(
    theme_id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    theme_out = await crud.theme.get(session=session, id=theme_id)
    if theme_out:
        return theme_out
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No theme with this id"
    )


@router.get(
    "/{theme_id}/files/",
    response_model=schemas.ThemeWithFiles,
    tags=["themes with files"],
)
@deps.auth_required(roles=RoleScope.all())
async def read_theme_with_files(
    theme_id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    theme_out = await crud.theme_with_files.get(session=session, id=theme_id)
    if theme_out:
        return theme_out
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No theme with this id"
    )


@router.post(
    "/{theme_id}/files/", response_model=schemas.ThemeWithFiles, tags=["upload files"]
)
@deps.auth_required(roles=RoleScope.exclude("STUDENT"))
async def upload_files_for_theme(
    theme_id: UUID,
    files: list[UploadFile],
    session: AsyncSession = Depends(deps.get_session),
) -> Any:
    theme = await crud.theme.get(session=session, id=theme_id)
    if theme:
        await crud.file_for_themes.create_multi(
            session=session, files=files, theme_id=theme_id
        )
        return await crud.theme_with_files.get(session=session, id=theme_id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No theme with this id"
    )


@router.get(
    "/complexes/{complex_id}/", response_model=list[schemas.Theme], tags=["themes"]
)
@deps.auth_required(roles=RoleScope.all())
async def read_themes_for_complex(
    complex_id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    complex_out = await crud.complex.get(session=session, id=complex_id)
    if complex_out:
        return await crud.theme_for_complex.get_for_complex(
            session=session, complex_id=complex_id
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No complex with this id"
    )


@router.get(
    "/complexes/{complex_id}/files/",
    response_model=list[schemas.ThemeWithFiles],
    tags=["themes with files"],
)
@deps.auth_required(roles=RoleScope.all())
async def read_themes_for_complex_with_files(
    complex_id: UUID, session: AsyncSession = Depends(deps.get_session)
) -> Any:
    complex_out = await crud.complex.get(session=session, id=complex_id)
    if complex_out:
        return await crud.theme_for_complex.get_for_complex(
            session=session, complex_id=complex_id
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No complex with this id"
    )


@router.post(
    "/complexes/{complex_id}/",
    response_model=schemas.ComplexWithThemes,
    tags=["themes"],
)
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
