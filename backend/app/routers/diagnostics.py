import os
import shutil
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from app.api.deps import require_role 
from app.models.auth import User, UserRole
from app.models.clinical import DiagnosticImage, MedicalValidation, DiagnosticRecord
from app.repositories.diagnostic_repo import diagnostic_repo
from app.repositories.patient_repo import patient_repo
from app.services.ia_engine import ia_engine
from app.core.config import settings

router = APIRouter(prefix="/diagnostics", tags=["Diagnósticos"])

upload_dir = Path(settings.UPLOAD_DIR)
upload_dir.mkdir(parents=True, exist_ok=True)

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_diagnostic_image(
    patient_id: str = Form(...),
    file: UploadFile = File(...),
    consultation_id: Optional[str] = Form(None),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.SPECIALIST]))
):

    patient = await patient_repo.get(patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Paciente no encontrado"
        )
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    file_extension = file.filename.split(".")[-1] if "." in file.filename else "bin"
    safe_filename = f"{patient_id}_{timestamp}.{file_extension}"
    file_path = upload_dir / safe_filename
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    diag_image = DiagnosticImage(
        filename=file.filename,
        content_type=file.content_type,
        file_path=str(file_path)
    )
    
    try:
        ai_result = await ia_engine.analyze_image_local(str(file_path))
    except Exception as e:
        if file_path.exists():
            file_path.unlink() 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )
    patient_diagnostics = await diagnostic_repo.get_by_patient_id(str(patient.id))
    
    if patient_diagnostics:
        diagnostic = patient_diagnostics[-1]
        diagnostic.images.append(diag_image)
        diagnostic.ai_results.append(ai_result)
        diagnostic.status = "En Revisión"
        diagnostic.especialista_id = str(current_user.id)
        if consultation_id:
            diagnostic.consultation_id = consultation_id
        diagnostic.updated_at = datetime.now(timezone.utc)
        await diagnostic.save()
    else:
        diagnostic = DiagnosticRecord(
            patient=patient,
            especialista_id=str(current_user.id),
            consultation_id=consultation_id,
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Diagnóstico no encontrado"
        )
        
    validation = MedicalValidation(
        specialist_id=str(current_user.id),
        notes=notes,
        clinical_stage=clinical_stage
    )
    
    diagnostic.medical_validations.append(validation)
    diagnostic.status = "Completado"
    diagnostic.updated_at = datetime.now(timezone.utc)
    await diagnostic.save()
    
    return diagnostic