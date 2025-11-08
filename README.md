# 🎓 IsCoolGPT - Assistente Inteligente para Estudantes

Aplicação de assistente inteligente que auxilia estudantes em suas disciplinas utilizando modelos de linguagem avançados (ChatGPT).

## 🏗️ Arquitetura

- **Backend**: Python com FastAPI
- **Containerização**: Docker com multi-stage builds
- **Versionamento**: GitHub
- **CI/CD**: GitHub Actions
- **Cloud**: AWS (CodeCommit, ECR, ECS)
- **Segurança**: IAM com princípio do menor privilégio

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.11+
- Docker e Docker Compose
- Conta OpenAI com API Key

### Instalação Local

1. Clone o repositório:
```bash
git clone <repository-url>
cd IsCoolGPT
```

2. Crie o arquivo `.env`:
```bash
cp .env.example .env
# Edite .env e adicione sua OPENAI_API_KEY
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute a aplicação:
```bash
# Opção 1: Diretamente com Python
uvicorn app.main:app --reload

# Opção 2: Com Docker Compose
docker-compose up --build
```

5. Acesse a documentação da API:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📚 Documentação Completa

Consulte o arquivo [GUIA_PASSO_A_PASSO.md](./GUIA_PASSO_A_PASSO.md) para o guia completo de implementação e deploy.

## 🧪 Testes

```bash
# Executar testes
pytest tests/ -v

# Com cobertura
pytest tests/ -v --cov=app --cov-report=html
```

## 📦 Estrutura do Projeto

```
IsCoolGPT/
├── app/
│   ├── api/
│   │   └── routes.py          # Rotas da API
│   ├── core/
│   │   └── config.py          # Configurações
│   ├── models/
│   │   └── schemas.py         # Modelos Pydantic
│   ├── services/
│   │   └── chat_service.py    # Serviço OpenAI
│   ├── utils/
│   └── main.py                # Ponto de entrada
├── tests/
│   └── test_api.py           # Testes
├── .github/
│   └── workflows/            # GitHub Actions
├── Dockerfile                 # Docker multi-stage
├── docker-compose.yml         # Docker Compose
├── requirements.txt           # Dependências
└── README.md
```

## 🔄 Fluxo de Deploy

1. **Desenvolvimento Local**: Codificação e testes
2. **Push para GitHub**: Commit e Pull Request
3. **Validação Automática**: GitHub Actions executa CI
4. **Deploy Staging**: Merge para staging → deploy automático
5. **Validação Final**: Testes em staging
6. **Produção**: Merge para main → deploy automático

## 🔒 Segurança

- Variáveis sensíveis em Secrets Manager (AWS)
- IAM Roles com menor privilégio
- Security Groups configurados
- Logs no CloudWatch

## 📝 Licença

Este projeto é parte de um trabalho acadêmico.

## 👨‍💻 Autor

Estudante de Ciência da Computação - Disciplina de Computação em Nuvem

