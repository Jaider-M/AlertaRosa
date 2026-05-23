from typing import Any
from typing import List
from beanie import PydanticObjectId
from app.repositories.base import BaseRepository
from app.models.clinical import Consultation, Alert
from app.schemas.diagnostic import DiagnosticCreate, DiagnosticUpdate

class ConsultationRepository(BaseRepository[Consultation, Any, Any]):
    async def get_by_specialist(self, doctor_id: str) -> List[Consultation]:
        return await self.model.find(
            {"doctor.$id": PydanticObjectId(doctor_id)},
            fetch_links=True
        ).to_list()

    async def get_by_patient(self, patient_id: str) -> List[Consultation]:
        return await self.model.find(
            {"patient.$id": PydanticObjectId(patient_id)},
            fetch_links=True
        ).to_list()


class AlertRepository(BaseRepository[Alert, Any, Any]):
    async def get_active_alerts(self) -> List[Alert]:
        return await self.model.find(
            self.model.is_resolved == False,
            fetch_links=True
        ).sort(-self.model.created_at).to_list()

consultation_repo = ConsultationRepository(Consultation)
alert_repo = AlertRepository(Alert)