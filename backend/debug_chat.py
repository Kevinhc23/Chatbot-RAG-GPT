#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.repositories.mongo_chunk import MongoChunkRepository
from app.services.embedding import EmbeddingService
from app.core.config import get_settings

def debug_retrieval():
    print("=== DIAGNÓSTICO DEL SISTEMA DE CHAT ===\n")
    
    # Inicializar servicios
    try:
        repo = MongoChunkRepository()
        embedding_service = EmbeddingService()
        print("✓ Servicios inicializados correctamente\n")
    except Exception as e:
        print(f"✗ Error inicializando servicios: {e}")
        return
    
    # Verificar chunks en el repositorio
    print("1. Verificando chunks en el repositorio:")
    chunks = list(repo.get_all())
    print(f"   Total de chunks encontrados: {len(chunks)}")
    
    if not chunks:
        print("   ✗ No se encontraron chunks en la base de datos")
        return
    
    for i, chunk in enumerate(chunks[:3]):
        print(f"   Chunk {i+1}:")
        print(f"     ID: {chunk.id}")
        print(f"     Texto: {chunk.texto[:100]}..." if chunk.texto else "     Texto: [VACÍO]")
        print(f"     Vector length: {len(chunk.vector) if chunk.vector else 0}")
        print(f"     Imágenes: {len(chunk.imagenes)}")
        print(f"     Videos: {len(chunk.videos)}")
        print()
    
    # Probar embeddings
    print("2. Probando servicio de embeddings:")
    test_query = "quiénes somos"
    try:
        query_embedding = embedding_service.embed(test_query)
        print(f"   ✓ Embedding generado para '{test_query}'")
        print(f"   Dimensiones del embedding: {len(query_embedding)}")
    except Exception as e:
        print(f"   ✗ Error generando embedding: {e}")
        return
    
    # Probar similitudes
    print("\n3. Calculando similitudes:")
    scored = []
    for i, chunk in enumerate(chunks):
        if not chunk.texto or len(chunk.vector) != 1536:
            print(f"   Chunk {i+1}: SALTADO (texto vacío o vector inválido)")
            continue
        try:
            dist = embedding_service.cosine_distance(query_embedding, chunk.vector)
            scored.append((dist, chunk))
            print(f"   Chunk {i+1}: distancia = {dist:.4f}")
        except Exception as e:
            print(f"   Chunk {i+1}: ERROR calculando distancia - {e}")
    
    if not scored:
        print("   ✗ No se pudieron calcular similitudes")
        return
    
    # Mostrar resultados ordenados
    print("\n4. Resultados ordenados por relevancia:")
    scored.sort(key=lambda x: x[0])
    
    min_relevance_values = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    for threshold in min_relevance_values:
        relevant = [chunk for dist, chunk in scored if dist <= threshold]
        print(f"   Con umbral {threshold}: {len(relevant)} chunks relevantes")
        if relevant and threshold == 0.5:  # Mostrar detalles para umbral medio
            for dist, chunk in scored[:3]:
                if dist <= threshold:
                    print(f"     - Distancia {dist:.4f}: {chunk.texto[:50]}...")
    
    print(f"\n5. Conclusión:")
    if len(scored) == 0:
        print("   ✗ PROBLEMA: No hay chunks con vectores válidos")
    elif all(dist > 0.3 for dist, _ in scored):
        print("   ⚠ PROBLEMA: Todos los chunks tienen baja relevancia (>0.3)")
        print("   Sugerencia: Usar umbral más alto (ej: 0.7) o revisar embeddings")
    else:
        print("   ✓ Sistema funcionando correctamente")

if __name__ == "__main__":
    debug_retrieval()
