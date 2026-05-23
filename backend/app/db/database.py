import certifi 
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings


from app.models.auth import User, SpecialistProfile
from app.models.patient import PatientDemographics
from app.models.clinical import DiagnosticRecord, Alert, Consultation

async def init_db():
    client = AsyncIOMotorClient(
        settings.MONGODB_URI,
        tlsCAFile=certifi.where() 
    )
    
    await init_beanie(
        database=client[settings.DATABASE_NAME],
        document_models=[
            User,
            SpecialistProfile,
            PatientDemographics,
            DiagnosticRecord,
            Alert,
            Consultation
        ]
    )