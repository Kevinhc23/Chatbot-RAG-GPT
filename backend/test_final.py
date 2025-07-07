from app.repositories.mongo_chunk import MongoChunkRepository
from app.services.embedding import EmbeddingService
from app.services.llm import LLMService
from app.services.chat import ChatService

repo = MongoChunkRepository()
emb = EmbeddingService()
llm = LLMService()
chat = ChatService(repo, emb, llm)

print('=== PRUEBA 1: quienes somos? (sin multimedia esperado) ===')
result1 = chat.answer('quienes somos?')
print(f'Imágenes: {len(result1.images)}')
print(f'Videos: {len(result1.videos)}')

print('\n=== PRUEBA 2: mejores lugares para acampar? (con multimedia esperado) ===')
result2 = chat.answer('cuales son los mejores lugares para acampar?')
print(f'Imágenes: {len(result2.images)}')
print(f'Videos: {len(result2.videos)}')

print('\n=== PRUEBA 3: tienes imagenes? (consulta visual explícita) ===')
result3 = chat.answer('tienes imagenes?')
print(f'Imágenes: {len(result3.images)}')
print(f'Videos: {len(result3.videos)}')

print('\n=== RESUMEN ===')
print(f'Consulta normal (quienes somos): {len(result1.images)} imgs, {len(result1.videos)} vids')
print(f'Consulta con contexto multimedia (camping): {len(result2.images)} imgs, {len(result2.videos)} vids')
print(f'Consulta visual explícita (imagenes): {len(result3.images)} imgs, {len(result3.videos)} vids')
