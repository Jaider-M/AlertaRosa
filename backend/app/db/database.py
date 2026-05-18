from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.models.auth import User
from app.models.patient import PatientDemographics
from app.models.clinical import DiagnosticRecord, Alert

async def init_db():
    # Create Motor client
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    
    # Init beanie with the Document class models
    await init_beanie(
        database=client[settings.DATABASE_NAME],
        document_models=[
            User,
            PatientDemographics,
            DiagnosticRecord,
            Alert
        ]
    )
