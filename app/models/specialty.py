from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from app.db.base_class import Base
from app.models.discipline_specialty import DisciplineSpecialty
from app.models.specialty_file import SpecialtyFile


class Specialty(Base):
    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    position = Column(String, nullable=False)
    number = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    files: relationship = relationship(
        "File", secondary=SpecialtyFile.__tablename__, lazy="select"
    )
    disciplines: relationship = relationship(
        "Discipline", secondary=DisciplineSpecialty.__tablename__, lazy="select"
    )
