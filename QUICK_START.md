# 🚀 Quick Start - IsCoolGPT

Guia rápido para começar a usar o projeto.

## 📋 Pré-requisitos

- Python 3.11+
- Docker e Docker Compose
- Conta OpenAI com API Key
- Conta AWS (para deploy)

## ⚡ Início Rápido Local

### 1. Clone e Configure

```bash
# Clone o repositório
git clone <seu-repositorio>
cd IsCoolGPT

# Crie o arquivo .env
cp .env.example .env

# Edite .env e adicione sua OPENAI_API_KEY
# OPENAI_API_KEY=sk-...
```

### 2. Execute com Docker (Recomendado)

```bash
# Build e execute
docker-compose up --build

# A API estará disponível em http://localhost:8000
```

### 3. Ou Execute Localmente

```bash
# Instale dependências
pip install -r requirements.txt

# Execute
uvicorn app.main:app --reload
```

### 4. Teste a API

```bash
# Health check
curl http://localhost:8000/health

# Teste o chat
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explique o que é Python",
    "subject": "Programação"
  }'
```

### 5. Documentação Interativa

Acesse:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testes

```bash
# Executar testes
pytest tests/ -v

# Com cobertura
pytest tests/ -v --cov=app
```

## 📦 Build Docker

```bash
# Build da imagem
docker build -t iscoolgpt:latest .

# Executar container
docker run -p 8000:8000 --env-file .env iscoolgpt:latest
```

## 🔄 Próximos Passos

Para deploy completo na AWS, consulte o [GUIA_PASSO_A_PASSO.md](./GUIA_PASSO_A_PASSO.md)

