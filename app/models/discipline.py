from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from app.db.base_class import Base
from app.models.complex_discipline import ComplexDiscipline


class Discipline(Base):
    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    name = Column(String, nullable=False)
    plan = Column(UUID(as_uuid=True), ForeignKey("file.id", ondelete="CASCADE"))

    complexes: relationship = relationship(
        "Complex", secondary=ComplexDiscipline.__tablename__, lazy="select"
    )
    plan_file: relationship = relationship("File", foreign_keys=[plan])
