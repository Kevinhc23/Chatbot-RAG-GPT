from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db, User
from app.core.security import verify_token, credentials_exception
from app.services.auth import UserService
from typing import Optional

# Configurar el esquema de autenticación
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Obtener usuario actual desde el token"""
    token = credentials.credentials
    email = verify_token(token)
    
    if email is None:
        raise credentials_exception
    
    user_service = UserService(db)
    user = user_service.get_user_by_email(email)
    
    if user is None:
        raise credentials_exception
    
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Obtener usuario activo actual"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current_user

def get_current_superuser(current_user: User = Depends(get_current_user)) -> User:
    """Obtener superusuario actual"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, 
            detail="El usuario no tiene suficientes permisos"
        )
    return current_user

# Dependencia opcional para obtener usuario si existe
def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Obtener usuario actual opcional (puede ser None)"""
    if not credentials:
        return None
    
    token = credentials.credentials
    email = verify_token(token)
    
    if email is None:
        return None
    
    user_service = UserService(db)
    user = user_service.get_user_by_email(email)
    
    return user
