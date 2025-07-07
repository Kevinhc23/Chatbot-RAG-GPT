"""
Pruebas para verificar el filtrado de imágenes en el ChatService
"""
import pytest
from app.services.chat import ChatService
from app.models.chunk import Chunk
from app.repositories.base import IChunkRepository
from app.services.embedding import EmbeddingService
from app.services.llm import LLMService
from typing import List

class MockChunkRepository(IChunkRepository):
    def __init__(self, chunks: List[Chunk]):
        self._chunks = chunks
    
    def get_all(self):
        return self._chunks

class MockEmbeddingService:
    def embed(self, text: str) -> List[float]:
        return [0.1] * 1536
    
    def cosine_distance(self, vec1: List[float], vec2: List[float]) -> float:
        return 0.7  # Dentro del umbral 0.85

class MockLLMService:
    def ask(self, prompt: str, user_settings=None) -> str:
        return "Respuesta de prueba"

def test_no_images_for_questions_without_media_chunks():
    """Chunks sin multimedia no devuelven imágenes"""
    chunks = [
        Chunk(
            id="1",
            texto="Texto sin multimedia",
            imagenes=[],
            videos=[],
            vector=[0.2] * 1536
        )
    ]
    
    repo = MockChunkRepository(chunks)
    embedding_service = MockEmbeddingService()
    llm_service = MockLLMService()
    chat_service = ChatService(repo, embedding_service, llm_service)
    
    result = chat_service.answer("¿Cuál es la capital de Francia?")
    
    assert len(result.images) == 0
    assert len(result.videos) == 0

def test_images_for_questions_with_media_chunks():
    """Chunks con multimedia devuelven imágenes automáticamente"""
    chunks = [
        Chunk(
            id="1",
            texto="Información turística",
            imagenes=["imagen1.jpg", "imagen2.jpg"],
            videos=["video1.mp4"],
            vector=[0.1] * 1536
        )
    ]
    
    repo = MockChunkRepository(chunks)
    embedding_service = MockEmbeddingService()
    llm_service = MockLLMService()
    chat_service = ChatService(repo, embedding_service, llm_service)
    
    result = chat_service.answer("¿Cuáles son los mejores lugares?")
    
    assert len(result.images) == 2
    assert len(result.videos) == 1

def test_images_for_visual_questions():
    """Consultas visuales explícitas devuelven todas las imágenes"""
    chunks = [
        Chunk(
            id="1",
            texto="Descripción",
            imagenes=["imagen1.jpg", "imagen2.jpg"],
            videos=["video1.mp4"],
            vector=[0.1] * 1536
        )
    ]
    
    repo = MockChunkRepository(chunks)
    embedding_service = MockEmbeddingService()
    llm_service = MockLLMService()
    chat_service = ChatService(repo, embedding_service, llm_service)
    
    result = chat_service.answer("¿Puedes mostrarme las imágenes?")
    
    assert len(result.images) == 2
    assert len(result.videos) == 1

if __name__ == "__main__":
    print("Ejecutando prueba 1: Chunks sin multimedia no devuelven imágenes")
    test_no_images_for_questions_without_media_chunks()
    print("✓ Prueba 1 pasó")
    
    print("\nEjecutando prueba 2: Chunks con multimedia devuelven imágenes automáticamente")
    test_images_for_questions_with_media_chunks()
    print("✓ Prueba 2 pasó")
    
    print("\nEjecutando prueba 3: Preguntas visuales explícitas devuelven imágenes")
    test_images_for_visual_questions()
    print("✓ Prueba 3 pasó")
    
    print("\nTodas las pruebas completadas exitosamente")
