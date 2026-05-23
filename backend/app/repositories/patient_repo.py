from typing import Optional, List
from app.repositories.base import BaseRepository
from app.models.patient import PatientDemographics
from app.schemas.patient import PatientCreate, PatientUpdate
from beanie import PydanticObjectId

class PatientRepository(BaseRepository[PatientDemographics, PatientCreate, PatientUpdate]):
    
    async def get_by_medical_record(self, medical_record_number: str) -> Optional[PatientDemographics]:
        return await self.model.find_one(self.model.medical_record_number == medical_record_number)
        
    async def get_by_user_id(self, user_id: str) -> Optional[PatientDemographics]:
        return await self.model.find_one(
            self.model.user.id == PydanticObjectId(user_id),
            fetch_links=True
        )

    async def get_patients_by_priority(self, prioridad: str) -> List[PatientDemographics]:
        return await self.model.find(
            self.model.prioridad == prioridad,
            fetch_links=True
        ).to_list()

patient_repo = PatientRepository(PatientDemographics)