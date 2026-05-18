from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import init_db
from app.core.middleware import AuditMiddleware
from app.routers import auth, patients, diagnostics

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Iniciando aplicación y conectando a base de datos...")
    await init_db()
    yield
    # Shutdown
    print("Cerrando aplicación...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción debe ser restringido a dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Audit Middleware (Security & Compliance)
app.add_middleware(AuditMiddleware)

# Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(patients.router, prefix=settings.API_V1_STR)
app.include_router(diagnostics.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API Backend de AlertaRosa"}
