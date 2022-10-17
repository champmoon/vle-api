from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text

from app.db.base_class import Base


class ComplexDiscipline(Base):
    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    complex_id = Column(
        UUID(as_uuid=True), ForeignKey("complex.id", ondelete="CASCADE")
    )
    discipline_id = Column(
        UUID(as_uuid=True), ForeignKey("discipline.id", ondelete="CASCADE")
    )
