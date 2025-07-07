from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db, User
from app.services.auth import UserService
from app.models.auth import (
    UserCreate, UserLogin, Token, UserResponse, 
    UserUpdate, UserWithSettings
)
from app.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.deps import get_current_active_user, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
async def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """Registrar nuevo usuario"""
    try:
        print(f"Intentando registrar usuario: {user.email}")
        user_service = UserService(db)
        result = user_service.create_user(user)
        print(f"Usuario registrado exitosamente: {result.email}")
        return result
    except Exception as e:
        print(f"Error al registrar usuario: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al registrar usuario: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """Iniciar sesión"""
    user_service = UserService(db)
    user = user_service.authenticate_user(user_credentials.email, user_credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserWithSettings)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener información del usuario actual"""
    user_service = UserService(db)
    settings = user_service.get_user_settings(current_user.id)
    
    return UserWithSettings(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        settings=settings
    )

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Actualizar información del usuario actual"""
    user_service = UserService(db)
    updated_user = user_service.update_user(current_user.id, user_update)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return updated_user

@router.post("/verify-token")
async def verify_token(current_user: User = Depends(get_current_user)):
    """Verificar si el token es válido"""
    return {"valid": True, "user_id": current_user.id, "email": current_user.email}
