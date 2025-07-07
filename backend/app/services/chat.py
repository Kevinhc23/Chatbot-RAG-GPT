from typing import List
from app.models.chat import ChatAnswer
from app.repositories.base import IChunkRepository
from app.services.embedding import EmbeddingService
from app.services.llm import LLMService
from app.core.config import get_settings

class ChatService:
    """Alta‑nivel orquestador → cumple Dependency‑Inversion: depende de abstracciones."""
    def __init__(
        self,
        repo: IChunkRepository,
        embeddings: EmbeddingService,
        llm: LLMService,
    ) -> None:
        self._repo = repo
        self._emb = embeddings
        self._llm = llm
        self._cfg = get_settings()

    def _retrieve(self, query: str, k: int = 3):
        q_vec = self._emb.embed(query)
        scored = []
        for chunk in self._repo.get_all():
            if not chunk.texto or len(chunk.vector) != 1536:
                continue
            dist = self._emb.cosine_distance(q_vec, chunk.vector)
            scored.append((dist, chunk))

        scored.sort(key=lambda x: x[0])
        return [c for _, c in scored[:k]]

    def answer(self, question: str) -> ChatAnswer:
        chunks = self._retrieve(question)
        context = "\n\n".join(c.texto for c in chunks)

        prompt = (
            "Eres un asistente experto y sólo debes usar el siguiente contexto para contestar.\n\n"
            f"{context}\n\n"
            f"Pregunta del usuario: {question}\n\n"
            "Si no sabes la respuesta, indícalo claramente."
        )
        raw_answer = self._llm.ask(prompt)

        images: List[str] = []
        videos: List[str] = []
        for c in chunks:
            images.extend(c.imagenes)
            videos.extend(c.videos)

        return ChatAnswer(answer=raw_answer, images=images, videos=videos)
