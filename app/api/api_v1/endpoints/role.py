from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=list[schemas.Role], tags=["roles"])
async def read_roles(session: AsyncSession = Depends(deps.get_session)) -> Any:
    return await crud.role.get_multi(session=session)
