from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.api_v1.api import api_router

app = FastAPI(
    title="vle-api", description="Virtual Learning Environment API", version="0.1.0"
)

app.mount("/storage", StaticFiles(directory="storage"), name="storage")

app.include_router(api_router)
