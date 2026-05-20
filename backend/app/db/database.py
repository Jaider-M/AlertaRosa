import certifi
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.models.auth import User
from app.models.specialist import SpecialistProfile
from app.models.patient import PatientDemographics
from app.models.clinical import DiagnosticRecord, Alert

logger = logging.getLogger("uvicorn.error")

async def init_db():
    """
    Inicializa la conexión asíncrona con MongoDB Atlas
    y mapea las colecciones del sistema con Beanie ODM.
    """
    client = AsyncIOMotorClient(settings.MONGODB_URI, tlsCAFile=certifi.where())
    db = client.get_database(settings.DATABASE_NAME)
    
    try:
        await init_beanie(
            database=db,
            document_models=[
                User,
                SpecialistProfile,
                PatientDemographics,
                DiagnosticRecord,
                Alert
            ]
        )
        logger.info(" Base de datos conectada: Beanie inicializó los 5 modelos correctamente.")
    except Exception as e:
        logger.error(f" ERROR CRÍTICO al inicializar las colecciones de Beanie: {str(e)}")
        raise e