import io
import base64
from typing import Optional
import aiofiles
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from weasyprint import HTML
from app.api.deps import require_role 
from app.models.auth import User, UserRole
from app.models.clinical import DiagnosticImage, DiagnosticRecord
from app.repositories.diagnostic_repo import diagnostic_repo
from app.repositories.patient_repo import patient_repo
from app.services.ia_engine import ia_engine
from app.core.config import settings
from datetime import datetime, timezone
from pathlib import Path

router = APIRouter(prefix="/diagnostics", tags=["Diagnósticos"])

@router.post("/upload-standalone", status_code=status.HTTP_200_OK)
async def upload_standalone_diagnostic(
    file: UploadFile = File(...),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.SPECIALIST]))
):
    # 1. Guardar archivo temporalmente
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    file_path = Path(settings.UPLOAD_DIR) / f"temp_{timestamp}_{file.filename}"
    
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    
    # 2. Procesar con IA
    ai_result = await ia_engine.analyze_image_local(str(file_path))
    
    # 3. Convertir imagen a Base64 para el PDF
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    # 4. Preparar HTML profesional
    html_content = f"""
    <html>
        <style>
            body {{ font-family: sans-serif; padding: 40px; color: #333; }}
            .header {{ color: #e11d48; border-bottom: 3px solid #e11d48; padding-bottom: 10px; }}
            .img-preview {{ text-align: center; margin: 25px 0; }}
            .img-preview img {{ max-width: 400px; border: 2px solid #eee; border-radius: 8px; }}
            .data {{ background: #fdf2f8; padding: 20px; border-radius: 8px; }}
        </style>
        <body>
            <div class="header"><h1>Reporte Médico AlertaRosa</h1></div>
            
            <div class="img-preview">
                <img src="data:image/jpeg;base64,{encoded_image}" />
            </div>

            <div class="data">
                <p><strong>Fecha del Análisis:</strong> {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
                <p><strong>Clasificación IA:</strong> {ai_result.birads_classification}</p>
                <p><strong>Puntaje de Riesgo:</strong> {ai_result.ai_risk_score * 100:.2f}%</p>
            </div>
            
            <p style="margin-top: 30px;"><small><em>Nota: Este reporte es generado automáticamente por el sistema AlertaRosa y debe ser validado por un especialista médico.</em></small></p>
        </body>
    </html>
    """
    
    # 5. Generar PDF
    pdf = HTML(string=html_content).write_pdf()
    
    return StreamingResponse(
        io.BytesIO(pdf),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=reporte_{timestamp}.pdf"}
    )

# --- Endpoint ORIGINAL (Se mantiene igual) ---
@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_diagnostic_image(
    patient_id: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.SPECIALIST]))
):
    # ... (tu lógica original se mantiene sin cambios)
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