from pydantic_settings import BaseSettings
from pathlib import Path
import os

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Mother's Day PDF Processor"
    DEBUG: bool = False
    
    STORAGE_DIR: Path = Path("/app/storage")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024
    
    TESSERACT_CMD: str = "/usr/bin/tesseract"
    OCR_LANG: str = "eng"
    
    MAX_WORKERS: int = 4
    PROCESS_TIMEOUT: int = 300
    
    ALLOW_ORIGINS: list = ["*"]
    
    class Config:
        case_sensitive = True

settings = Settings()

settings.STORAGE_DIR.mkdir(parents=True, exist_ok=True) 