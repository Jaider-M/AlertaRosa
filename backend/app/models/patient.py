from datetime import date
from typing import Optional
from beanie import Document, Link, Indexed
from pydantic import Field
from app.models.auth import User

class PatientDemographics(Document):
    user: Link[User]
    medical_record_number: Optional[str] = None 
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None 
    phone: Optional[str] = None
    address: Optional[str] = None
    prioridad: str = Field(default="Baja", description="Nivel de prioridad clínica: Baja, Media, Alta")

    class Settings:
        name = "patients"