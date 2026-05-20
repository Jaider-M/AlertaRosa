from datetime import datetime, timezone # <-- Añadimos timezone
from enum import Enum
from beanie import Document, Indexed
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

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"