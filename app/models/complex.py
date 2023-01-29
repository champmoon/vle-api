from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from app.db.base_class import Base
from app.models.theme_complex import ThemeComplex


class Complex(Base):
    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    name = Column(String, nullable=False)

    themes: relationship = relationship(
        "Theme",
        secondary=ThemeComplex.__tablename__,
        lazy="select",
        cascade="all, delete",
    )
