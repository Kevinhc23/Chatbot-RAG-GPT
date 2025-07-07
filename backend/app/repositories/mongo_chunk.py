from typing import Iterable, Optional
from pymongo import MongoClient
from bson import ObjectId
from app.core.config import get_settings
from app.models.chunk import Chunk
from .base import IChunkRepository

class MongoChunkRepository(IChunkRepository):
    """Implementación que cumple Liskov: se puede sustituir por otra fuente (p.e. Postgres)."""
    def __init__(self, user_settings: Optional[dict] = None) -> None:
        cfg = get_settings()
        
        # Usar configuración del usuario si está disponible
        if user_settings and user_settings.get("mongodb_url"):
            mongo_uri = user_settings.get("mongodb_url")
            mongo_db = user_settings.get("mongodb_db_name", cfg.mongo_db)
            mongo_collection = user_settings.get("mongodb_collection_name", cfg.mongo_collection)
        else:
            mongo_uri = cfg.mongo_uri
            mongo_db = cfg.mongo_db
            mongo_collection = cfg.mongo_collection
        
        self._collection = (
            MongoClient(mongo_uri)
            [mongo_db]
            [mongo_collection]
        )
    
    def _convert_object_ids(self, doc: dict) -> dict:
        """Convierte ObjectId a string para compatibilidad con Pydantic."""
        if "_id" in doc and isinstance(doc["_id"], ObjectId):
            doc["_id"] = str(doc["_id"])
        return doc

    def get_all(self) -> Iterable[Chunk]:
        for doc in self._collection.find():
            # Convertir ObjectId a string para compatibilidad con Pydantic
            doc = self._convert_object_ids(doc)
            yield Chunk(**doc)
