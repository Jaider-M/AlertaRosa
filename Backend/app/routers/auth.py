from app.core.security import verify_password
from datetime import timedelta, date
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel 
from app.core.config import settings 
from app.schemas.user import UserCreate, UserResponse
from app.repositories.user_repo import user_repo
from app.models.auth import UserRole
from app.models.patient import PatientDemographics
from app.models.specialist import SpecialistProfile

router = APIRouter(prefix="/auth", tags=["Autenticación"])

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate):
    user = await user_repo.get_by_username(user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado.",
        )
    
    user = await user_repo.get_by_email(user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado.",
        )

    user = await user_repo.create(user_in)
    
    if user.role == UserRole.PATIENT:
        patient_data = {
            "user": user,
            "medical_record_number": user_in.medical_record_number or f"HC-{user.username.upper()}-{str(user.id)[-6:]}",
            "full_name": user_in.full_name or user.username,
            "date_of_birth": user_in.date_of_birth or date(1900, 1, 1),
            "phone": user_in.phone or "000000000",
            "address": user_in.address or "Pendiente",
            "prioridad": "Baja"
        }
        patient_profile = PatientDemographics(**patient_data)
        await patient_profile.insert()
        
    elif user.role == UserRole.SPECIALIST:
        specialist_data = {
            "user": user,
            "nombre_completo": user_in.nombre_completo or f"Dr. {user.username.capitalize()}",
            "especialidad": user_in.especialidad or "Mastología",
            "registro_medico": user_in.registro_medico or f"RM-{user.username.upper()}-{str(user.id)[-6:]}"
        }
        specialist_profile = SpecialistProfile(**specialist_data)
        await specialist_profile.insert()
        
    return user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_repo.get_by_username(form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo"
        )
    

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id), 
        role=user.role, 
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }

