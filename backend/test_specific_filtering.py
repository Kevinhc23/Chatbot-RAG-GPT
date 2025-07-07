"""
Prueba del filtrado inteligente de imágenes por relevancia específica
"""
from app.repositories.mongo_chunk import MongoChunkRepository
from app.services.embedding import EmbeddingService
from app.services.llm import LLMService
from app.services.chat import ChatService

def test_specific_image_filtering():
    """Probar que solo se devuelvan imágenes específicas para cada consulta"""
    
    repo = MongoChunkRepository()
    emb = EmbeddingService()
    llm = LLMService()
    chat = ChatService(repo, emb, llm)
    
    print("=== PRUEBA DE FILTRADO ESPECÍFICO DE IMÁGENES ===")
    
    # Obtener información de la base de datos
    chunks = list(repo.get_all())
    print(f"Total chunks en DB: {len(chunks)}")
    
    print("\nChunks con multimedia:")
    multimedia_chunks = []
    for i, chunk in enumerate(chunks):
        if (chunk.imagenes and len(chunk.imagenes) > 0) or (chunk.videos and len(chunk.videos) > 0):
            multimedia_chunks.append((i, chunk))
            print(f"Chunk {i+1}:")
            print(f"  Texto: {chunk.texto[:80]}...")
            print(f"  Imágenes: {chunk.imagenes}")
            print(f"  Videos: {chunk.videos}")
            print()
    
    # Prueba 1: Consulta específica sobre Cotopaxi
    print("=== PRUEBA 1: Consulta sobre Cotopaxi ===")
    result1 = chat.answer("¿Tienes un tour de Cotopaxi?")
    print(f"Pregunta: '¿Tienes un tour de Cotopaxi?'")
    print(f"Imágenes devueltas: {len(result1.images)}")
    print(f"Videos devueltos: {len(result1.videos)}")
    if result1.images:
        for img in result1.images:
            print(f"  - {img}")
    print()
    
    # Prueba 2: Consulta específica sobre Cajas
    print("=== PRUEBA 2: Consulta sobre El Cajas ===")
    result2 = chat.answer("¿Qué información tienes sobre el Parque Nacional El Cajas?")
    print(f"Pregunta: '¿Qué información tienes sobre el Parque Nacional El Cajas?'")
    print(f"Imágenes devueltas: {len(result2.images)}")
    print(f"Videos devueltos: {len(result2.videos)}")
    if result2.images:
        for img in result2.images:
            print(f"  - {img}")
    print()
    
    # Prueba 3: Consulta específica sobre Amazonía
    print("=== PRUEBA 3: Consulta sobre Amazonía ===")
    result3 = chat.answer("¿Tienes tours a la Amazonía o Cuyabeno?")
    print(f"Pregunta: '¿Tienes tours a la Amazonía o Cuyabeno?'")
    print(f"Imágenes devueltas: {len(result3.images)}")
    print(f"Videos devueltos: {len(result3.videos)}")
    if result3.images:
        for img in result3.images:
            print(f"  - {img}")
    print()
    
    # Prueba 4: Consulta general (no específica)
    print("=== PRUEBA 4: Consulta general ===")
    result4 = chat.answer("¿Cuáles son los mejores lugares para acampar?")
    print(f"Pregunta: '¿Cuáles son los mejores lugares para acampar?'")
    print(f"Imágenes devueltas: {len(result4.images)}")
    print(f"Videos devueltos: {len(result4.videos)}")
    if result4.images:
        for img in result4.images:
            print(f"  - {img}")
    print()
    
    # Prueba 5: Consulta visual explícita
    print("=== PRUEBA 5: Consulta visual explícita ===")
    result5 = chat.answer("Muéstrame todas las imágenes de los lugares")
    print(f"Pregunta: 'Muéstrame todas las imágenes de los lugares'")
    print(f"Imágenes devueltas: {len(result5.images)}")
    print(f"Videos devueltos: {len(result5.videos)}")
    if result5.images:
        for img in result5.images:
            print(f"  - {img}")
    print()
    
    print("=== ANÁLISIS DE RESULTADOS ===")
    print("El sistema debería:")
    print("1. Devolver imágenes específicas para consultas específicas (Cotopaxi, Cajas, etc.)")
    print("2. Ser selectivo en consultas generales (solo el chunk más relevante)")
    print("3. Devolver más imágenes solo en consultas visuales explícitas")

if __name__ == "__main__":
    test_specific_image_filtering()
