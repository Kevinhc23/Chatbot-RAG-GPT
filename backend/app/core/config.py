from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import SecretStr
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    OPENAI_API_KEY: SecretStr = os.getenv("OPENAI_API_KEY")
    mongo_uri: str = "mongodb://localhost:27017/"
    mongo_db: str = "BaseConocimiento"
    mongo_collection: str = "viajes_chunks"
    embedding_model_name: str = "text-embedding-3-small"
    llm_model_name: str = "gpt-4o-mini"
    llm_temperature: float = 0.0

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()
