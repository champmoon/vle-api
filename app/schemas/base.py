from typing import Any

from pydantic import BaseModel


class BaseSchema(BaseModel):
    def dict(self, *args: Any, **kwargs: Any) -> dict:
        kwargs.pop("exclude_none", None)
        return super().dict(*args, exclude_none=True, **kwargs)
