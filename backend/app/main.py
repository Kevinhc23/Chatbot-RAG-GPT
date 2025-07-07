from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.chat import router as chat_router
from app.api.v1.chat_history import router as chat_history_router
from app.api.v1.history import router as history_router
from app.database import create_tables

def create_app() -> FastAPI:
    # Crear las tablas de la base de datos
    create_tables()
    
    app = FastAPI(
        title="Knowledge‑Base Chat API",
        version="0.1.0",
        description="Chatbot con contexto multimedia almacenado en MongoDB y embeddings OpenAI.",
    )
    
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:3001"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Incluir rutas
    app.include_router(chat_router)
    app.include_router(chat_history_router)
    app.include_router(history_router)
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)