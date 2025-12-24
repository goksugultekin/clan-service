from pydantic_settings import BaseSettings
from pydantic import PostgresDsn

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn | None = None

    class Config:
        env_file = ".env"

settings = Settings()
