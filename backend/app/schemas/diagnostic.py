from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.clinical import DiagnosticImage, AIResult, MedicalValidation

class DiagnosticCreate(BaseModel):
    patient_id: str = Field(..., description="ID del documento PatientDemographics")
    especialista_id: str = Field(..., description="ID del usuario Especialista asignado a la lectura")
    consultation_id: Optional[str] = Field(None, description="ID opcional de la cita asociada")

class DiagnosticUpdate(BaseModel):
    status: Optional[str] = Field(None, description="Pendiente, En Revisión, Completado")
    images: Optional[List[DiagnosticImage]] = None
    ai_results: Optional[List[AIResult]] = None
    medical_validations: Optional[List[MedicalValidation]] = None

class DiagnosticResponse(BaseModel):
    """
    Esquema de salida plano y seguro para los tableros de Vue.js.
    Soporta la Tarea 4 (Historial del Paciente y Alertas del Doctor).
    """
    id: str
    patient_id: str
    especialista_id: str
    consultation_id: Optional[str] = None
    status: str
    images: List[DiagnosticImage] = []
    ai_results: List[AIResult] = []
    medical_validations: List[MedicalValidation] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 