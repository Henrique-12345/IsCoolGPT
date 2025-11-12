"""
Rotas da API
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()
chat_service = ChatService()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint principal para interação com o assistente

    Recebe uma mensagem do estudante e retorna uma resposta do assistente
    """
    try:
        response = await chat_service.get_response(
            message=request.message, context=request.context, subject=request.subject
        )

        return ChatResponse(response=response, model="gpt-4")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar mensagem: {str(e)}"
        )


@router.get("/subjects")
async def get_subjects():
    """
    Retorna lista de disciplinas suportadas
    """
    subjects = [
        "Matemática",
        "Física",
        "Química",
        "Biologia",
        "História",
        "Geografia",
        "Português",
        "Inglês",
        "Programação",
        "Ciência da Computação",
    ]
    return {"subjects": subjects}
