from uuid import UUID

from app.schemas import RoleEnum
from app.schemas.base import BaseSchema


class Token(BaseSchema):
    user_id: UUID
    role: RoleEnum
