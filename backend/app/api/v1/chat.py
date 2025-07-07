from fastapi import APIRouter, Depends
from app.models.chat import ChatRequest, ChatAnswer
from app.repositories.mongo_chunk import MongoChunkRepository
from app.services.embedding import EmbeddingService
from app.services.llm import LLMService
from app.services.chat import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])

def get_chat_service() -> ChatService:
    """Factory para inyectar dependencias – puedes cambiar repo o LLM sin tocar el handler."""
    repo = MongoChunkRepository()
    emb = EmbeddingService()
    llm = LLMService()
    return ChatService(repo, emb, llm)

@router.post("", response_model=ChatAnswer, summary="Genera respuesta desde la KB")
async def chat_endpoint(
    payload: ChatRequest,
    service: ChatService = Depends(get_chat_service),
) -> ChatAnswer:
    return service.answer(payload.question)
