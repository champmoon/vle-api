from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text

from app.db.base_class import Base


class ThemeComplex(Base):
    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    theme_id = Column(UUID(as_uuid=True), ForeignKey("theme.id", ondelete="CASCADE"))
    complex_id = Column(
        UUID(as_uuid=True), ForeignKey("complex.id", ondelete="CASCADE")
    )
