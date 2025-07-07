from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db, User
from app.services.history import ChatHistoryService
from app.core.deps import get_current_active_user
from app.models.history import (
    ChatSessionResponse, 
    ChatHistoryResponse, 
    ChatSessionCreate,
    ChatMessageResponse
)

router = APIRouter(prefix="/history", tags=["Chat History"])

@router.get("/sessions", response_model=List[ChatHistoryResponse])
async def get_chat_sessions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener todas las sesiones de chat con información resumida"""
    service = ChatHistoryService(db)
    sessions = service.get_user_sessions(current_user.id)
    
    result = []
    for session in sessions:
        # Contar mensajes y obtener preview del último mensaje
        message_count = len(session.messages)
        last_message_preview = None
        
        if session.messages:
            # Obtener el último mensaje del usuario (no del asistente)
            user_messages = [msg for msg in session.messages if msg.role == "user"]
            if user_messages:
                last_message_preview = user_messages[-1].content[:100]
                if len(user_messages[-1].content) > 100:
                    last_message_preview += "..."
        
        result.append(ChatHistoryResponse(
            id=session.id,
            title=session.title,
            created_at=session.created_at,
            updated_at=session.updated_at,
            message_count=message_count,
            last_message_preview=last_message_preview
        ))
    
    return result

@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session(
    session_id: int, 
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener una sesión específica con todos sus mensajes"""
    service = ChatHistoryService(db)
    session = service.get_user_session(current_user.id, session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    return session

@router.post("/sessions", response_model=ChatSessionResponse)
async def create_chat_session(
    session_data: ChatSessionCreate, 
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Crear una nueva sesión de chat"""
    service = ChatHistoryService(db)
    session = service.create_session(session_data.title, current_user.id)
    return session

@router.delete("/sessions/{session_id}")
async def delete_chat_session(
    session_id: int, 
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Eliminar una sesión de chat"""
    service = ChatHistoryService(db)
    success = service.delete_user_session(current_user.id, session_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    return {"message": "Sesión eliminada exitosamente"}

@router.put("/sessions/{session_id}/title")
async def update_session_title(
    session_id: int, 
    title_data: dict, 
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Actualizar el título de una sesión"""
    service = ChatHistoryService(db)
    success = service.update_user_session_title(current_user.id, session_id, title_data["title"])
    
    if not success:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    return {"message": "Título actualizado exitosamente"}
