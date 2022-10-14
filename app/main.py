from fastapi import FastAPI
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
