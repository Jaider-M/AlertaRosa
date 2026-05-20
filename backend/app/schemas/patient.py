from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field

class PatientCreate(BaseModel):
    user_id: str = Field(..., description="ID del usuario vinculado en la colección de autenticación")
    medical_record_number: str = Field(..., description="Número único de historia clínica del paciente")
    full_name: str = Field(..., min_length=3, max_length=100)
    date_of_birth: date = Field(..., description="Fecha de nacimiento pura (sin hora) YYYY-MM-DD")
    phone: str = Field(..., min_length=7, max_length=20)
    address: str = Field(..., min_length=5, max_length=150)

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "603d214f0f123456789abcdef",
                "medical_record_number": "HC-2026-9943",
                "full_name": "María Camila Restrepo",
                "date_of_birth": "1988-04-15",
                "phone": "+573157654321",
                "address": "Calle 5 # 34-12, Cali"
            }
        }

class PatientUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=3, max_length=100)
    phone: Optional[str] = Field(None, min_length=7, max_length=20)
    address: Optional[str] = Field(None, min_length=5, max_length=150)
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone": "+573001234567",
                "address": "Avenida Pasoancho # 80-25, Cali"
            }
        }