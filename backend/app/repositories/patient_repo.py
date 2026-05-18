from typing import Optional
from app.repositories.base import BaseRepository
from app.models.patient import PatientDemographics
from app.schemas.patient import PatientCreate, PatientUpdate
from beanie import PydanticObjectId

class PatientRepository(BaseRepository[PatientDemographics, PatientCreate, PatientUpdate]):
    async def get_by_medical_record(self, medical_record_number: str) -> Optional[PatientDemographics]:
        return await self.model.find_one(self.model.medical_record_number == medical_record_number)
        
    async def get_by_user_id(self, user_id: str) -> Optional[PatientDemographics]:
        return await self.model.find_one(self.model.user.id == PydanticObjectId(user_id))

patient_repo = PatientRepository(PatientDemographics)
