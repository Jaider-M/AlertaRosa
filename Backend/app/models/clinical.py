<<<<<<< HEAD
=======
from beanie import Replace
>>>>>>> develop
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from beanie import Document, Link, before_event, Update, Save  # <-- Importamos hooks de Beanie
from pydantic import BaseModel, Field
from app.models.auth import User
from app.models.patient import PatientDemographics

class RiskLevel(str, Enum):
    LOW = "Bajo"
    MEDIUM = "Medio"
    HIGH = "Alto"

class AlertPriority(str, Enum):
    LOW = "Baja"
    MEDIUM = "Media"
    HIGH = "Alta"

class DiagnosticImage(BaseModel):
    filename: str
    content_type: str
    file_path: str
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AIResult(BaseModel):
    ai_risk_score: float = Field(default=0.0, ge=0.0, le=1.0)
    birads_classification: str
    processed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MedicalValidation(BaseModel):
    specialist_id: str
    notes: str
    clinical_stage: Optional[str] = None
    validated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DiagnosticRecord(Document):
    patient: Link[PatientDemographics]
<<<<<<< HEAD
    especialista_id: str = Field(..., description="ID del médico especialista asignado")
=======
    especialista: Link[User]
>>>>>>> develop
    consultation_id: Optional[str] = Field(None, description="Vínculo opcional a la consulta médica")
    images: List[DiagnosticImage] = Field(default=[])
    ai_results: List[AIResult] = Field(default=[])
    medical_validations: List[MedicalValidation] = Field(default=[])
    status: str = Field(default="Pendiente", description="Pendiente, En Revisión, Completado")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
<<<<<<< HEAD
=======

    @before_event([Replace, Save, Update])
    async def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc)
>>>>>>> develop

    class Settings:
        name = "diagnostics"

class Alert(Document):
    patient: Link[PatientDemographics] 
    sender: Link[User]
    priority: AlertPriority
    message: str = Field(..., min_length=5, max_length=500)
    sent_via: str
    read_by_patient: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "alerts"

class Consultation(Document):
    patient: Link[PatientDemographics]
<<<<<<< HEAD
    doctor: Link[User]
    fecha_hora: datetime
    motivo: str = Field(..., min_length=3, max_length=500)
    status: str = Field(default="Programada", description="Programada, Completada, Cancelada")
=======
    doctor: Link[User]  # Vinculado a la cuenta del especialista
    fecha_hora: datetime = Field(..., description="Fecha y hora exacta de la cita")
    motivo: str = Field(..., min_length=5, max_length=300, description="Motivo de la consulta")
    status: str = Field(default="Programada", description="Programada, Completada, Cancelada")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
>>>>>>> develop

    class Settings:
        name = "consultations"