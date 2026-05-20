from typing import Optional
from fastapi import HTTPException, status
from beanie import PydanticObjectId
from app.repositories.base import BaseRepository
from app.models.patient import PatientDemographics
from app.schemas.patient import PatientCreate, PatientUpdate

class PatientRepository(BaseRepository[PatientDemographics, PatientCreate, PatientUpdate]):
    async def get_by_medical_record(self, medical_record_number: str) -> Optional[PatientDemographics]:
        return await self.model.find_one(self.model.medical_record_number == medical_record_number)
        
    async def get_by_user_id(self, user_id: str) -> Optional[PatientDemographics]:
        try:
            valid_user_id = PydanticObjectId(user_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El ID de usuario proporcionado no es un identificador válido."
            )
        return await self.model.find_one({"user.$id": valid_user_id})
patient_repo = PatientRepository(PatientDemographics)