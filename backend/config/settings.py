"""
Application Settings
"""
import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application Settings - Production Ready"""
    
    # App Info
    APP_NAME: str = "Enterprise Data Cleaner"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False  # Changed to False for production safety
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # Security - READ FROM ENVIRONMENT VARIABLES
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production-URGENT")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database - READ FROM ENVIRONMENT
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data_cleaning.db")
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    
    # Upload Settings
    UPLOAD_DIR: str = "./uploads"
    EXPORT_DIR: str = "./exports"
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB - يستحمل ملفات ضخمة
    ALLOWED_EXTENSIONS: str = ".xlsx,.xls,.csv,.txt"
    
    # Processing Settings - محسّن للآلاف من الصفوف
    CHUNK_SIZE: int = 5000  # معالجة 5000 صف دفعة واحدة
    MAX_WORKERS: int = 8  # 8 عمليات متوازية
    MAX_ROWS_LIMIT: int = 100000  # حد أقصى 100,000 صف
    
    # Celery Settings
    CELERY_BROKER_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # CORS - READ FROM ENVIRONMENT
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000")
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get list of CORS origins"""
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(',')]
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Get list of allowed extensions"""
        return self.ALLOWED_EXTENSIONS.split(',')
    
    class Config:
        case_sensitive = True
        env_file = ".env"


# Create settings instance
settings = Settings()

