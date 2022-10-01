from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates
from sqlalchemy.sql.expression import text

from app.db.base_class import Base


class Role(Base):
    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    name = Column(String, unique=True)

    @validates("name")
    def validate_role(self, col_name: str, col_value: str) -> str | ValueError:
        if not col_value.isupper():
            raise ValueError("role name must be in uppercase")
        return col_value
