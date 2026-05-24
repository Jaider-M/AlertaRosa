<<<<<<< HEAD
from datetime import date 
=======
from datetime import date
from typing import Optional
>>>>>>> develop
from beanie import Document, Link, Indexed
from pydantic import Field
from app.models.auth import User

class PatientDemographics(Document):
    user: Link[User]
<<<<<<< HEAD
    medical_record_number: Indexed(str, unique=True)
    full_name: str = Field(..., min_length=3, max_length=100)
    date_of_birth: date 
    phone: str = Field(..., max_length=20)
    address: str = Field(..., max_length=150)
    prioridad: str = Field(default="Baja")
    
=======
    medical_record_number: Optional[str] = None 
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None 
    phone: Optional[str] = None
    address: Optional[str] = None
    prioridad: str = Field(default="Baja", description="Nivel de prioridad clínica: Baja, Media, Alta")

>>>>>>> develop
    class Settings:
        name = "patients"