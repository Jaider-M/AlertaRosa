from fastapi import APIRouter, Depends, HTTPException, status
# Ya no importamos List de typing
from app.api.deps import require_role
from app.models.auth import User, UserRole
from app.schemas.patient import PatientResponse
from app.models.patient import Patient 

router = APIRouter(prefix="/patients", tags=["Pacientes"])

@router.get("/doctor/my-patients", response_model=list[PatientResponse])
async def get_doctor_patients(
    current_user: User = Depends(require_role([UserRole.SPECIALIST, UserRole.ADMIN]))
):
    # Agrega fetch_links=True aquí
    patients = await Patient.find_all(fetch_links=True).to_list()
    
    response_list = []
    for p in patients:
        # Ahora p.user es el objeto completo, no solo un Link
        response_list.append(PatientResponse(
            id=str(p.id),
            user_id=str(p.user.id) if p.user else "N/A", 
            medical_record_number=p.medical_record_number or "",
            full_name=p.full_name or "Sin nombre",
            date_of_birth=p.date_of_birth,
            phone=p.phone or "",
            address=p.address or "",
            prioridad=p.prioridad
        ))
    return response_list