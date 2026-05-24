from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from beanie import PydanticObjectId

class ConsultationBase(BaseModel):
    patient_id: PydanticObjectId
    diagnostico_id: Optional[PydanticObjectId] = None
    notas: str

class ConsultationCreate(ConsultationBase):
    pass

class ConsultationUpdate(BaseModel):
    notas: Optional[str] = None
    diagnostico_id: Optional[PydanticObjectId] = None

class ConsultationResponse(ConsultationBase):
    id: PydanticObjectId
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True