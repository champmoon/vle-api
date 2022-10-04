from fastapi import APIRouter

from .role import router as role_router
from .user import router as user_router

api_router = APIRouter()
api_router.include_router(user_router)
api_router.include_router(role_router)
