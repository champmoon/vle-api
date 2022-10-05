from fastapi import APIRouter

from app.api.api_v1.endpoints import role, user

api_router = APIRouter()

api_router.include_router(role.router, prefix="/roles", tags=["roles"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
