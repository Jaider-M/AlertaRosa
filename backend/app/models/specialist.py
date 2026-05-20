from beanie import Document, Link, Indexed
from pydantic import Field
from app.models.auth import User

class SpecialistProfile(Document):
    user: Link[User]
    nombre_completo: str = Field(..., min_length=3, max_length=100)
    especialidad: str = Field(..., min_length=3, max_length=100)
    registro_medico: Indexed(str, unique=True)

    class Settings:
        name = "specialists"
