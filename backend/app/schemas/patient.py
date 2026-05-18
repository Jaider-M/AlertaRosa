from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class PatientCreate(BaseModel):
    user_id: str
    medical_record_number: str
    full_name: str = Field(..., min_length=3, max_length=100)
    date_of_birth: datetime
    phone: str = Field(..., max_length=20)
    address: str = Field(..., max_length=150)

class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
