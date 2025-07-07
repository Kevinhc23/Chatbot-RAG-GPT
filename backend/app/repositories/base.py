from abc import ABC, abstractmethod
from typing import Iterable
from app.models import chunk

class IChunkRepository(ABC):
    """Interface Segregation: sólo expone lo que el servicio necesita."""
    @abstractmethod
    def get_all(self) -> Iterable[chunk]:
        raise NotImplementedError
