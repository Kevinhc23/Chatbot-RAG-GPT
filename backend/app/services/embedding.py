from typing import List
import numpy as np
from langchain_openai.embeddings import OpenAIEmbeddings
from app.core.config import get_settings

class EmbeddingService:
    """Responsabilidad única: convertir texto en vectores."""
    def __init__(self) -> None:
        cfg = get_settings()
        self._model = OpenAIEmbeddings(
            model=cfg.embedding_model_name,
            openai_api_key=cfg.OPENAI_API_KEY
        )

    def embed(self, text: str) -> List[float]:
        return self._model.embed_query(text)

    @staticmethod
    def cosine_distance(a: List[float], b: List[float]) -> float:
        a_np, b_np = np.array(a, dtype=np.float32), np.array(b, dtype=np.float32)
        sim = np.dot(a_np, b_np) / (np.linalg.norm(a_np) * np.linalg.norm(b_np))
        return 1 - float(sim)