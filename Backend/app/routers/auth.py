from app.models.auth import SpecialistProfile
from app.core.security import verify_password, create_access_token
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel 
from app.schemas.user import UserCreate, UserResponse
from app.repositories.user_repo import user_repo
from app.models.auth import UserRole
from app.models.patient import Patient

router = APIRouter(prefix="/auth", tags=["Autenticación"])

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate):
    # 1. Verificar existencia
    if await user_repo.get_by_username(user_in.username):
        raise HTTPException(status_code=400, detail="El usuario ya existe.")
    
    # 2. Crear usuario base mediante repositorio
    user = await user_repo.create(user_in)
    
    # 3. Crear perfil de forma segura
    try:
        if user.role == UserRole.PATIENT:
            patient = Patient(
                user=user, # Beanie ahora enlazará esto correctamente
                medical_record_number=user_in.medical_record_number or f"HC-{user.id}",
                full_name=user_in.full_name or user.username,
                date_of_birth=user_in.date_of_birth or date(1900, 1, 1),
                phone=user_in.phone or "0000000000",
                address=user_in.address or "Pendiente",
                prioridad="Baja"
            )
            await patient.insert()
            
        elif user.role == UserRole.SPECIALIST:
            specialist = SpecialistProfile(
                user=user,
                nombre_completo=user_in.nombre_completo or f"Dr. {user.username}",
                especialidad=user_in.especialidad or "Mastología",
                registro_medico=user_in.registro_medico or f"RM-{user.id}"
            )
            await specialist.insert()
            
    except Exception as e:
        # Rollback: si el perfil falla, borramos el usuario para no dejar registros huérfanos
        await user.delete()
        print(f"ERROR: Fallo al crear perfil, usuario eliminado: {e}")
        raise HTTPException(status_code=500, detail="Error al asignar perfil al usuario.")
        
    return user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_repo.get_by_username(form_data.username)
    
    # 1. Validar usuario y contraseña
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. Validar si está activo
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    
    # 3. Generar token
    access_token = create_access_token(subject=str(user.id), role=user.role)
    
    return {"access_token": access_token, "token_type": "bearer"}