from datetime import date 
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.auth import UserRole

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: UserRole
    
    # Datos para cuando el rol es PACIENTE:
    medical_record_number: Optional[str] = None
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    
    # Datos para cuando el rol es ESPECIALISTA:
    nombre_completo: Optional[str] = None
    especialidad: Optional[str] = None
    registro_medico: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

class UserInDBBase(BaseModel):
    id: str
    username: str
    email: EmailStr
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True

class UserResponse(UserInDBBase):
    pass

class SpecialistCreate(BaseModel):
    user_id: str
    nombre_completo: str = Field(..., min_length=3, max_length=100)
    especialidad: str = Field(..., min_length=3, max_length=50)
    registro_medico: str = Field(..., description="Número de tarjeta profesional médica")

class SpecialistResponse(BaseModel):
    id: str
    user_id: str
    nombre_completo: str
    especialidad: str
    registro_medico: str

    class Config:
        from_attributes = True