#!/usr/bin/env python3
"""
Script de prueba para verificar que el contexto de conversación funciona correctamente.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.chat import ChatService
from app.repositories.mongo_chunk import MongoChunkRepository
from app.services.embedding import EmbeddingService
from app.services.llm import LLMService

def test_conversation_context():
    """Prueba que el contexto de conversación se mantenga correctamente"""
    
    # Configurar servicios
    repo = MongoChunkRepository()
    emb = EmbeddingService()
    llm = LLMService()
    chat_service = ChatService(repo, emb, llm)
    
    print("=== Prueba de Contexto de Conversación ===\n")
    
    # Simular historial de conversación
    conversation_history = [
        {"role": "user", "content": "¿Cuál es tu nombre?"},
        {"role": "assistant", "content": "Soy un asistente de IA basado en conocimiento."},
        {"role": "user", "content": "¿Cuántos años tienes?"},
        {"role": "assistant", "content": "Como IA, no tengo edad física, pero puedo ayudarte con información."}
    ]
    
    # Hacer una pregunta que requiere contexto
    question = "¿Puedes recordar lo que me dijiste sobre tu identidad?"
    
    print(f"Historial de conversación:")
    for msg in conversation_history:
        print(f"  {msg['role']}: {msg['content']}")
    
    print(f"\nPregunta actual: {question}")
    print(f"\nRespuesta con contexto:")
    
    try:
        # Generar respuesta con contexto
        answer = chat_service.answer(question, conversation_history)
        print(f"  {answer.answer}")
        
        print(f"\nRespuesta sin contexto:")
        # Generar respuesta sin contexto para comparar
        answer_no_context = chat_service.answer(question)
        print(f"  {answer_no_context.answer}")
        
        print("\n=== Prueba completada ===")
        
    except Exception as e:
        print(f"Error durante la prueba: {e}")
        print("Asegúrate de que:")
        print("1. La clave API de OpenAI esté configurada correctamente")
        print("2. MongoDB esté ejecutándose y tenga datos")
        print("3. Todas las dependencias estén instaladas")

if __name__ == "__main__":
    test_conversation_context()
