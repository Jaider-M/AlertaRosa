import os
import shutil
from pathlib import Path
from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from app.api.deps import get_current_active_user, require_role
from app.models.auth import User, UserRole
from app.models.clinical import DiagnosticImage, MedicalValidation
from app.schemas.diagnostic import DiagnosticCreate
from app.repositories.diagnostic_repo import diagnostic_repo
from app.repositories.patient_repo import patient_repo
from app.services.ia_engine import ia_engine
from app.core.config import settings

router = APIRouter(prefix="/diagnostics", tags=["Diagnósticos"])

# Ensure upload directory exists
upload_dir = Path(settings.UPLOAD_DIR)
upload_dir.mkdir(parents=True, exist_ok=True)

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_diagnostic_image(
    patient_id: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.SPECIALIST]))
):
    # Verify patient exists
    patient = await patient_repo.get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    # Guardar archivo localmente
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = file.filename.split(".")[-1]
    safe_filename = f"{patient_id}_{timestamp}.{file_extension}"
    file_path = upload_dir / safe_filename
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Crear registro de imagen
    diag_image = DiagnosticImage(
        filename=file.filename,
        content_type=file.content_type,
        file_path=str(file_path)
    )
    
    # Procesar imagen con MONAI / PyTorch en local
    try:
        ai_result = await ia_engine.analyze_image_local(str(file_path))
    except Exception as e:
        # En caso de fallo en el motor IA, loguear y retornar error.
        raise HTTPException(status_code=500, detail=f"Error en IA Engine: {str(e)}")

    # Crear o actualizar el DiagnosticRecord unificado para el paciente
    # Por simplicidad, obtenemos el último diagnóstico del paciente o creamos uno nuevo.
    patient_diagnostics = await diagnostic_repo.get_by_patient_id(str(patient.id))
    if patient_diagnostics:
        diagnostic = patient_diagnostics[-1]
        diagnostic.images.append(diag_image)
        diagnostic.ai_results.append(ai_result)
        diagnostic.status = "En Revisión"
        diagnostic.updated_at = datetime.utcnow()
        await diagnostic.save()
    else:
        # Crear nuevo registro
        from app.models.clinical import DiagnosticRecord
        diagnostic = DiagnosticRecord(
            patient=patient,
            images=[diag_image],
            ai_results=[ai_result],
            status="En Revisión"
        )
        await diagnostic.insert()
        
    return diagnostic

@router.put("/{diagnostic_id}/validate")
async def validate_diagnostic(
    diagnostic_id: str,
    notes: str = Form(...),
    clinical_stage: str = Form(None),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.SPECIALIST]))
):
    diagnostic = await diagnostic_repo.get(diagnostic_id)
    if not diagnostic:
        raise HTTPException(status_code=404, detail="Diagnóstico no encontrado")
        
    validation = MedicalValidation(
        specialist_id=str(current_user.id),
        notes=notes,
        clinical_stage=clinical_stage
    )
    
    diagnostic.medical_validations.append(validation)
    diagnostic.status = "Completado"
    diagnostic.updated_at = datetime.utcnow()
    await diagnostic.save()
    
    return diagnostic
