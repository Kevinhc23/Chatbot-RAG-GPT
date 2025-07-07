from typing import Iterable
from pymongo import MongoClient
from app.core.config import get_settings
from app.models.chunk import Chunk
from .base import IChunkRepository

class MongoChunkRepository(IChunkRepository):
    """Implementación que cumple Liskov: se puede sustituir por otra fuente (p.e. Postgres)."""
    def __init__(self) -> None:
        cfg = get_settings()
        self._collection = (
            MongoClient(cfg.mongo_uri)
            [cfg.mongo_db]
            [cfg.mongo_collection]
        )

    def get_all(self) -> Iterable[Chunk]:
        for doc in self._collection.find():
            yield Chunk(**doc)
