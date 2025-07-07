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

    def answer(self, question: str, conversation_history: List[dict] = None) -> ChatAnswer:
        chunks = self._retrieve(question)
        context = "\n\n".join(c.texto for c in chunks)

        # Construir el contexto de conversación
        conversation_context = ""
        if conversation_history:
            # Limitar el historial a los últimos 10 mensajes para no sobrecargar el prompt
            recent_history = conversation_history[-10:]
            conversation_context = "\n".join([
                f"{'Usuario' if msg['role'] == 'user' else 'Asistente'}: {msg['content']}"
                for msg in recent_history
            ])
            conversation_context = f"\n\nContexto de la conversación:\n{conversation_context}\n"

        prompt = (
            "Eres un asistente experto y sólo debes usar el siguiente contexto para contestar.\n\n"
            f"Contexto de la base de conocimiento:\n{context}\n\n"
            f"{conversation_context}"
            f"Pregunta actual del usuario: {question}\n\n"
            "Instrucciones:\n"
            "- Usa tanto el contexto de la base de conocimiento como el historial de conversación para dar una respuesta coherente\n"
            "- Si la pregunta se refiere a algo mencionado anteriormente en la conversación, úsalo para dar contexto\n"
            "- Si no sabes la respuesta basándote en el contexto proporcionado, indícalo claramente\n"
            "- Mantén la coherencia con las respuestas anteriores en la conversación"
        )
        raw_answer = self._llm.ask(prompt)

        images: List[str] = []
        videos: List[str] = []
        for c in chunks:
            images.extend(c.imagenes)
            videos.extend(c.videos)

        return ChatAnswer(answer=raw_answer, images=images, videos=videos)
