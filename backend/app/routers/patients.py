from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_current_active_user, require_role
from app.models.auth import User, UserRole
from app.schemas.patient import PatientCreate, PatientUpdate
from app.repositories.patient_repo import patient_repo

router = APIRouter(prefix="/patients", tags=["Pacientes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_patient(
    patient_in: PatientCreate,
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.SPECIALIST]))
):
    # Verificar duplicados en las historias clínicas
    existing_patient = await patient_repo.get_by_medical_record(patient_in.medical_record_number)
    if existing_patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Número de historia clínica ya existe"
        )
    
    patient = await patient_repo.create(patient_in)
    return patient

@router.get("/{medical_record_number}", status_code=status.HTTP_200_OK)
async def get_patient(
    medical_record_number: str,
    current_user: User = Depends(get_current_active_user)
):
    patient = await patient_repo.get_by_medical_record(medical_record_number)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Paciente no encontrado"
        )
    
    # Restricción estricta de privacidad: El paciente solo ve sus propios datos
    if current_user.role == UserRole.PATIENT:
        # Asegúrate de que el modelo Patient contenga la relación 'user' o cámbialo a 'user_id' si aplica
        patient_user_id = str(patient.user.id) if hasattr(patient.user, 'id') else str(patient.user)
        if patient_user_id != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No tienes permisos para ver la información de este paciente"
            )
        
    return patient

@router.put("/{medical_record_number}", status_code=status.HTTP_200_OK)
async def update_patient(
    medical_record_number: str,
    patient_in: PatientUpdate,
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.SPECIALIST]))
):
    patient = await patient_repo.get_by_medical_record(medical_record_number)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Paciente no encontrado"
        )
        
    updated_patient = await patient_repo.update(patient, patient_in)
    return updated_patient