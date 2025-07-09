from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Medical Wallet API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # FHIR Server settings
    FHIR_SERVER_URL: str = "http://localhost:8080/fhir"
    FHIR_TIMEOUT: int = 30
    
    # Security settings
    SECRET_KEY: str = "-cG31ErB1Fk6gpQvWTDFustGYOq2PYn3mdqiUig1_Nw"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Backend DB
    DATABASE_URL: str = "postgresql://medwallet_app:medwallet_app@localhost:5432/medical_wallet_backend"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

