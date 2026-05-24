from app.models.auth import SpecialistProfile
from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories.user_repo import user_repo
from app.api.deps import require_role
from app.models.auth import User, UserRole
from app.schemas.user import UserUpdate
from beanie import PydanticObjectId

router = APIRouter(prefix="/admin", tags=["Administrador"])

# --- 1. Listados ---

@router.get("/all-users")
async def get_all_users(current_user: User = Depends(require_role([UserRole.ADMIN]))):
    # Traemos todos excepto al admin que está logueado
    users = await User.find(User.id != current_user.id).to_list()
    return [
        {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active
        }
        for user in users
    ]

@router.get("/specialists")
async def list_specialists(current_user: User = Depends(require_role([UserRole.ADMIN]))):
    specialists = await User.find(User.role == "Especialista").to_list()
    return [{"id": str(u.id), "nombre": u.username, "correo": u.email, "is_active": u.is_active} for u in specialists]

@router.get("/patients")
async def get_patients(current_user: User = Depends(require_role([UserRole.ADMIN]))):
    return await user_repo.get_all_patients()

# --- 2. Gestión de Estados ---

@router.patch("/users/{id}/toggle-active")
async def toggle_user_active(id: PydanticObjectId, current_user: User = Depends(require_role([UserRole.ADMIN]))):
    user = await User.get(id)
    if not user: raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if id == current_user.id: raise HTTPException(status_code=400, detail="No puedes desactivar tu propia cuenta.")
        
    user.is_active = not user.is_active
    await user.save()
    return {"message": "Estado cambiado", "is_active": user.is_active}

# --- 3. Edición y Eliminación ---
@router.put("/users/{user_id}")
async def update_user(
    user_id: PydanticObjectId, 
    user_data: UserUpdate, 
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    update_data = user_data.model_dump(exclude_unset=True)
    
    # 1. Actualización segura del modelo base User
    user_fields = {"email", "role", "is_active", "password", "username"}
    for key, value in update_data.items():
        if key in user_fields:
            setattr(user, key, value)
    await user.save()

    # 2. Actualización condicional del perfil de especialista
    if user.role == UserRole.SPECIALIST:
        profile = await SpecialistProfile.find_one(SpecialistProfile.user.id == user.id)
        if profile:
            # Solo actualizamos si el campo existe Y tiene al menos 3 caracteres
            nombre = update_data.get("nombre_completo")
            if nombre and len(nombre) >= 3:
                profile.nombre_completo = nombre
                
            especialidad = update_data.get("especialidad")
            if especialidad and len(especialidad) >= 3:
                profile.especialidad = especialidad
            
            await profile.save()
            
    return {"message": "Usuario y perfil actualizados correctamente"}

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: PydanticObjectId, 
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    user = await User.get(user_id)
    if not user: raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    await user.delete()
    return {"message": "Usuario eliminado correctamente"}