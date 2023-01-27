from .crud_complex import complex, complex_for_discipline, complex_with_themes
from .crud_discipline import (
    discipline,
    discipline_for_specialty,
    discipline_with_complexes,
    discipline_with_plan,
)
from .crud_file import file, file_for_specialty
from .crud_role import role
from .crud_specialty import specialty, specialty_with_disciplines, specialty_with_files
from .crud_theme import theme, theme_for_complex
from .crud_user import user
