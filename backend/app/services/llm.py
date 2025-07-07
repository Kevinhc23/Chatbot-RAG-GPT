from langchain.chat_models import ChatOpenAI
from app.core.config import get_settings

class LLMService:
    def __init__(self) -> None:
        cfg = get_settings()
        self._chat = ChatOpenAI(
            model_name=cfg.llm_model_name,
            temperature=cfg.llm_temperature,
            openai_api_key=cfg.OPENAI_API_KEY.get_secret_value(),
            max_tokens=1000,  # Limitar tokens para respuestas más rápidas
            timeout=30,  # Timeout de 30 segundos
            max_retries=2,  # Máximo 2 reintentos
        )

    def ask(self, prompt: str) -> str:
        response = self._chat.invoke(prompt)
        return response.content
