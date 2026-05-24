from datetime import date 
from typing import Optional, Annotated, Any
from pydantic import BaseModel, EmailStr, Field, ConfigDict, BeforeValidator
from app.models.auth import UserRole

# Validador para convertir automáticamente el ObjectId de MongoDB a string
PyObjectId = Annotated[str, BeforeValidator(str)]

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: UserRole
    
    # Datos opcionales para evitar errores de validación
    medical_record_number: Optional[str] = None
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None  
    nombre_completo: Optional[str] = None
    especialidad: Optional[str] = None
    registro_medico: Optional[str] = None

class UserUpdate(BaseModel):
    
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
    # Añadimos los campos que te faltaban
    username: Optional[str] = None
    nombre_completo: Optional[str] = None
    phone: Optional[str] = None
    especialidad: Optional[str] = None

class UserInDBBase(BaseModel):
    # El alias _id es necesario porque MongoDB guarda el identificador así
    id: PyObjectId = Field(alias="_id") 
    
    model_config = ConfigDict(
        from_attributes=True, 
        populate_by_name=True
    )
    
    username: str
    email: EmailStr
    role: UserRole
    is_active: bool

class UserResponse(UserInDBBase):
    pass

class SpecialistCreate(BaseModel):
    user_id: str
    nombre_completo: str = Field(..., min_length=3, max_length=100)
    especialidad: str = Field(..., min_length=3, max_length=50)
    registro_medico: str = Field(..., description="Número de tarjeta profesional médica")

class SpecialistResponse(BaseModel):
    id: PyObjectId = Field(alias="_id")
    user_id: str
    nombre_completo: str
    especialidad: str
    registro_medico: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
