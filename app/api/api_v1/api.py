from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    complex,
    discipline,
    file,
    role,
    specialty,
    theme,
    user,
)

api_router = APIRouter()

api_router.include_router(role.router, prefix="/roles")
api_router.include_router(user.router, prefix="/users")
api_router.include_router(specialty.router, prefix="/specialties")
api_router.include_router(file.router, prefix="/files")
api_router.include_router(discipline.router, prefix="/disciplines")
api_router.include_router(complex.router, prefix="/complexes")
api_router.include_router(theme.router, prefix="/themes")
