from typing import List, Optional, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field, model_validator
from beanie import PydanticObjectId

class AIResultSchema(BaseModel):
    """
    Sub-esquema para estructurar la salida de los datos del análisis de la IA.
    Desacopla el modelo de Beanie de la respuesta de la API.
    """
    ai_risk_score: float = Field(..., description="Score de riesgo devuelto por DenseNet121 (0.0 a 1.0)")
    birads_classification: str = Field(..., description="Clasificación BI-RADS mapeada según el score")

    processed_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), 
        description="Fecha exacta de la inferencia en formato UTC"
    )

class DiagnosticCreate(BaseModel):

    patient_id: str = Field(..., description="ID del paciente (Referencia de Beanie/MongoDB)")
    especialista_id: str = Field(..., description="ID del médico especialista asignado (doctor_id)")
    motivo_consulta: Optional[str] = Field(None, description="Motivo de la consulta o sintomatología inicial")
    status: Optional[str] = Field("En Revisión", description="Estado inicial del flujo clínico")

    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": "65f1a2b3c4d5e6f7a8b9c0d1",
                "especialista_id": "65f1a2b3c4d5e6f7a8b9c0d2",
                "motivo_consulta": "Paciente refiere masa palpable en cuadrante superior externo izquierdo.",
                "status": "En Revisión"
            }
        }

class DiagnosticUpdate(BaseModel):

    status: Optional[str] = Field(None, description="Estado actual del flujo clínico (ej: 'En Revisión', 'Completado')")
    notes: Optional[str] = Field(None, description="Notas o validaciones del especialista médico")
    ia_results: Optional[AIResultSchema] = Field(None, description="Resultados del análisis del motor de IA")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "Completado",
                "notes": "Se valida el hallazgo de la IA. Paciente requiere biopsia urgente."
            }
        }

class DiagnosticResponse(BaseModel):

    id: PydanticObjectId = Field(..., alias="_id")
    patient_id: str
    especialista_id: str
    status: str
    motivo_consulta: Optional[str] = None
    consultation_id: Optional[str] = None
    ia_results: Optional[AIResultSchema] = None 
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

    @model_validator(mode="before")
    @classmethod
    def map_diagnostic_fields(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            # Extraemos patient_id del link patient
            patient_val = getattr(data, "patient", None)
            patient_id = None
            if patient_val:
                if hasattr(patient_val, "id"):
                    patient_id = str(patient_val.id)
                elif isinstance(patient_val, dict) and "$id" in patient_val:
                    patient_id = str(patient_val["$id"])
                else:
                    patient_id = str(patient_val)

            # Mapeamos ai_results a un único ia_results
            ai_results = getattr(data, "ai_results", None)
            ia_results = None
            if ai_results and len(ai_results) > 0:
                last_ai = ai_results[-1]
                if hasattr(last_ai, "ai_risk_score"):
                    ia_results = {
                        "ai_risk_score": getattr(last_ai, "ai_risk_score"),
                        "birads_classification": getattr(last_ai, "birads_classification"),
                        "processed_at": getattr(last_ai, "processed_at")
                    }
                elif isinstance(last_ai, dict):
                    ia_results = last_ai

            db_id = getattr(data, "id", None) or getattr(data, "_id", None)
            
            return {
                "_id": db_id,
                "patient_id": patient_id,
                "especialista_id": getattr(data, "especialista_id", None),
                "status": getattr(data, "status", None),
                "consultation_id": getattr(data, "consultation_id", None),
                "motivo_consulta": getattr(data, "motivo_consulta", None),
                "ia_results": ia_results,
                "created_at": getattr(data, "created_at", None),
                "updated_at": getattr(data, "updated_at", None)
            }
        else:
            if "patient" in data and "patient_id" not in data:
                patient_val = data["patient"]
                if isinstance(patient_val, dict) and "$id" in patient_val:
                    data["patient_id"] = str(patient_val["$id"])
                elif hasattr(patient_val, "id"):
                    data["patient_id"] = str(patient_val.id)
                else:
                    data["patient_id"] = str(patient_val)
            if "ai_results" in data and "ia_results" not in data:
                ai_results = data["ai_results"]
                if ai_results and len(ai_results) > 0:
                    data["ia_results"] = ai_results[-1]
            if "_id" not in data and "id" in data:
                data["_id"] = data["id"]
        return data