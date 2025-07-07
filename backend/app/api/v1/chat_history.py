from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.chat import ChatRequest, ChatAnswer
from app.repositories.mongo_chunk import MongoChunkRepository
from app.services.embedding import EmbeddingService
from app.services.llm import LLMService
from app.services.chat import ChatService
from app.services.history import ChatHistoryService
from app.database import get_db, User
from app.core.deps import get_current_active_user
from app.services.user_settings import UserSettingsService
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/chat-history", tags=["Chat with History"])

class ChatWithHistoryRequest(BaseModel):
    question: str
    session_id: Optional[int] = None

class ChatWithHistoryResponse(ChatAnswer):
    session_id: int

def get_chat_service(user_settings: dict = None) -> ChatService:
    """Factory para inyectar dependencias – puedes cambiar repo o LLM sin tocar el handler."""
    repo = MongoChunkRepository(user_settings)
    emb = EmbeddingService()
    llm = LLMService()
    return ChatService(repo, emb, llm)

@router.post("", response_model=ChatWithHistoryResponse, summary="Genera respuesta desde la KB con historial")
async def chat_with_history_endpoint(
    payload: ChatWithHistoryRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> ChatWithHistoryResponse:
    history_service = ChatHistoryService(db)
    settings_service = UserSettingsService(db)
    
    # Obtener configuración del usuario
    user_settings = settings_service.get_user_settings_dict(current_user.id)
    
    # Crear servicio con configuración del usuario
    service = get_chat_service(user_settings)
    
    # Si no hay session_id, crear una nueva sesión asociada al usuario
    if payload.session_id is None:
        title = history_service.generate_session_title(payload.question)
        session = history_service.create_session(title, current_user.id)
        session_id = session.id
    else:
        session_id = payload.session_id
        # Verificar que la sesión pertenece al usuario
        session = history_service.get_session(session_id)
        if not session or session.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sesión no encontrada"
            )
    
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
    
    # Generar respuesta con contexto de conversación y configuración del usuario
    answer = service.answer(payload.question, conversation_history, user_settings)
    
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
