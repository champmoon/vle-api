from fastapi import FastAPI

from app.api.api_v1.api import api_router

app = FastAPI(
    title="vle-api", description="Virtual Learning Environment API", version="0.1.0"
)

app.include_router(api_router)
