from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.db.database import init_db
from app.core.middleware import AuditMiddleware
from app.routers import auth, patients, diagnostics, admin, consultations

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando aplicación y conectando a base de datos...")
    await init_db()
    yield
    print("Cerrando aplicación...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# 1. CORS Middleware (SIEMPRE PRIMERO)
# Permite que el navegador reciba los errores 422 con los headers correctos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Manejador de excepciones global para asegurar CORS en errores inesperados
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
        headers={"Access-Control-Allow-Origin": "*"}
    )

# 3. Audit Middleware (DESPUÉS DEL CORS)
app.add_middleware(AuditMiddleware)

# 4. Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(patients.router, prefix=settings.API_V1_STR)
app.include_router(diagnostics.router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=settings.API_V1_STR)
app.include_router(consultations.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API Backend de AlertaRosa"}