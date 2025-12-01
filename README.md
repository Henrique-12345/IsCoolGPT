﻿#  IsCoolGPT - Assistente Inteligente para Estudantes

Aplicação de assistente inteligente que auxilia estudantes em suas disciplinas utilizando modelos de linguagem avançados (ChatGPT).

## Arquitetura

- **Backend**: Python com FastAPI
- **Frontend**: Página estática em HTML/CSS/JS
- **Containerização**: Docker com multi-stage builds
- **Versionamento**: GitHub + espelhamento em CodeCommit
- **CI/CD**: GitHub Actions (build, testes, deploy)
- **Cloud**: AWS (CodeCommit, ECR, ECS, Secrets Manager, CloudWatch)
- **Segurança**: IAM com princÃ­pio do menor privilégio

## Início Rápido

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

## Frontend

A interface web estática permite testar rapidamente a API sem depender de ferramentas externas.

- Caminho: `frontend/index.html`
- Estilos: `frontend/styles.css`
- Lógica: `frontend/script.js`
- URL padrão da API: `http://localhost:8000`

### Como executar o frontend localmente

```bash
cd frontend
python -m http.server 5500
```

Abra http://localhost:5500 no navegador e, se necessário, ajuste o campo URL da API para apontar para o endpoint desejado (por exemplo, o DNS público do Load Balancer na AWS).

## Documentação Completa

- [GUIA_PASSO_A_PASSO.md](./GUIA_PASSO_A_PASSO.md): guia completo de implementação e deploy
- [COMO_CONFIGURAR_SECRETS_GITHUB.md](./COMO_CONFIGURAR_SECRETS_GITHUB.md): configuração de secrets no GitHub Actions
- [COMO_CRIAR_ECS_CONSOLE_AWS.md](./COMO_CRIAR_ECS_CONSOLE_AWS.md): criação da infraestrutura no console AWS

## Testes

```bash
# Executar testes
pytest tests/ -v

# Com cobertura
pytest tests/ -v --cov=app --cov-report=html
```

## Estrutura do Projeto

```
IsCoolGPT/
app/
 api/
 routes.py          # Rotas da API
 core/
 config.py          # Configurações
 models/
 schemas.py         # Modelos Pydantic
 services/
 chat_service.py    # Integração com OpenAI
 utils/
 main.py                # Ponto de entrada FastAPI
frontend/
 index.html             # Interface web da assistente
 styles.css             # Estilos do frontend
 script.js              # Integração com a API
 tests/
 test_api.py            # Testes unitários
 .github/
 workflows/             # Pipelines GitHub Actions
 Dockerfile                 # Docker multi-stage
 docker-compose.yml         # Ambiente local com Docker
 requirements.txt           # Dependências principais
 README.md
```

## Fluxo de Deploy

1. **Desenvolvimento Local**: codificação, testes e build Docker
2. **Push para GitHub**: criação de Pull Request (feature develop)
3. **Validação Automática**: GitHub Actions executa lint, testes, build
4. **Deploy Staging**: merge para `staging` (+ deploy automático no ECS)
5. **Validação Final**: testes de integração no ambiente de staging
6. **Produção**: merge para `main` (+ deploy automático com zero downtime)

## Segurança

- Variáveis sensí­veis no AWS Secrets Manager
- IAM Roles com permissões mí­nimas para ECS, ECR e CodeCommit
- Security Groups, ALB e VPC configurados para acesso seguro
- Logs e métricas no CloudWatch (aplicação e infraestrutura)

## Licença

Projeto desenvolvido como trabalho acadêmico na disciplina de Computação em Nuvem