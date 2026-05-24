from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List
import shutil
import os
from app.models.auth import User, UserRole
from app.models.clinical import Consultation
from app.schemas.clinical import ConsultationCreate, ConsultationResponse
from app.repositories.clinical_repo import consultation_repo
from app.api.deps import get_current_active_user, require_role
from beanie import PydanticObjectId

router = APIRouter(prefix="/consultations", tags=["Citas Médicas"])

# --- Endpoints de Consulta ---

@router.get("/my-patients", response_model=List[dict])
async def get_my_patients(current_user: User = Depends(require_role([UserRole.SPECIALIST]))):
    """Obtiene una lista única de pacientes que tienen citas con el doctor logueado."""
    citas = await consultation_repo.get_by_specialist(str(current_user.id))
    
    unique_patients = {}
    for c in citas:
        if c.patient and str(c.patient.id) not in unique_patients:
            unique_patients[str(c.patient.id)] = {
                "id": str(c.patient.id),
                "name": c.patient.username
            }
    return list(unique_patients.values())

@router.post("/{consultation_id}/upload")
async def upload_diagnosis_file(
    consultation_id: PydanticObjectId,
    file: UploadFile = File(...),
    current_user: User = Depends(require_role([UserRole.SPECIALIST]))
):
    """Carga de archivos para procesamiento de IA."""
    # 1. Validar que la consulta existe y pertenece al doctor
    cita = await Consultation.get(consultation_id)
    if not cita or str(cita.doctor.id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="No tienes acceso a esta consulta")

    # 2. Guardar archivo en servidor (carpeta 'uploads')
    upload_dir = "app/storage"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = f"{upload_dir}/{consultation_id}_{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"message": "Archivo subido correctamente", "path": file_path}