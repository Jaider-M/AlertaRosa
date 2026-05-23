from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from beanie import PydanticObjectId

from app.api.deps import get_current_active_user, require_role
from app.models.auth import User, UserRole
from app.models.patient import PatientDemographics
from app.models.specialist import SpecialistProfile
from app.models.clinical import Consultation
from pydantic import BaseModel, Field

router = APIRouter(prefix="/consultations", tags=["Consultas"])

class ConsultationCreate(BaseModel):
    patient_id: str = Field(..., description="ID del paciente (PatientDemographics)")
    doctor_id: str = Field(..., description="ID del usuario doctor (User)")
    fecha_hora: datetime = Field(..., description="Fecha y hora de la cita")
    motivo: str = Field(..., min_length=3, max_length=500, description="Motivo de la consulta")

class ConsultationResponse(BaseModel):
    id: str
    patient_id: str
    patient_name: str
    doctor_id: str
    doctor_name: str
    fecha_hora: datetime
    motivo: str
    status: str

async def _map_consultation(c: Consultation) -> ConsultationResponse:
    patient_id = ""
    patient_name = "Paciente"
    if c.patient:
        patient_id = str(c.patient.id)
        patient_name = getattr(c.patient, "full_name", "Paciente")

    doctor_id = ""
    doctor_name = "Médico"
    if c.doctor:
        doctor_id = str(c.doctor.id)
        spec = await SpecialistProfile.find_one({"user.$id": c.doctor.id})
        if spec:
            doctor_name = spec.nombre_completo
        else:
            doctor_name = getattr(c.doctor, "username", "Médico")

    return ConsultationResponse(
        id=str(c.id),
        patient_id=patient_id,
        patient_name=patient_name,
        doctor_id=doctor_id,
        doctor_name=doctor_name,
        fecha_hora=c.fecha_hora,
        motivo=c.motivo,
        status=c.status
    )

@router.post("/", response_model=ConsultationResponse, status_code=status.HTTP_201_CREATED)
async def create_consultation(
    obj_in: ConsultationCreate,
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.SPECIALIST]))
):
    """
    Crea una nueva consulta programada.
    """
    try:
        pat_oid = PydanticObjectId(obj_in.patient_id)
        doc_oid = PydanticObjectId(obj_in.doctor_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="IDs de paciente o doctor inválidos."
        )

    patient = await PatientDemographics.get(pat_oid)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente no encontrado."
        )

    doctor = await User.get(doc_oid)
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Médico no encontrado."
        )

    consultation = Consultation(
        patient=patient,
        doctor=doctor,
        fecha_hora=obj_in.fecha_hora,
        motivo=obj_in.motivo,
        status="Programada"
    )
    await consultation.insert()
    return await _map_consultation(consultation)

@router.get("/doctor/{doctor_id}", response_model=List[ConsultationResponse])
async def get_doctor_consultations(
    doctor_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Retorna las citas programadas de un médico para pintar su calendario.
    """
    try:
        doc_oid = PydanticObjectId(doctor_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de médico inválido."
        )

    consultations = await Consultation.find(
        {"doctor.$id": doc_oid},
        Consultation.status == "Programada"
    ).find_all(fetch_links=True).to_list()

    return [await _map_consultation(c) for c in consultations]

@router.get("/patient/{patient_id}", response_model=List[ConsultationResponse])
async def get_patient_consultations(
    patient_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Retorna las citas pendientes del paciente.
    """
    try:
        pat_oid = PydanticObjectId(patient_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de paciente inválido."
        )

    consultations = await Consultation.find(
        {"patient.$id": pat_oid},
        Consultation.status == "Programada"
    ).find_all(fetch_links=True).to_list()

    return [await _map_consultation(c) for c in consultations]
