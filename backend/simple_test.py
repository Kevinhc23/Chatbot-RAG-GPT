from app.repositories.mongo_chunk import MongoChunkRepository
from app.services.embedding import EmbeddingService
from app.services.llm import LLMService
from app.services.chat import ChatService

repo = MongoChunkRepository()
emb = EmbeddingService()
llm = LLMService()
chat = ChatService(repo, emb, llm)

print("=== PRUEBA SIMPLE DE FILTRADO ===")

# Prueba con Cotopaxi
result = chat.answer("tienes un tour de cotopaxi?")
print(f"Pregunta Cotopaxi - Imágenes: {len(result.images)}, Videos: {len(result.videos)}")

# Prueba general
result2 = chat.answer("mejores lugares para acampar")
print(f"Pregunta general - Imágenes: {len(result2.images)}, Videos: {len(result2.videos)}")

print("Listo")
