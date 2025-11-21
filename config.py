import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://admin:secret@postgres_service/link_db")

    class Config:
        case_sensitive = True

settings = Settings()