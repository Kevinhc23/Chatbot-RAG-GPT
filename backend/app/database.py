from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con configuraciones
    settings = relationship("UserSettings", back_populates="user", uselist=False)
    
    # Relación con sesiones de chat
    chat_sessions = relationship("ChatSession", back_populates="user")

class UserSettings(Base):
    __tablename__ = "user_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Configuración de APIs
    openai_api_key = Column(Text, nullable=True)
    mongodb_url = Column(String(500), nullable=True)
    mongodb_db_name = Column(String(100), nullable=True)
    mongodb_collection_name = Column(String(100), nullable=True)
    
    # Configuración de modelos
    default_model = Column(String(100), default="gpt-3.5-turbo")
    max_tokens = Column(Integer, default=1000)
    temperature = Column(String(10), default="0.7")
    top_k = Column(Integer, default=40)
    top_p = Column(String(10), default="0.9")
    
    # Configuración de chunking
    chunk_size = Column(Integer, default=1000)
    chunk_overlap = Column(Integer, default=200)
    
    # Configuración de prompts
    system_prompt = Column(Text, nullable=True)
    
    # Configuración de UI (campos adicionales para compatibilidad)
    theme = Column(String(20), default="light")
    language = Column(String(10), default="es")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con usuario
    user = relationship("User", back_populates="settings")

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Permitir null para compatibilidad
    title = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con mensajes
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")
    
    # Relación con usuario
    user = relationship("User", back_populates="chat_sessions")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String(50), nullable=False)  # 'user' o 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relación con sesión
    session = relationship("ChatSession", back_populates="messages")

# Configuración de la base de datos
DATABASE_URL = "sqlite:///./chat_history.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
