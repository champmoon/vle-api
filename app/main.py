from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.api_v1.api import api_router
from app.core.settings import settings

app = FastAPI(
    title="vle-api", description="Virtual Learning Environment API", version="0.1.0"
)

app.mount(
    "/" + settings.STATIC_FILES_DIR,
    StaticFiles(directory=settings.STATIC_FILES_DIR),
)

app.include_router(api_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
