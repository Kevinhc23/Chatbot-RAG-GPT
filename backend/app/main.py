from fastapi import FastAPI
from app.api.v1.chat import router as chat_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Knowledge‑Base Chat API",
        version="0.1.0",
        description="Chatbot con contexto multimedia almacenado en MongoDB y embeddings OpenAI.",
    )
    app.include_router(chat_router)
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)