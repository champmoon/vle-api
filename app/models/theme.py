from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from app.db.base_class import Base
from app.models.file_theme import FileTheme


class Theme(Base):
    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    name = Column(String, nullable=False)

    files: relationship = relationship(
        "File", secondary=FileTheme.__tablename__, lazy="select"
    )
