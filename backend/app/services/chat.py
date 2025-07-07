from typing import List, Optional
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

    def _retrieve(self, query: str, k: int = 3, min_relevance: float = 0.85):
        """Recupera chunks relevantes basados en similitud de embeddings.
        
        Args:
            query: La consulta del usuario
            k: Número máximo de chunks a devolver
            min_relevance: Umbral mínimo de relevancia (0.0 = muy relevante, 1.0 = no relevante)
        """
        q_vec = self._emb.embed(query)
        scored = []
        for chunk in self._repo.get_all():
            if not chunk.texto or len(chunk.vector) != 1536:
                continue
            dist = self._emb.cosine_distance(q_vec, chunk.vector)
            # Solo incluir chunks que superen el umbral de relevancia
            if dist <= min_relevance:
                scored.append((dist, chunk))

        scored.sort(key=lambda x: x[0])
        return [c for _, c in scored[:k]]

    def answer(self, question: str, conversation_history: List[dict] = None, user_settings: Optional[dict] = None) -> ChatAnswer:
        # Usar configuración del usuario si está disponible
        top_k = user_settings.get("top_k", 3) if user_settings else 3
        min_relevance = user_settings.get("min_relevance", 0.85) if user_settings else 0.85
        system_prompt = user_settings.get("system_prompt", "Eres un asistente experto") if user_settings else "Eres un asistente experto"
        
        # Verificar si la pregunta está relacionada con imágenes o contenido visual
        visual_keywords = [
            'imagen', 'imagenes', 'foto', 'fotos', 'picture', 'pictures', 
            'visual', 'ver', 'mostrar', 'muestra', 'show', 'image', 'images',
            'video', 'videos', 'clip', 'clips', 'película', 'pelicula',
            'gráfico', 'grafico', 'diagram', 'diagrama', 'chart', 'gráfica', 'grafica'
        ]
        
        question_lower = question.lower()
        is_visual_query = any(keyword in question_lower for keyword in visual_keywords)
        
        # Si es una consulta visual, aumentar top_k para encontrar chunks con multimedia
        if is_visual_query:
            top_k = max(top_k, 6)  # Aumentar a mínimo 6 para tener más posibilidades
        
        chunks = self._retrieve(question, top_k, min_relevance)
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
            f"{system_prompt}\n\n"
            f"Contexto de la base de conocimiento:\n{context}\n\n"
            f"{conversation_context}"
            f"Pregunta actual del usuario: {question}\n\n"
            "Instrucciones:\n"
            "- Usa tanto el contexto de la base de conocimiento como el historial de conversación para dar una respuesta coherente\n"
            "- Si la pregunta se refiere a algo mencionado anteriormente en la conversación, úsalo para dar contexto\n"
            "- Si no sabes la respuesta basándote en el contexto proporcionado, indícalo claramente\n"
            "- Mantén la coherencia con las respuestas anteriores en la conversación"
        )
        
        # Pasar configuración del usuario al LLM si está disponible
        if user_settings:
            raw_answer = self._llm.ask(prompt, user_settings)
        else:
            raw_answer = self._llm.ask(prompt)

        # Incluir imágenes y videos de los chunks recuperados
        images: List[str] = []
        videos: List[str] = []
        
        # Estrategia de inclusión de multimedia:
        # 1. Si es consulta visual explícita: incluir todo el multimedia de los chunks
        # 2. Si no es consulta visual pero hay chunks con multimedia: incluir al menos una imagen/video representativo
        # 3. Si no hay texto relevante en chunks: incluir multimedia como alternativa
        
        # Filtrar solo chunks que realmente tienen multimedia (arrays no vacíos)
        chunks_with_media = [c for c in chunks if (c.imagenes and len(c.imagenes) > 0) or (c.videos and len(c.videos) > 0)]
        
        if is_visual_query:
            # Consulta visual explícita: incluir todo el multimedia de TODOS los chunks
            for c in chunks:
                if c.imagenes and len(c.imagenes) > 0:
                    images.extend(c.imagenes)
                if c.videos and len(c.videos) > 0:
                    videos.extend(c.videos)
        elif chunks_with_media:
            # No es consulta visual pero hay chunks con multimedia: incluir al menos uno
            # Priorizar chunks con más multimedia o más relevantes (primeros en la lista)
            for c in chunks_with_media[:2]:  # Máximo 2 chunks con multimedia
                if c.imagenes and len(c.imagenes) > 0:
                    images.extend(c.imagenes)
                if c.videos and len(c.videos) > 0:
                    videos.extend(c.videos)
        elif len(chunks) > 0 and all(not c.texto.strip() for c in chunks):
            # Fallback: si no hay texto, incluir multimedia disponible (solo si no está vacío)
            for c in chunks:
                if c.imagenes and len(c.imagenes) > 0:
                    images.extend(c.imagenes)
                if c.videos and len(c.videos) > 0:
                    videos.extend(c.videos)
        
        # Remover duplicados manteniendo el orden
        images = list(dict.fromkeys(images))
        videos = list(dict.fromkeys(videos))

        return ChatAnswer(answer=raw_answer, images=images, videos=videos)
