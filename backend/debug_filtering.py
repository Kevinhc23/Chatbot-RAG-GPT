"""
Verificación del filtrado inteligente - versión simplificada
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.repositories.mongo_chunk import MongoChunkRepository
    from app.services.embedding import EmbeddingService
    from app.services.llm import LLMService
    from app.services.chat import ChatService
    
    print("=== INICIANDO PRUEBA DE FILTRADO INTELIGENTE ===")
    
    # Inicializar servicios
    repo = MongoChunkRepository()
    emb = EmbeddingService()
    llm = LLMService()
    chat = ChatService(repo, emb, llm)
    
    print("Servicios inicializados correctamente")
    
    # Verificar chunks con multimedia
    chunks = list(repo.get_all())
    multimedia_count = sum(1 for c in chunks if (c.imagenes and len(c.imagenes) > 0) or (c.videos and len(c.videos) > 0))
    print(f"Chunks totales: {len(chunks)}, Con multimedia: {multimedia_count}")
    
    # Prueba específica: Cotopaxi
    print("\\n--- Probando consulta específica sobre Cotopaxi ---")
    query1 = "tienes un tour de cotopaxi"
    result1 = chat.answer(query1)
    print(f"Consulta: '{query1}'")
    print(f"Resultado: {len(result1.images)} imágenes, {len(result1.videos)} videos")
    
    # Prueba general
    print("\\n--- Probando consulta general ---")
    query2 = "mejores lugares para acampar"
    result2 = chat.answer(query2)
    print(f"Consulta: '{query2}'")
    print(f"Resultado: {len(result2.images)} imágenes, {len(result2.videos)} videos")
    
    # Comparación
    print("\\n--- ANÁLISIS ---")
    if len(result1.images) != len(result2.images):
        print("✓ ÉXITO: El filtrado está funcionando - diferentes consultas devuelven diferentes cantidades de imágenes")
    else:
        print("⚠ El filtrado podría necesitar ajustes - ambas consultas devuelven la misma cantidad de imágenes")
    
    print("\\n=== PRUEBA COMPLETADA ===")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
