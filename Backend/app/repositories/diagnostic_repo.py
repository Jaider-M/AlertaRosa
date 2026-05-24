<<<<<<< HEAD
from typing import Optional, List
from fastapi import HTTPException, status
=======
from typing import List, Optional
>>>>>>> develop
from beanie import PydanticObjectId
from app.repositories.base import BaseRepository
from app.models.clinical import DiagnosticRecord
from app.schemas.diagnostic import DiagnosticCreate, DiagnosticUpdate

class DiagnosticRepository(BaseRepository[DiagnosticRecord, DiagnosticCreate, DiagnosticUpdate]):
    
    async def get_by_patient_id(self, patient_id: str) -> List[DiagnosticRecord]:
<<<<<<< HEAD
        try:
            valid_id = PydanticObjectId(patient_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El ID del paciente proporcionado no es válido"
            )

        return await self.model.find(self.model.patient.id == valid_id).to_list()
=======
        return await self.model.find(
            self.model.patient.id == PydanticObjectId(patient_id),
            fetch_links=True
        ).to_list()

    async def get_pending_by_specialist(self, especialista_id: str) -> List[DiagnosticRecord]:
        return await self.model.find(
            self.model.especialista_id == especialista_id,
            self.model.status != "Completado",
            fetch_links=True
        ).to_list()

    async def get_all_with_patient_data(self, skip: int = 0, limit: int = 100) -> List[DiagnosticRecord]:
        return await self.model.find_all(fetch_links=True).skip(skip).limit(limit).to_list()
>>>>>>> develop

diagnostic_repo = DiagnosticRepository(DiagnosticRecord)