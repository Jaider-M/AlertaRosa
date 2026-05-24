from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from beanie import Document, Indexed, Link, PydanticObjectId
from pydantic import Field, EmailStr

class UserRole(str, Enum):
    ADMIN = "Administrador"
    SPECIALIST = "Especialista"
    PATIENT = "Paciente"

class User(Document):
    id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
    
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    hashed_password: str
    role: UserRole
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"

class SpecialistProfile(Document):
    id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
    user: Link[User]
    nombre_completo: str = Field(..., min_length=3, max_length=100)
    especialidad: str = Field(..., min_length=3, max_length=50)
    registro_medico: Indexed(str, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "specialists"