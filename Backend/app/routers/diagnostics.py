import aiofiles
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from app.api.deps import require_role 
from app.models.auth import User, UserRole
from app.models.clinical import DiagnosticImage, MedicalValidation, DiagnosticRecord
from app.repositories.diagnostic_repo import diagnostic_repo
from app.repositories.patient_repo import patient_repo
from app.services.ia_engine import ia_engine
from app.core.config import settings
from datetime import datetime, timezone
from pathlib import Path

router = APIRouter(prefix="/diagnostics", tags=["Diagnósticos"])
@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_diagnostic_image(
    patient_id: str = Form(...),
    file: UploadFile = File(...),
    consultation_id: Optional[str] = Form(None),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.SPECIALIST]))
):
    patient = await patient_repo.get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    file_path = Path(settings.UPLOAD_DIR) / f"{patient_id}_{timestamp}_{file.filename}"
    
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
        
    diag_image = DiagnosticImage(
        filename=file.filename,
        content_type=file.content_type,
        file_path=str(file_path)
    )

    ai_result = await ia_engine.analyze_image_local(str(file_path))
    patient_diagnostics = await diagnostic_repo.get_by_patient_id(str(patient.id))
    
    if patient_diagnostics:
        diagnostic = patient_diagnostics[-1]
        diagnostic.images.append(diag_image)
        diagnostic.ai_results.append(ai_result)
        diagnostic.status = "En Revisión"
        await diagnostic.save()
    else:
        diagnostic = DiagnosticRecord(
            patient=patient,
            especialista=current_user,
            images=[diag_image],
            ai_results=[ai_result],
            status="En Revisión"
        )
        await diagnostic.insert()
    return diagnostic