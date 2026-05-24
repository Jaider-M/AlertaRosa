from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.api.deps import get_current_active_user, require_role
from app.models.auth import User, UserRole
from app.schemas.patient import PatientCreate, PatientUpdate
from app.repositories.patient_repo import patient_repo
from app.models.clinical import DiagnosticRecord
from beanie import PydanticObjectId

router = APIRouter(prefix="/patients", tags=["Pacientes"])

@router.get("/doctor/my-patients")
async def get_doctor_patients(
    current_user: User = Depends(require_role([UserRole.SPECIALIST, UserRole.ADMIN]))
):
<<<<<<< HEAD
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
=======

    pipeline = [
        {"$match": {"especialista.$id": current_user.id}},  
        {"$group": {"_id": "$patient.$id"}},               
        {"$lookup": {                                       
            "from": "PatientDemographics", 
            "localField": "_id", 
            "foreignField": "_id", 
            "as": "patient_data"
        }},
        {"$unwind": "$patient_data"}
    ]
    
    results = await DiagnosticRecord.aggregate(pipeline).to_list()
    my_patients = [r["patient_data"] for r in results]
    
    priority_order = {"Alta": 0, "Media": 1, "Baja": 2}
    my_patients.sort(key=lambda p: priority_order.get(getattr(p, "prioridad", "Baja"), 2))
    
    return my_patients

@router.get("/me/history")
async def get_my_history(
    current_user: User = Depends(require_role([UserRole.PATIENT]))
>>>>>>> develop
):
    patient = await patient_repo.get_by_user_id(str(current_user.id))
    if not patient:
<<<<<<< HEAD
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Paciente no encontrado"
        )
        
    updated_patient = await patient_repo.update(patient, patient_in)
    return updated_patient

from app.models.clinical import DiagnosticRecord

@router.get("/doctor/my-patients", status_code=status.HTTP_200_OK)
async def get_doctor_patients(
    current_user: User = Depends(require_role([UserRole.SPECIALIST, UserRole.ADMIN]))
):
    """
    Retorna la lista de pacientes que tienen registros de diagnóstico con este médico,
    ordenados de forma descendente por prioridad (Alta -> Media -> Baja).
    """
    diagnostics = await DiagnosticRecord.find(
        DiagnosticRecord.especialista_id == str(current_user.id)
    ).find_all(fetch_links=True).to_list()
    
    seen_patient_ids = set()
    my_patients = []
    for diag in diagnostics:
        if diag.patient and diag.patient.id not in seen_patient_ids:
            seen_patient_ids.add(diag.patient.id)
            my_patients.append(diag.patient)
            
    priority_order = {"Alta": 0, "Media": 1, "Baja": 2}
    my_patients.sort(key=lambda p: priority_order.get(getattr(p, "prioridad", "Baja"), 2))
    
    return my_patients

@router.get("/me/history", status_code=status.HTTP_200_OK)
async def get_my_history(
    current_user: User = Depends(require_role([UserRole.PATIENT]))
):
    """
    Retorna cronológicamente todos los DiagnosticRecord del paciente autenticado.
    """
    patient = await patient_repo.get_by_user_id(str(current_user.id))
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de paciente no encontrado para el usuario actual."
        )
        
    records = await DiagnosticRecord.find(
        {"patient.$id": patient.id}
    ).to_list()
    
    records.sort(key=lambda r: r.created_at)
    
    return records
=======
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
        
    records = await DiagnosticRecord.find({"patient.$id": patient.id}, fetch_links=True).to_list()
    return sorted(records, key=lambda r: r.created_at, reverse=True) 
>>>>>>> develop
