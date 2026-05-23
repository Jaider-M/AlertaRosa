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
):
    patient = await patient_repo.get_by_user_id(str(current_user.id))
    if not patient:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
        
    records = await DiagnosticRecord.find({"patient.$id": patient.id}, fetch_links=True).to_list()
    return sorted(records, key=lambda r: r.created_at, reverse=True) 