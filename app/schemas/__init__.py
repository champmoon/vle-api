from .complex import Complex, ComplexCreate, ComplexUpdate
from .discipline import (
    Discipline,
    DisciplineCreate,
    DisciplineUpdate,
    DisciplineWithComplexes,
)
from .file import File, FileCreate, FileUpdate
from .role import Role, RoleCreate, RoleEnum, RoleUpdate
from .specialty import (
    Specialty,
    SpecialtyCreate,
    SpecialtyUpdate,
    SpecialtyWithDisciplines,
    SpecialtyWithFiles,
)
from .user import User, UserCreate, UserUpdate
