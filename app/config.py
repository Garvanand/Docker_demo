from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'garv-secret-key-2024')
    DEBUG: bool = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', 5000))

    class Config:
        env_file = ".env"

settings = Settings() 