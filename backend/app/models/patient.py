from datetime import datetime
from beanie import Document, Link, Indexed
from pydantic import Field
from app.models.auth import User

class PatientDemographics(Document):
    user: Link[User]
    medical_record_number: Indexed(str, unique=True)
    full_name: str = Field(..., min_length=3, max_length=100)
    date_of_birth: datetime
    phone: str = Field(..., max_length=20)
    address: str = Field(..., max_length=150)
    
    class Settings:
        name = "patients"