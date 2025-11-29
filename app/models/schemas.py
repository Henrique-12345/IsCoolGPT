"""
Modelos Pydantic para validação de dados
"""
from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    """Modelo de requisição para chat"""

    message: str = Field(
        ..., min_length=1, max_length=2000, description="Mensagem do estudante"
    )
    subject: Optional[str] = Field(None, description="Disciplina relacionada")
    context: Optional[str] = Field(None, description="Contexto adicional da conversa")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Explique o que é uma função em Python",
                "subject": "Programação",
                "context": "Estou estudando Python básico",
            }
        }


class ChatResponse(BaseModel):
    """Modelo de resposta do chat"""

    response: str = Field(..., description="Resposta do assistente")
    model: str = Field(..., description="Modelo utilizado")

    class Config:
        json_schema_extra = {
            "example": {
                "response": "Uma função em Python é um bloco de código reutilizável...",
                "model": "gpt-4",
            }
        }
