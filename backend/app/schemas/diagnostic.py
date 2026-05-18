from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.clinical import DiagnosticImage, AIResult, MedicalValidation

class DiagnosticCreate(BaseModel):
    patient_id: str

class DiagnosticUpdate(BaseModel):
    status: Optional[str] = None
    images: Optional[List[DiagnosticImage]] = None
    ai_results: Optional[List[AIResult]] = None
    medical_validations: Optional[List[MedicalValidation]] = None
