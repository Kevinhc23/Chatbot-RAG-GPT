from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import ChatSession, ChatMessage
from app.models.history import ChatSessionCreate, ChatMessageCreate
from datetime import datetime

class ChatHistoryService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_session(self, title: str) -> ChatSession:
        """Crear una nueva sesión de chat"""
        session = ChatSession(title=title)
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session
    
    def get_session(self, session_id: int) -> Optional[ChatSession]:
        """Obtener una sesión específica con todos sus mensajes"""
        return self.db.query(ChatSession).filter(ChatSession.id == session_id).first()
    
    def get_all_sessions(self) -> List[ChatSession]:
        """Obtener todas las sesiones ordenadas por fecha de actualización"""
        return self.db.query(ChatSession).order_by(ChatSession.updated_at.desc()).all()
    
    def add_message(self, session_id: int, role: str, content: str) -> ChatMessage:
        """Agregar un mensaje a una sesión"""
        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content
        )
        self.db.add(message)
        
        # Actualizar timestamp de la sesión
        session = self.db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if session:
            session.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(message)
        return message
    
    def delete_session(self, session_id: int) -> bool:
        """Eliminar una sesión y todos sus mensajes"""
        session = self.db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if session:
            self.db.delete(session)
            self.db.commit()
            return True
        return False
    
    def update_session_title(self, session_id: int, new_title: str) -> bool:
        """Actualizar el título de una sesión"""
        session = self.db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if session:
            session.title = new_title
            session.updated_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
    
    def get_session_messages(self, session_id: int) -> List[ChatMessage]:
        """Obtener todos los mensajes de una sesión"""
        return self.db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.created_at.asc()).all()
    
    def generate_session_title(self, first_message: str) -> str:
        """Generar un título para la sesión basado en el primer mensaje"""
        # Tomar las primeras 50 caracteres del mensaje
        title = first_message[:50]
        if len(first_message) > 50:
            title += "..."
        return title
