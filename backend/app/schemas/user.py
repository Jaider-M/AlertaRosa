from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr, Field
from app.models.auth import UserRole

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario único para inicio de sesión")
    email: EmailStr = Field(..., description="Correo electrónico institucional o personal")
    password: str = Field(..., min_length=8, max_length=100, description="Contraseña segura (mínimo 8 caracteres)")
    role: UserRole = Field(..., description="Rol asignado en el sistema (ADMIN, SPECIALIST, PATIENT)")

    # Campos opcionales para creación automática de PatientDemographics
    medical_record_number: Optional[str] = None
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None

    # Campos opcionales para creación automática de SpecialistProfile
    nombre_completo: Optional[str] = None
    especialidad: Optional[str] = None
    registro_medico: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "username": "dr_restrepo",
                "email": "camilo.restrepo@alertarosa.com",
                "password": "PasswordSeguro2026*",
                "role": "SPECIALIST"
            }
        }

class UserUpdate(BaseModel):
    
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "email": "camilo.nuevo_correo@alertarosa.com",
                "is_active": True
            }
        }

class UserInDBBase(BaseModel):
    id: str = Field(..., description="ID único del documento generado por MongoDB")
    username: str
    email: EmailStr
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True 

class UserResponse(UserInDBBase):
    pass