from app.crud.base import CRUDBase, RelationshipBase
from app.models import DisciplineSpecialty, Specialty, SpecialtyFile
from app.schemas import SpecialtyCreate, SpecialtyUpdate


class CRUDSpecialty(CRUDBase[Specialty, SpecialtyCreate, SpecialtyUpdate]):
    ...


class RelationshipFiles(RelationshipBase[Specialty, SpecialtyFile, SpecialtyCreate]):
    ...


class RelationshipDiscipline(
    RelationshipBase[Specialty, DisciplineSpecialty, SpecialtyCreate]
):
    ...


specialty = CRUDSpecialty(model=Specialty)

specialty_with_files = RelationshipFiles(
    model=Specialty, relationship_attr=Specialty.files, m2m_model=SpecialtyFile
)

specialty_with_disciplines = RelationshipDiscipline(
    model=Specialty,
    relationship_attr=Specialty.disciplines,
    m2m_model=DisciplineSpecialty,
)
