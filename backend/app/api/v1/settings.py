from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db, User
from app.services.auth import UserService
from app.models.auth import UserSettingsUpdate, UserSettingsResponse
from app.core.deps import get_current_active_user

router = APIRouter(prefix="/settings", tags=["User Settings"])

@router.get("", response_model=UserSettingsResponse)
async def get_user_settings(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener configuración del usuario"""
    user_service = UserService(db)
    settings = user_service.get_user_settings(current_user.id)
    
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuración no encontrada"
        )
    
    return settings

@router.put("", response_model=UserSettingsResponse)
async def update_user_settings(
    settings_update: UserSettingsUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Actualizar configuración del usuario"""
    user_service = UserService(db)
    updated_settings = user_service.update_user_settings(current_user.id, settings_update)
    
    if not updated_settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuración no encontrada"
        )
    
    return updated_settings

@router.post("/test-openai")
async def test_openai_key(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Probar la clave API de OpenAI"""
    user_service = UserService(db)
    settings = user_service.get_user_settings(current_user.id)
    
    if not settings or not settings.openai_api_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se ha configurado la clave API de OpenAI"
        )
    
    try:
        import openai
        openai.api_key = settings.openai_api_key
        
        # Hacer una llamada simple para probar la clave
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=5
        )
        
        return {"valid": True, "message": "Clave API válida"}
    except Exception as e:
        return {"valid": False, "message": f"Error: {str(e)}"}

@router.post("/test-mongodb")
async def test_mongodb_connection(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Probar la conexión a MongoDB"""
    user_service = UserService(db)
    settings = user_service.get_user_settings(current_user.id)
    
    if not settings or not settings.mongo_uri:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se ha configurado la URI de MongoDB"
        )
    
    try:
        from pymongo import MongoClient
        
        client = MongoClient(settings.mongo_uri)
        # Probar conexión
        client.admin.command('ping')
        
        # Verificar base de datos y colección si están configuradas
        if settings.mongo_db and settings.mongo_collection:
            db_mongo = client[settings.mongo_db]
            collection = db_mongo[settings.mongo_collection]
            count = collection.count_documents({})
            
            return {
                "valid": True, 
                "message": f"Conexión exitosa. Documentos en colección: {count}"
            }
        else:
            return {"valid": True, "message": "Conexión exitosa"}
            
    except Exception as e:
        return {"valid": False, "message": f"Error: {str(e)}"}
