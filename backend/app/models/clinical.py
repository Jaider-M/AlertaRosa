from datetime import datetime
from enum import Enum
from typing import List, Optional
from beanie import Document, Link
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
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

class AIResult(BaseModel):
    ai_risk_score: float = Field(default=0.0, ge=0.0, le=1.0)
    birads_classification: str
    processed_at: datetime = Field(default_factory=datetime.utcnow)

class MedicalValidation(BaseModel):
    specialist_id: str
    notes: str
    clinical_stage: Optional[str] = None
    validated_at: datetime = Field(default_factory=datetime.utcnow)

class DiagnosticRecord(Document):
    patient: Link[PatientDemographics]
    images: List[DiagnosticImage] = Field(default=[])
    ai_results: List[AIResult] = Field(default=[])
    medical_validations: List[MedicalValidation] = Field(default=[])
    status: str = Field(default="Pendiente", description="Pendiente, En Revisión, Completado")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "diagnostics"

class Alert(Document):
    patient: Link[User]
    sender: Link[User]
    priority: AlertPriority
    message: str = Field(..., min_length=5, max_length=500)
    sent_via: str
    read_by_patient: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "alerts"