from sqlalchemy.orm import Session
from typing import Optional
from fastapi import HTTPException, status
from app.database import User, UserSettings
from app.models.auth import UserCreate, UserUpdate, UserSettingsCreate, UserSettingsUpdate
from app.core.security import get_password_hash, verify_password
from datetime import datetime

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user: UserCreate) -> User:
        """Crear nuevo usuario"""
        print(f"Intentando crear usuario: {user.email}, {user.username}")
        
        # Verificar que el email no exista
        existing_email = self.get_user_by_email(user.email)
        if existing_email:
            print(f"Email ya existe: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Verificar que el username no exista
        existing_username = self.get_user_by_username(user.username)
        if existing_username:
            print(f"Username ya existe: {user.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya existe"
            )
        
        print("Creando usuario...")
        # Crear usuario
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            hashed_password=hashed_password
        )
        
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            print(f"Usuario creado con ID: {db_user.id}")
            
            # Crear configuración por defecto
            print("Creando configuración por defecto...")
            self.create_default_settings(db_user.id)
            print("Configuración por defecto creada")
            
            return db_user
        except Exception as e:
            print(f"Error en base de datos: {str(e)}")
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear usuario: {str(e)}"
            )
    
    def create_default_settings(self, user_id: int) -> UserSettings:
        """Crear configuración por defecto para usuario"""
        print(f"Creando configuración por defecto para usuario {user_id}")
        try:
            default_settings = UserSettings(
                user_id=user_id,
                # Configuración de OpenAI
                openai_api_key=None,
                
                # Configuración de MongoDB
                mongodb_url=None,
                mongodb_db_name=None,
                mongodb_collection_name=None,
                
                # Configuración del modelo
                default_model="gpt-3.5-turbo",
                max_tokens=1000,
                temperature=0.7,
                top_k=40,
                top_p=0.9,
                
                # Configuración de chunking
                chunk_size=1000,
                chunk_overlap=200,
                
                # Configuración de prompts
                system_prompt="Eres un asistente útil que responde preguntas basado en el contexto proporcionado.",
                
                # Configuración de UI
                theme="light",
                language="es"
            )
            
            self.db.add(default_settings)
            self.db.commit()
            self.db.refresh(default_settings)
            print(f"Configuración por defecto creada con ID: {default_settings.id}")
            
            return default_settings
        except Exception as e:
            print(f"Error creando configuración por defecto: {str(e)}")
            self.db.rollback()
            raise
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Obtener usuario por username"""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Obtener usuario por ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Autenticar usuario"""
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Actualizar usuario"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        update_data = user_update.dict(exclude_unset=True)
        
        # Si se actualiza la contraseña, hashearla
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        # Actualizar campos
        for field, value in update_data.items():
            setattr(user, field, value)
        
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def get_user_settings(self, user_id: int) -> Optional[UserSettings]:
        """Obtener configuración de usuario"""
        return self.db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    
    def update_user_settings(self, user_id: int, settings_update: UserSettingsUpdate) -> Optional[UserSettings]:
        """Actualizar configuración de usuario"""
        settings = self.get_user_settings(user_id)
        if not settings:
            return None
        
        update_data = settings_update.dict(exclude_unset=True)
        
        # Actualizar campos
        for field, value in update_data.items():
            setattr(settings, field, value)
        
        settings.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(settings)
        
        return settings
