from typing import List
from pydantic import BaseModel, Field

class Chunk(BaseModel):
    id: str | None = Field(alias="_id", default=None)
    texto: str
    imagenes: List[str] = []
    videos: List[str] = []
    vector: List[float] = Field(default_factory=list, min_length=1536, max_length=1536)
