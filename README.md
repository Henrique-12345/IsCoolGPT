# ðŸŽ“ IsCoolGPT - Assistente Inteligente para Estudantes

AplicaÃ§Ã£o de assistente inteligente que auxilia estudantes em suas disciplinas utilizando modelos de linguagem avanÃ§ados (ChatGPT).

## ðŸ—ï¸ Arquitetura

- **Backend**: Python com FastAPI
- **Frontend**: PÃ¡gina estÃ¡tica em HTML/CSS/JS
- **ContainerizaÃ§Ã£o**: Docker com multi-stage builds
- **Versionamento**: GitHub + espelhamento em CodeCommit
- **CI/CD**: GitHub Actions (build, testes, deploy)
- **Cloud**: AWS (CodeCommit, ECR, ECS, Secrets Manager, CloudWatch)
- **SeguranÃ§a**: IAM com princÃ­pio do menor privilÃ©gio

## ðŸš€ InÃ­cio RÃ¡pido

### PrÃ©-requisitos

- Python 3.11+
- Docker e Docker Compose
- Conta OpenAI com API Key

### InstalaÃ§Ã£o Local

1. Clone o repositÃ³rio:
```bash
git clone <repository-url>
cd IsCoolGPT
```

2. Crie o arquivo `.env`:
```bash
cp .env.example .env
# Edite .env e adicione sua OPENAI_API_KEY
```

3. Instale as dependÃªncias:
```bash
pip install -r requirements.txt
```

4. Execute a aplicaÃ§Ã£o:
```bash
# OpÃ§Ã£o 1: Diretamente com Python
uvicorn app.main:app --reload

# OpÃ§Ã£o 2: Com Docker Compose
docker-compose up --build
```

5. Acesse a documentaÃ§Ã£o da API:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## ðŸ–¥ï¸ Frontend

A interface web estÃ¡tica permite testar rapidamente a API sem depender de ferramentas externas.

- Caminho: `frontend/index.html`
- Estilos: `frontend/styles.css`
- LÃ³gica: `frontend/script.js`
- URL padrÃ£o da API: `http://localhost:8000`

### Como executar o frontend localmente

```bash
cd frontend
python -m http.server 5500
```

Abra http://localhost:5500 no navegador e, se necessÃ¡rio, ajuste o campo â€œURL da APIâ€ para apontar para o endpoint desejado (por exemplo, o DNS pÃºblico do Load Balancer na AWS).

## ðŸ“š DocumentaÃ§Ã£o Completa

- [GUIA_PASSO_A_PASSO.md](./GUIA_PASSO_A_PASSO.md) â€” guia completo de implementaÃ§Ã£o e deploy
- [COMO_CONFIGURAR_SECRETS_GITHUB.md](./COMO_CONFIGURAR_SECRETS_GITHUB.md) â€” configuraÃ§Ã£o de secrets no GitHub Actions
- [COMO_CRIAR_ECS_CONSOLE_AWS.md](./COMO_CRIAR_ECS_CONSOLE_AWS.md) â€” criaÃ§Ã£o da infraestrutura no console AWS

## ðŸ§ª Testes

```bash
# Executar testes
pytest tests/ -v

# Com cobertura
pytest tests/ -v --cov=app --cov-report=html
```

## ðŸ“¦ Estrutura do Projeto

```
IsCoolGPT/
â”œâ”€â”€ app/
â”‚   â”œâ”€â”€ api/
â”‚   â”‚   â””â”€â”€ routes.py          # Rotas da API
â”‚   â”œâ”€â”€ core/
â”‚   â”‚   â””â”€â”€ config.py          # ConfiguraÃ§Ãµes
â”‚   â”œâ”€â”€ models/
â”‚   â”‚   â””â”€â”€ schemas.py         # Modelos Pydantic
â”‚   â”œâ”€â”€ services/
â”‚   â”‚   â””â”€â”€ chat_service.py    # IntegraÃ§Ã£o com OpenAI
â”‚   â”œâ”€â”€ utils/
â”‚   â””â”€â”€ main.py                # Ponto de entrada FastAPI
â”œâ”€â”€ frontend/
â”‚   â”œâ”€â”€ index.html             # Interface web da assistente
â”‚   â”œâ”€â”€ styles.css             # Estilos do frontend
â”‚   â””â”€â”€ script.js              # IntegraÃ§Ã£o com a API
â”œâ”€â”€ tests/
â”‚   â””â”€â”€ test_api.py            # Testes unitÃ¡rios
â”œâ”€â”€ .github/
â”‚   â””â”€â”€ workflows/             # Pipelines GitHub Actions
â”œâ”€â”€ Dockerfile                 # Docker multi-stage
â”œâ”€â”€ docker-compose.yml         # Ambiente local com Docker
â”œâ”€â”€ requirements.txt           # DependÃªncias principais
â””â”€â”€ README.md
```

## ðŸ”„ Fluxo de Deploy

1. **Desenvolvimento Local** â€” codificaÃ§Ã£o, testes e build Docker
2. **Push para GitHub** â€” criaÃ§Ã£o de Pull Request (feature â†’ develop)
3. **ValidaÃ§Ã£o AutomÃ¡tica** â€” GitHub Actions executa lint, testes, build
4. **Deploy Staging** â€” merge para `staging` (+ deploy automÃ¡tico no ECS)
5. **ValidaÃ§Ã£o Final** â€” testes de integraÃ§Ã£o no ambiente de staging
6. **ProduÃ§Ã£o** â€” merge para `main` (+ deploy automÃ¡tico com zero downtime)

## ðŸ”’ SeguranÃ§a

- VariÃ¡veis sensÃ­veis no AWS Secrets Manager
- IAM Roles com permissÃµes mÃ­nimas para ECS, ECR e CodeCommit
- Security Groups, ALB e VPC configurados para acesso seguro
- Logs e mÃ©tricas no CloudWatch (aplicaÃ§Ã£o e infraestrutura)

## ðŸ“ LicenÃ§a

Projeto desenvolvido como trabalho acadÃªmico na disciplina de ComputaÃ§Ã£o em Nuvem.

## ðŸ‘¨â€ðŸ’» Autor

Estudante de CiÃªncia da ComputaÃ§Ã£o â€” Disciplina de ComputaÃ§Ã£o em Nuvem
