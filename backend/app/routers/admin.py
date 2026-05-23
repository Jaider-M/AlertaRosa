from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import require_role
from app.models.auth import User, UserRole
from beanie import PydanticObjectId

router = APIRouter(prefix="/admin", tags=["Administrador"])

@router.get("/specialists")
async def list_specialists(
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    specialists = await User.find(User.role == UserRole.SPECIALIST).to_list()
    
    return [
        {
            "id": str(user.id),
            "nombre": user.username, 
            "correo": user.email,
            "is_active": user.is_active
        }
        for user in specialists
    ]

@router.patch("/users/{id}/toggle-active")
async def toggle_user_active(
    id: PydanticObjectId,
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):

    if id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes desactivar tu propia cuenta de administrador."
        )

    user = await User.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    user.is_active = not user.is_active
    await user.save()
    
    return {
        "message": f"Usuario {'activado' if user.is_active else 'desactivado'}",
        "is_active": user.is_active
    }