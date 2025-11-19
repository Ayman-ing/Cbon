import os
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    DB_USER: str = os.getenv("PGUSER", "cbonuser")
    DB_PASSWORD: str = os.getenv("PGPASSWORD", "cbonpass")
    DB_HOST: str = os.getenv("PGHOST", "localhost")
    DB_PORT: str = os.getenv("PGPORT", "5432")
    DB_NAME: str = os.getenv("PGDATABASE", "cbon_db")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

def get_settings() -> Settings:
    return Settings()
