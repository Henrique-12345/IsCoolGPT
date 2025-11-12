"""
Configurações centralizadas da aplicação
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    
    # OpenAI Settings
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_MAX_TOKENS: int = 1000
    OPENAI_TEMPERATURE: float = 0.7
    
    # Application Settings
    APP_NAME: str = "IsCoolGPT"
    APP_DESCRIPTION: str = "Assistente Inteligente para Estudantes"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

