from app.crud.base import CRUDBase, RelationshipBase
from app.models import Specialty, SpecialtyFile
from app.schemas import SpecialtyCreate, SpecialtyUpdate


class CRUDSpecialty(CRUDBase[Specialty, SpecialtyCreate, SpecialtyUpdate]):
    ...


class RelationshipFiles(RelationshipBase[Specialty, SpecialtyFile]):
    ...


specialty = CRUDSpecialty(model=Specialty)

specialty_with_files = RelationshipFiles(
    model=Specialty, relationship_attr=Specialty.files, many_to_many_model=SpecialtyFile
)
