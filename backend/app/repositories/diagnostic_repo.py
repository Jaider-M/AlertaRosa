from typing import Optional, List
from beanie import PydanticObjectId
from app.repositories.base import BaseRepository
from app.models.clinical import DiagnosticRecord
from app.schemas.diagnostic import DiagnosticCreate, DiagnosticUpdate

class DiagnosticRepository(BaseRepository[DiagnosticRecord, DiagnosticCreate, DiagnosticUpdate]):
    async def get_by_patient_id(self, patient_id: str) -> List[DiagnosticRecord]:
        return await self.model.find(self.model.patient.id == PydanticObjectId(patient_id)).to_list()

diagnostic_repo = DiagnosticRepository(DiagnosticRecord)
