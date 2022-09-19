from typing import Any

from fastapi import FastAPI

app = FastAPI(title="vle-api", description="Virtual Learning Environment API")


@app.get("/hello/{id}")
def get_hello_world(id: int) -> Any:
    return {"msg": f"Hello World_{id}_!!!"}
