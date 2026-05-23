from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from beanie import Document, Indexed, Link
from pydantic import Field, EmailStr

class UserRole(str, Enum):
    ADMIN = "Administrador"
    SPECIALIST = "Especialista"
    PATIENT = "Paciente"

class User(Document):
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    hashed_password: str
    role: UserRole
    is_active: bool = Field(default=True)
    # Corrección de la estampa de tiempo al estándar moderno de 2026
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"

class SpecialistProfile(Document):

    user: Link[User]  # Relación 1:1 con la cuenta de usuario nativa
    nombre_completo: str = Field(..., min_length=3, max_length=100)
    especialidad: str = Field(..., min_length=3, max_length=50)
    registro_medico: Indexed(str, unique=True)  # Tarjeta profesional única
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "specialists"  # Nombre exacto de la colección en MongoDB