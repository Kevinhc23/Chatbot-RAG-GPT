from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Esquemas para autenticación
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None

# Esquemas para configuración de usuario
class UserSettingsBase(BaseModel):
    openai_api_key: Optional[str] = None
    mongo_uri: Optional[str] = None
    mongo_db: Optional[str] = None
    mongo_collection: Optional[str] = None
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4o-mini"
    llm_temperature: str = "0.0"
    system_prompt: Optional[str] = None
    welcome_message: Optional[str] = None
    theme: str = "light"
    language: str = "es"

class UserSettingsCreate(UserSettingsBase):
    pass

class UserSettingsUpdate(BaseModel):
    openai_api_key: Optional[str] = None
    mongo_uri: Optional[str] = None
    mongo_db: Optional[str] = None
    mongo_collection: Optional[str] = None
    embedding_model: Optional[str] = None
    llm_model: Optional[str] = None
    llm_temperature: Optional[str] = None
    system_prompt: Optional[str] = None
    welcome_message: Optional[str] = None
    theme: Optional[str] = None
    language: Optional[str] = None

class UserSettingsResponse(UserSettingsBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserWithSettings(UserResponse):
    settings: Optional[UserSettingsResponse] = None
