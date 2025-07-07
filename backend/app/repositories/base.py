from abc import ABC, abstractmethod
from typing import Iterable
from app.models.chunk import Chunk

class IChunkRepository(ABC):
    """Interface Segregation: sólo expone lo que el servicio necesita."""
    @abstractmethod
    def get_all(self) -> Iterable[Chunk]:
        raise NotImplementedError
