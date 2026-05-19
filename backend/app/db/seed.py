import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from passlib.context import CryptContext

from app.core.config import settings
from app.models.auth import User
from app.models.patient import PatientDemographics
from app.models.clinical import DiagnosticRecord, Alert

# Contexto para encintar de forma segura la contraseña del Administrador inicial
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_database():
    print(" [AlertaRosa DB] Conectando a MongoDB para inicialización física...")
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.DATABASE_NAME]
    
    # 1. Inicializar Beanie para que cree las colecciones e índices automáticos
    await init_beanie(
        database=db,
        document_models=[
            User,
            PatientDemographics,
            DiagnosticRecord,
            Alert
        ]
    )
    print(" [AlertaRosa DB] Colecciones mapeadas e índices creados en MongoDB.")

    # 2. Verificar si ya existe un Administrador en la base de datos
    admin_exist = await User.find_one(User.email == "admin@alertarosa.com")
    
    if not admin_exist:
        print(" [AlertaRosa DB] No se detectó administrador. Creando cuenta raíz de auditoría...")
        
        # Ajusta los campos según los atributos reales que definiste en tu modelo User
        admin_user = User(
            username="admin_alerta_rosa",
            email="admin@alertarosa.com",
            hashed_password=pwd_context.hash("AdminAlertaRosa2026*"), # Contraseña segura inicial
            role="admin", # Rol requerido para la gestión y estadísticas del proyecto
            is_active=True
        )
        await admin_user.insert()
        print(" [AlertaRosa DB] Usuario administrador creado exitosamente.")
        print(" Credenciales: admin@alertarosa.com | Contraseña: AdminAlertaRosa2026*")
    else:
        print("ℹ [AlertaRosa DB] El usuario administrador ya existe. Omitiendo inserción.")

    print("[AlertaRosa DB] Base de datos completamente lista para producción local offline.")

if __name__ == "__main__":
    # Permite ejecutar este script directamente desde la terminal si lo deseas
    asyncio.run(seed_database())