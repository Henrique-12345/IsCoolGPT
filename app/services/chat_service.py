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
        # Modo de teste (quando OPENAI_API_KEY não está configurada ou é "test")
        if settings.ENVIRONMENT == "test" or not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "test":
            return self._get_mock_response(message, subject, context)
        
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
            # Se for erro de quota, retorna resposta mock
            error_str = str(e)
            if "quota" in error_str.lower() or "429" in error_str or "insufficient_quota" in error_str:
                return self._get_mock_response(message, subject, context, is_quota_error=True)
            raise Exception(f"Erro ao comunicar com OpenAI: {str(e)}")
    
    def _get_mock_response(
        self,
        message: str,
        subject: Optional[str] = None,
        context: Optional[str] = None,
        is_quota_error: bool = False
    ) -> str:
        """
        Retorna uma resposta simulada para testes ou quando há erro de quota
        
        Args:
            message: Mensagem do estudante
            subject: Disciplina relacionada
            context: Contexto adicional
            is_quota_error: Se True, indica que é um erro de quota
            
        Returns:
            Resposta simulada do assistente
        """
        if is_quota_error:
            prefix = "⚠️ [MODO TESTE - Quota OpenAI esgotada]\n\n"
        else:
            prefix = "🧪 [MODO TESTE]\n\n"
        
        # Respostas simuladas baseadas na mensagem
        message_lower = message.lower()
        
        if "função" in message_lower or "function" in message_lower:
            response = f"""{prefix}Uma função em Python é um bloco de código reutilizável que executa uma tarefa específica. 

**Sintaxe básica:**
```python
def nome_da_funcao(parametros):
    # código aqui
    return resultado
```

**Exemplo prático:**
```python
def saudacao(nome):
    return f"Olá, {nome}! Bem-vindo ao Python!"
```

**Características principais:**
- Permite reutilização de código
- Pode receber parâmetros
- Pode retornar valores
- Ajuda a organizar o código

**Dica:** Use funções para evitar repetir código e tornar seu programa mais organizado!"""
        
        elif "variável" in message_lower or "variable" in message_lower:
            response = f"""{prefix}Uma variável em Python é um espaço na memória usado para armazenar dados.

**Como criar:**
```python
nome = "João"
idade = 25
altura = 1.75
```

**Tipos de variáveis:**
- **String (str)**: Texto - `"Olá"`
- **Int (int)**: Números inteiros - `42`
- **Float (float)**: Números decimais - `3.14`
- **Boolean (bool)**: True ou False

**Dica:** Python detecta automaticamente o tipo da variável!"""
        
        elif "lista" in message_lower or "list" in message_lower:
            response = f"""{prefix}Uma lista em Python é uma coleção ordenada de itens.

**Criar uma lista:**
```python
frutas = ["maçã", "banana", "laranja"]
numeros = [1, 2, 3, 4, 5]
```

**Operações comuns:**
- Adicionar: `frutas.append("uva")`
- Acessar: `frutas[0]` (primeiro item)
- Tamanho: `len(frutas)`

**Dica:** Listas são mutáveis, você pode alterá-las depois de criadas!"""
        
        else:
            response = f"""{prefix}Olá! Sou o IsCoolGPT, seu assistente educacional.

Você perguntou: "{message}"

**Resposta simulada (modo teste):**

Esta é uma resposta de exemplo. Para obter respostas reais do assistente, você precisa:

1. Adicionar créditos na sua conta OpenAI
2. Ou configurar uma nova chave API com créditos disponíveis

**Sobre sua pergunta:**
Sua pergunta parece ser sobre "{subject or 'um tópico geral'}". Em modo de produção, eu forneceria uma explicação detalhada e personalizada sobre este assunto.

**Dica:** Configure sua conta OpenAI para usar o assistente completo!"""
        
        return response
    
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

