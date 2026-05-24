from pydantic import BaseModel, Field, model_validator
from beanie import PydanticObjectId
from typing import Any

class SpecialistCreate(BaseModel):
    user_id: str = Field(..., description="ID del usuario (User) asociado en la colección de autenticación")
    nombre_completo: str = Field(..., min_length=3, max_length=100, description="Nombre completo del especialista")
    especialidad: str = Field(..., min_length=3, max_length=100, description="Especialidad médica del especialista")
    registro_medico: str = Field(..., min_length=3, max_length=50, description="Número de registro o licencia médica único")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "65f1a2b3c4d5e6f7a8b9c0d2",
                "nombre_completo": "Dr. Alejandro Restrepo",
                "especialidad": "Mastología",
                "registro_medico": "RM-994321-CO"
            }
        }

class SpecialistResponse(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    user_id: str = Field(..., description="ID del usuario asociado")
    nombre_completo: str = Field(..., min_length=3, max_length=100)
    especialidad: str = Field(..., min_length=3, max_length=100)
    registro_medico: str = Field(..., min_length=3, max_length=50)

    class Config:
        from_attributes = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "65f1a2b3c4d5e6f7a8b9c0d3",
                "user_id": "65f1a2b3c4d5e6f7a8b9c0d2",
                "nombre_completo": "Dr. Alejandro Restrepo",
                "especialidad": "Mastología",
                "registro_medico": "RM-994321-CO"
            }
        }

    @model_validator(mode="before")
    @classmethod
    def map_links(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            # Extrae la información desde el objeto Beanie/documento
            user_val = getattr(data, "user", None)
            user_id = None
            if user_val:
                if hasattr(user_val, "id"):
                    user_id = str(user_val.id)
                elif isinstance(user_val, dict) and "$id" in user_val:
                    user_id = str(user_val["$id"])
                else:
                    user_id = str(user_val)

            db_id = getattr(data, "id", None)
            return {
                "_id": db_id or getattr(data, "_id", None),
                "user_id": user_id,
                "nombre_completo": getattr(data, "nombre_completo", None),
                "especialidad": getattr(data, "especialidad", None),
                "registro_medico": getattr(data, "registro_medico", None)
            }
        else:
            if "user" in data and "user_id" not in data:
                user_val = data["user"]
                if isinstance(user_val, dict) and "$id" in user_val:
                    data["user_id"] = str(user_val["$id"])
                elif hasattr(user_val, "id"):
                    data["user_id"] = str(user_val.id)
                else:
                    data["user_id"] = str(user_val)
            if "_id" not in data and "id" in data:
                data["_id"] = data["id"]
        return data
