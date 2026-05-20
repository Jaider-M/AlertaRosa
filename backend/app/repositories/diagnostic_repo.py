from typing import Optional, List
from fastapi import HTTPException, status
from beanie import PydanticObjectId
from app.repositories.base import BaseRepository
from app.models.clinical import DiagnosticRecord
from app.schemas.diagnostic import DiagnosticCreate, DiagnosticUpdate

class DiagnosticRepository(BaseRepository[DiagnosticRecord, DiagnosticCreate, DiagnosticUpdate]):
    async def get_by_patient_id(self, patient_id: str) -> List[DiagnosticRecord]:
        try:
            valid_id = PydanticObjectId(patient_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El ID del paciente proporcionado no es válido"
            )

        return await self.model.find(self.model.patient.id == valid_id).to_list()

diagnostic_repo = DiagnosticRepository(DiagnosticRecord)