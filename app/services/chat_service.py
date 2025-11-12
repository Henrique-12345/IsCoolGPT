"""
Serviço de integração com OpenAI
"""
from openai import AsyncOpenAI
from app.core.config import settings
from typing import Optional


class ChatService:
    """Serviço para interação com OpenAI"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
    
    async def get_response(
        self,
        message: str,
        subject: Optional[str] = None,
        context: Optional[str] = None
    ) -> str:
        """
        Obtém resposta do modelo de linguagem
        
        Args:
            message: Mensagem do estudante
            subject: Disciplina relacionada
            context: Contexto adicional
            
        Returns:
            Resposta do assistente
        """
        # Construir prompt do sistema
        system_prompt = self._build_system_prompt(subject)
        
        # Construir mensagens
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        if context:
            messages.append({
                "role": "user",
                "content": f"Contexto: {context}\n\nPergunta: {message}"
            })
        else:
            messages.append({"role": "user", "content": message})
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=settings.OPENAI_MAX_TOKENS,
                temperature=settings.OPENAI_TEMPERATURE
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Erro ao comunicar com OpenAI: {str(e)}")
    
    def _build_system_prompt(self, subject: Optional[str] = None) -> str:
        """
        Constrói o prompt do sistema baseado na disciplina
        
        Args:
            subject: Disciplina relacionada
            
        Returns:
            Prompt do sistema
        """
        base_prompt = """Você é um assistente educacional inteligente chamado IsCoolGPT, 
        especializado em ajudar estudantes em suas disciplinas acadêmicas. 
        Seu objetivo é fornecer explicações claras, didáticas e precisas.
        
        Diretrizes:
        - Seja paciente e encorajador
        - Use linguagem clara e acessível
        - Forneça exemplos práticos quando possível
        - Incentive o aprendizado ativo
        - Se não souber algo, seja honesto sobre isso
        """
        
        if subject:
            base_prompt += f"\n\nFoco atual: {subject}"
        
        return base_prompt

