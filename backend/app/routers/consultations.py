from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.auth import User, UserRole
from app.models.clinical import Consultation
from app.schemas.clinical import ConsultationCreate, ConsultationUpdate, ConsultationResponse
from app.repositories.clinical_repo import consultation_repo
from app.api.deps import get_current_active_user, require_role
from beanie import PydanticObjectId

router = APIRouter(prefix="/consultations", tags=["Citas Médicas"])

async def _map_consultation(c: Consultation) -> ConsultationResponse:
    return ConsultationResponse(
        id=str(c.id),
        patient_id=str(c.patient.id),
        patient_name=c.patient.full_name if c.patient else "N/A",
        doctor_id=str(c.doctor.id),
        doctor_name=c.doctor.username, 
        fecha_hora=c.fecha_hora,
        motivo=c.motivo,
        status=c.status
    )

@router.post("/", response_model=ConsultationResponse, status_code=status.HTTP_201_CREATED)
async def create_consultation(
    obj_in: ConsultationCreate,
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.SPECIALIST]))
):
    new_consultation = await consultation_repo.create(obj_in)
    return await _map_consultation(new_consultation)

@router.get("/doctor/{doctor_id}", response_model=List[ConsultationResponse])
async def get_doctor_consultations(
    doctor_id: str,
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != UserRole.ADMIN and str(current_user.id) != doctor_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver estas citas")
        
    citas = await consultation_repo.get_by_specialist(doctor_id)
    return [await _map_consultation(c) for c in citas]

@router.get("/patient/{patient_id}", response_model=List[ConsultationResponse])
async def get_patient_consultations(
    patient_id: str,
    current_user: User = Depends(get_current_active_user)
):
    citas = await consultation_repo.get_by_patient(patient_id)
    return [await _map_consultation(c) for c in citas]