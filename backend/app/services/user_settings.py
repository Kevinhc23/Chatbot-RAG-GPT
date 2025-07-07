from sqlalchemy.orm import Session
from typing import Optional
from app.database import UserSettings

class UserSettingsService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_settings(self, user_id: int) -> Optional[UserSettings]:
        """Obtener configuración del usuario"""
        return self.db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    
    def create_or_update_user_settings(self, user_id: int, settings_data: dict) -> UserSettings:
        """Crear o actualizar configuración del usuario"""
        # Buscar configuración existente
        existing_settings = self.get_user_settings(user_id)
        
        if existing_settings:
            # Actualizar configuración existente
            for key, value in settings_data.items():
                if hasattr(existing_settings, key):
                    setattr(existing_settings, key, value)
            self.db.commit()
            self.db.refresh(existing_settings)
            return existing_settings
        else:
            # Crear nueva configuración
            new_settings = UserSettings(user_id=user_id, **settings_data)
            self.db.add(new_settings)
            self.db.commit()
            self.db.refresh(new_settings)
            return new_settings
    
    def get_user_settings_dict(self, user_id: int) -> dict:
        """Obtener configuración del usuario como diccionario"""
        settings = self.get_user_settings(user_id)
        if settings:
            return {
                "openai_api_key": settings.openai_api_key,
                "mongodb_url": settings.mongodb_url,
                "mongodb_db_name": settings.mongodb_db_name,
                "mongodb_collection_name": settings.mongodb_collection_name,
                "system_prompt": settings.system_prompt,
                "default_model": settings.default_model,
                "max_tokens": settings.max_tokens,
                "temperature": float(settings.temperature) if settings.temperature else 0.7,
                "top_k": settings.top_k,
                "top_p": float(settings.top_p) if settings.top_p else 0.9,
                "chunk_size": settings.chunk_size,
                "chunk_overlap": settings.chunk_overlap,
            }
        return {}
