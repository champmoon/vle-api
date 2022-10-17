from fastapi import APIRouter

from app.api.api_v1.endpoints import complex, discipline, file, role, specialty, user

api_router = APIRouter()

api_router.include_router(role.router, prefix="/roles", tags=["roles"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(specialty.router, prefix="/specialties", tags=["specialties"])
api_router.include_router(file.router, prefix="/files", tags=["files"])
api_router.include_router(
    discipline.router, prefix="/disciplines", tags=["disciplines"]
)
api_router.include_router(complex.router, prefix="/complexes", tags=["complexes"])
