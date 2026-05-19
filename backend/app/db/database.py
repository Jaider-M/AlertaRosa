from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.models.auth import User
from app.models.patient import PatientDemographics
from app.models.clinical import DiagnosticRecord, Alert

async def init_db():
    # Create Motor client
    client = AsyncIOMotorClient(settings.MONGODB_URI)

    db = client.get_database(settings.DATABASE_NAME)
    
    try:
        await init_beanie(
            database=db,
            document_models=[
                User,
                PatientDemographics,
                DiagnosticRecord,
                Alert
            ]
        )
    except Exception as e:
        print(f" ERROR CRÍTICO al inicializar las colecciones de Beanie: {str(e)}")
        raise e
