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
        start_time = time.time()
        
        # Extraer información relevante del request
        method = request.method
        url = request.url.path
        client_ip = request.client.host if request.client else "Unknown"
        
        # Procesar request
        response = await call_next(request)
        
        process_time = time.time() - start_time
        status_code = response.status_code
        
        # Solo registrar endpoints confidenciales: pacientes y diagnósticos
        if "/api/patients" in url or "/api/diagnostics" in url:
            # En un entorno real se extraería el usuario del request.state o token para saber quién accedió
            audit_logger.info(
                f"AUDIT - Method: {method} - Path: {url} - Status: {status_code} - "
                f"Client IP: {client_ip} - Duration: {process_time:.4f}s"
            )
            
        return response
