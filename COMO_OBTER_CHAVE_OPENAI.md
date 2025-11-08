# 🔑 Como Obter sua OPENAI_API_KEY

## 📍 Localização do Arquivo .env

O arquivo `.env` deve estar na **raiz do projeto**, no mesmo nível que:
- `requirements.txt`
- `Dockerfile`
- `docker-compose.yml`
- `README.md

## 📝 Nome do Arquivo

O nome do arquivo é exatamente: **`.env`** (com o ponto no início)

⚠️ **Importante**: 
- O arquivo `.env` está no `.gitignore` e **NÃO será versionado** no Git
- Isso é uma boa prática de segurança para não expor suas chaves

## 🔑 Como Obter sua OPENAI_API_KEY

### Passo 1: Acesse a Plataforma OpenAI

1. Acesse: https://platform.openai.com/
2. Faça login com sua conta OpenAI (ou crie uma se não tiver)

### Passo 2: Navegue até API Keys

1. No menu lateral, clique em **"API keys"** ou acesse diretamente:
   https://platform.openai.com/api-keys

### Passo 3: Criar uma Nova Chave

1. Clique no botão **"+ Create new secret key"**
2. Dê um nome para sua chave (ex: "IsCoolGPT - Projeto Acadêmico")
3. Clique em **"Create secret key"**
4. **COPIE A CHAVE IMEDIATAMENTE** - ela só será mostrada uma vez!

### Passo 4: Adicionar ao Arquivo .env

1. Abra o arquivo `.env` na raiz do projeto
2. Substitua `your_openai_api_key_here` pela chave que você copiou
3. Salve o arquivo

**Exemplo:**
```env
OPENAI_API_KEY=sk-proj-abc123xyz789...
```

## ⚠️ Segurança

- **NUNCA** compartilhe sua chave API
- **NUNCA** faça commit do arquivo `.env` no Git
- Se sua chave for exposta, **revogue-a imediatamente** e crie uma nova
- Use chaves diferentes para desenvolvimento e produção

## 💰 Custos

⚠️ **Atenção**: A API da OpenAI é **paga** (pós créditos gratuitos iniciais)

- Você recebe créditos gratuitos ao criar a conta
- Após esgotar, você será cobrado por uso
- Monitore seu uso em: https://platform.openai.com/usage

## ✅ Verificar se a Chave Está Funcionando

Após configurar, teste com:

```bash
# Se estiver usando Docker
docker-compose up --build

# Ou localmente
uvicorn app.main:app --reload
```

Depois acesse: http://localhost:8000/docs e teste o endpoint `/api/v1/chat`

## 🆘 Problemas Comuns

### Erro: "Invalid API Key"
- Verifique se copiou a chave completa (começa com `sk-`)
- Verifique se não há espaços antes ou depois da chave
- Certifique-se de que salvou o arquivo `.env`

### Erro: "Insufficient quota"
- Você esgotou seus créditos gratuitos
- Adicione um método de pagamento na plataforma OpenAI

### Erro: "API key not found"
- A chave pode ter sido revogada
- Crie uma nova chave na plataforma OpenAI

