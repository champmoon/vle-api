from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text

from app.db.base_class import Base


class Discipline(Base):
    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    name = Column(String, nullable=False)
    param = Column(String, nullable=False)
