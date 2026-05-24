import secrets
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AlertaRosa Backend API"
    API_V1_STR: str = "/api"
    
    # SECURITY
    SECRET_KEY: str  
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # DATABASE
    MONGODB_URI: str
    DATABASE_NAME: str = "alertarosa_db"
    
    # IA UPLOADS
    UPLOAD_DIR: str = "uploads/medical_images"

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),  
        env_file_encoding="utf-8",
        case_sensitive=True,  
        extra="ignore"        
    )

settings = Settings()
