import pytest
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.main import app
from app.core.config import settings
from app.models.auth import User, UserRole
from app.models.patient import PatientDemographics
from app.models.specialist import SpecialistProfile
from app.models.clinical import DiagnosticRecord, Alert, Consultation
from app.core.security import get_password_hash

# Configurar DB de pruebas
test_settings = settings.copy()
test_settings.DATABASE_NAME = "alertarosa_test_db"

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def db_setup() -> AsyncGenerator:
    client = AsyncIOMotorClient(test_settings.MONGODB_URI)
    await init_beanie(
        database=client[test_settings.DATABASE_NAME],
        document_models=[User, SpecialistProfile, PatientDemographics, DiagnosticRecord, Alert, Consultation]
    )
    
    # Limpiar BD antes de tests
    await User.delete_all()
    await SpecialistProfile.delete_all()
    await PatientDemographics.delete_all()
    await DiagnosticRecord.delete_all()
    await Alert.delete_all()
    await Consultation.delete_all()

    # Crear usuario Admin por defecto para tests
    admin_user = User(
        username="admin_test",
        email="admin@test.com",
        hashed_password=get_password_hash("password123"),
        role=UserRole.ADMIN
    )
    await admin_user.insert()

    yield

    # Limpiar al finalizar
    await client.drop_database(test_settings.DATABASE_NAME)
    client.close()

@pytest.fixture(scope="module")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="module")
async def admin_token(client: AsyncClient) -> str:
    response = await client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "admin_test", "password": "password123"}
    )
    return response.json()["access_token"]
