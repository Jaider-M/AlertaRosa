<<<<<<< HEAD
from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr, Field
=======
from datetime import date 
from typing import Optional, Annotated, Any
from pydantic import BaseModel, EmailStr, Field, ConfigDict, BeforeValidator
>>>>>>> develop
from app.models.auth import UserRole

# Validador para convertir automáticamente el ObjectId de MongoDB a string
PyObjectId = Annotated[str, BeforeValidator(str)]

class UserCreate(BaseModel):
<<<<<<< HEAD
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario único para inicio de sesión")
    email: EmailStr = Field(..., description="Correo electrónico institucional o personal")
    password: str = Field(..., min_length=8, max_length=100, description="Contraseña segura (mínimo 8 caracteres)")
    role: UserRole = Field(..., description="Rol asignado en el sistema (ADMIN, SPECIALIST, PATIENT)")

    # Campos opcionales para creación automática de PatientDemographics
=======
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: UserRole
    
    # Datos opcionales para evitar errores de validación
>>>>>>> develop
    medical_record_number: Optional[str] = None
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    address: Optional[str] = None
<<<<<<< HEAD

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
=======
    
    nombre_completo: Optional[str] = None
    especialidad: Optional[str] = None
    registro_medico: Optional[str] = None
>>>>>>> develop

class UserUpdate(BaseModel):
    
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
<<<<<<< HEAD

    class Config:
        json_schema_extra = {
            "example": {
                "email": "camilo.nuevo_correo@alertarosa.com",
                "is_active": True
            }
        }

class UserInDBBase(BaseModel):
    id: str = Field(..., description="ID único del documento generado por MongoDB")
=======
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
    
>>>>>>> develop
    username: str
    email: EmailStr
    role: UserRole
    is_active: bool

<<<<<<< HEAD
    class Config:
        from_attributes = True 

class UserResponse(UserInDBBase):
    pass
=======
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
>>>>>>> develop
