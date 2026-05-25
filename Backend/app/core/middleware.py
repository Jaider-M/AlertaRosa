import logging
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings

# Configurar un logger local para auditoría
audit_logger = logging.getLogger("audit")
audit_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("audit_logs.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
audit_logger.addHandler(file_handler)

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Rutas que NO queremos auditar (Auth)
        excluded_paths = ["/api/auth/login", "/api/auth/register", "/api/auth/logout"]
        
        # Si es una ruta de auth, solo la dejamos pasar sin hacer nada más
        if any(path in request.url.path for path in excluded_paths):
            return await call_next(request)

        # 2. Lógica de auditoría para rutas protegidas
        start_time = time.time()
        
        try:
            response = await call_next(request)
        except Exception as e:
            # Si el middleware falla en el auth, el error se captura aquí
            raise e
            
        process_time = time.time() - start_time
        status_code = response.status_code
        
        if "/api/patients" in request.url.path or "/api/diagnostics" in request.url.path:
            audit_logger.info(
                f"AUDIT - Method: {request.method} - Path: {request.url.path} - Status: {status_code} - "
                f"Duration: {process_time:.4f}s"
            )
            
        return response