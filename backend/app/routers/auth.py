from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.config import settings
from app.security import create_access_token, verify_password  
from app.schemas.user import UserCreate, UserResponse
from app.repositories.user_repo import user_repo

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate):
    user = await user_repo.get_by_username(user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="El nombre de usuario ya está registrado.",
        )
    
    user = await user_repo.get_by_email(user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="El email ya está registrado.",
        )

    user = await user_repo.create(user_in)
    return user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_repo.get_by_username(form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id), expires_delta=access_token_expires
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