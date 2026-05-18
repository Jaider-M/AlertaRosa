import secrets
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AlertaRosa Backend API"
    API_V1_STR: str = "/api"
    
    # SECURITY
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # DATABASE
    MONGODB_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "alertarosa_db"
    
    # IA UPLOADS
    UPLOAD_DIR: str = "uploads/medical_images"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
