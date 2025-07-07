from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import SecretStr
from dotenv import load_dotenv
import os
from pathlib import Path

# Cargar variables de entorno desde el archivo .env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    OPENAI_API_KEY: SecretStr
    mongo_uri: str = "mongodb://localhost:27017/"
    mongo_db: str = "BaseConocimiento"
    mongo_collection: str = "Viaje"
    embedding_model_name: str = "text-embedding-3-small"
    llm_model_name: str = "gpt-4o-mini"
    llm_temperature: float = 0.0

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore"
    }

@lru_cache
def get_settings() -> Settings:
    return Settings()
