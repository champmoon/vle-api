# Import all the models for alembic
from app.db.base_class import Base  # noqa
from app.models.complex import Complex  # noqa
from app.models.complex_discipline import ComplexDiscipline  # noqa
from app.models.discipline import Discipline  # noqa
from app.models.discipline_specialty import DisciplineSpecialty  # noqa
from app.models.file import File  # noqa
from app.models.role import Role  # noqa
from app.models.specialty import Specialty  # noqa
from app.models.specialty_file import SpecialtyFile  # noqa
from app.models.theme import Theme  # noqa
from app.models.theme_complex import ThemeComplex  # noqa
from app.models.user import User  # noqa
