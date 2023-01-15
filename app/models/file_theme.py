from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text

from app.db.base_class import Base


class FileTheme(Base):
    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    file_id = Column(UUID(as_uuid=True), ForeignKey("file.id", ondelete="CASCADE"))
    theme_id = Column(UUID(as_uuid=True), ForeignKey("theme.id", ondelete="CASCADE"))
