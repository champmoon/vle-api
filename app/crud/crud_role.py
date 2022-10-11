from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Role
from app.schemas import RoleCreate, RoleUpdate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    async def get_by_name(self, session: AsyncSession, role_name: str) -> Role | None:
        obj = await session.execute(
            select(self.model).where(self.model.name == role_name)
        )
        return obj.scalars().first()


role = CRUDRole(Role)
