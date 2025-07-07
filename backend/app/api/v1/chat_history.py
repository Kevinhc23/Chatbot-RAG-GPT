from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.chat import ChatRequest, ChatAnswer
from app.repositories.mongo_chunk import MongoChunkRepository
from app.services.embedding import EmbeddingService
from app.services.llm import LLMService
from app.services.chat import ChatService
from app.services.history import ChatHistoryService
from app.database import get_db
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/chat-history", tags=["Chat with History"])

class ChatWithHistoryRequest(BaseModel):
    question: str
    session_id: Optional[int] = None

class ChatWithHistoryResponse(ChatAnswer):
    session_id: int

def get_chat_service() -> ChatService:
    """Factory para inyectar dependencias – puedes cambiar repo o LLM sin tocar el handler."""
    repo = MongoChunkRepository()
    emb = EmbeddingService()
    llm = LLMService()
    return ChatService(repo, emb, llm)

@router.post("", response_model=ChatWithHistoryResponse, summary="Genera respuesta desde la KB con historial")
async def chat_with_history_endpoint(
    payload: ChatWithHistoryRequest,
    service: ChatService = Depends(get_chat_service),
    db: Session = Depends(get_db)
) -> ChatWithHistoryResponse:
    history_service = ChatHistoryService(db)
    
    # Si no hay session_id, crear una nueva sesión
    if payload.session_id is None:
        title = history_service.generate_session_title(payload.question)
        session = history_service.create_session(title)
        session_id = session.id
    else:
        session_id = payload.session_id
    
    # Obtener el historial de conversación para contexto
    conversation_history = []
    if payload.session_id is not None:
        messages = history_service.get_session_messages(session_id)
        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
    
    # Guardar el mensaje del usuario
    history_service.add_message(session_id, "user", payload.question)
    
    # Generar respuesta con contexto de conversación
    answer = service.answer(payload.question, conversation_history)
    
    # Guardar la respuesta del asistente
    history_service.add_message(session_id, "assistant", answer.answer)
    
    # Crear respuesta con session_id
    response = ChatWithHistoryResponse(
        answer=answer.answer,
        images=answer.images,
        videos=answer.videos,
        session_id=session_id
    )
    
    return response
