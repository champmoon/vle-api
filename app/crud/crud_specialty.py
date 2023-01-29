import json

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.crud.base import CRUDBase, RelationshipBase
from app.models import DisciplineSpecialty, Specialty, SpecialtyFile
from app.schemas import (
    ComplexCreate,
    DisciplineCreate,
    SpecialtyCreate,
    SpecialtyUpdate,
)

DEFAULT_SPECIALTY_JSON_PATH = "app/json/default_specialty.json"


class CRUDSpecialty(CRUDBase[Specialty, SpecialtyCreate, SpecialtyUpdate]):
    async def default_create(
        self, session: AsyncSession, obj_in: SpecialtyCreate
    ) -> Specialty:
        specialty_out = await self.create(session=session, obj_in=obj_in)

        default_data = []
        with open(DEFAULT_SPECIALTY_JSON_PATH) as f:
            default_data = json.load(f)

        specialty_id = specialty_out.id
        for discipline_for_specialty in default_data:
            discipline_name = discipline_for_specialty["name"]

            discipline_in = DisciplineCreate(name=discipline_name)

            discipline_id = await crud.discipline_for_specialty.create(
                session=session, discipline_in=discipline_in, specialty_id=specialty_id  # type: ignore
            )

            complexes_for_discipline = discipline_for_specialty["complexes"]
            for complex_for_discipline in complexes_for_discipline:
                complex_name = complex_for_discipline["name"]

                complex_in = ComplexCreate(name=complex_name)

                await crud.complex_for_discipline.create(
                    session=session, complex_in=complex_in, discipline_id=discipline_id
                )

        await session.refresh(specialty_out)
        return specialty_out


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
