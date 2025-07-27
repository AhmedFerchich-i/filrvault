# app/core/config.py
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "File Vault"
    UPLOAD_DIR: Path = Path("uploads")
    CHUNK_DIR: Path = Path("chunks")
    MAX_UPLOAD_SIZE_MB: int = 1024  # Optional: limit file size
    DB_HOST: str
    DB_USER:str
    DB_PASSWORD:str
    DB_NAME:str
    DB_PORT:int

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
