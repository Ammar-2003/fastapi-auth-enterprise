# app/core/config.py 

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load from .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

class Settings(BaseSettings):
    SECRET_KEY: str
    ADMIN_PATH: str = "/admin"
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    PROJECT_NAME: str = "My FastAPI App"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
