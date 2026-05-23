from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import require_role
from app.models.auth import User, UserRole
from app.models.specialist import SpecialistProfile
from beanie import PydanticObjectId

router = APIRouter(prefix="/admin", tags=["Administrador"])

@router.get("/specialists", status_code=status.HTTP_200_OK)
async def list_specialists(
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    """
    Listado masivo de especialistas unificando datos de User y SpecialistProfile
    mediante un .find().fetch() automático de Beanie.
    """
    specialists = await SpecialistProfile.find_all(fetch_links=True).to_list()
    
    results = []
    for spec in specialists:
        user = spec.user
        results.append({
            "id": str(spec.id),
            "nombre": spec.nombre_completo,
            "correo": user.email if user else None,
            "especialidad": spec.especialidad,
            "registro_medico": spec.registro_medico,
            "is_active": user.is_active if user else False
        })
    return results

@router.patch("/users/{id}/toggle-active", status_code=status.HTTP_200_OK)
async def toggle_user_active(
    id: PydanticObjectId,
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    """
    Activa o desactiva un usuario del sistema por su ID.
    """
    user = await User.get(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    user.is_active = not user.is_active
    await user.save()
    return {
        "message": f"Usuario {'activado' if user.is_active else 'desactivado'} exitosamente",
        "user_id": str(user.id),
        "is_active": user.is_active
    }
