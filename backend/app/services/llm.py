from langchain.chat_models import ChatOpenAI
from app.core.config import get_settings
from typing import Optional

class LLMService:
    def __init__(self) -> None:
        cfg = get_settings()
        self._cfg = cfg
        self._chat = ChatOpenAI(
            model_name=cfg.llm_model_name,
            temperature=cfg.llm_temperature,
            openai_api_key=cfg.OPENAI_API_KEY.get_secret_value(),
            max_tokens=1000,  # Limitar tokens para respuestas más rápidas
            timeout=30,  # Timeout de 30 segundos
            max_retries=2,  # Máximo 2 reintentos
        )

    def ask(self, prompt: str, user_settings: Optional[dict] = None) -> str:
        # Usar configuración del usuario si está disponible
        if user_settings:
            api_key = user_settings.get("openai_api_key") or self._cfg.OPENAI_API_KEY.get_secret_value()
            model = user_settings.get("default_model", self._cfg.llm_model_name)
            temperature = user_settings.get("temperature", self._cfg.llm_temperature)
            max_tokens = user_settings.get("max_tokens", 1000)
            
            # Crear instancia temporal con configuración del usuario
            chat = ChatOpenAI(
                model_name=model,
                temperature=temperature,
                openai_api_key=api_key,
                max_tokens=max_tokens,
                timeout=30,
                max_retries=2,
            )
            response = chat.invoke(prompt)
        else:
            response = self._chat.invoke(prompt)
        
        return response.content
