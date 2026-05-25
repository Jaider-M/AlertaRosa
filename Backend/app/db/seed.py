import asyncio
import certifi 
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from passlib.context import CryptContext

from app.core.config import settings
from app.models.auth import User, UserRole, SpecialistProfile  
from app.models.patient import Patient
from app.models.clinical import DiagnosticRecord, Alert, Consultation 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_database():
    print(" [AlertaRosa DB] Conectando a MongoDB para inicialización física...")
    
    client = AsyncIOMotorClient(settings.MONGODB_URI, tlsCAFile=certifi.where())
    db = client[settings.DATABASE_NAME]
    await init_beanie(
        database=db,
        document_models=[
            User,
            SpecialistProfile,
            PatientDemographics,
            DiagnosticRecord,
            Alert,
            Consultation
        ]
    )
    print(" [AlertaRosa DB] Colecciones mapeadas e índices creados en MongoDB.")
    # Verificamos si ya existe el Administrador raíz
    admin_exist = await User.find_one(User.email == "admin@alertarosa.com")
    
    if not admin_exist:
        print(" [AlertaRosa DB] No se detectó administrador. Creando cuenta raíz de auditoría...")
        
        admin_user = User(
            username="admin_alerta_rosa",
            email="admin@alertarosa.com",
            hashed_password=pwd_context.hash("AdminAlertaRosa2026*"), 
            role=UserRole.ADMIN, 
            is_active=True
        )
        await admin_user.insert()
        print(" [AlertaRosa DB] Usuario administrador creado exitosamente.")
        print("=========================================================================")
        print("  Credenciales: admin@alertarosa.com | Contraseña: AdminAlertaRosa2026*")
        print("=========================================================================")
    else:
        print("ℹ [AlertaRosa DB] El usuario administrador ya existe. Omitiendo inserción.")
    print(" [AlertaRosa DB] Base de datos completamente lista para producción o desarrollo local.")

if __name__ == "__main__":
    asyncio.run(seed_database())