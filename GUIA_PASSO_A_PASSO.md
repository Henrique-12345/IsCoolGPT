# 🚀 Guia Completo: Assistente Inteligente para Estudantes

## 📋 Visão Geral do Projeto

Este projeto implementa uma assistente inteligente que auxilia estudantes em suas disciplinas utilizando modelos de linguagem avançados (ChatGPT). A arquitetura utiliza FastAPI, Docker, GitHub Actions e serviços AWS.

---

## 📚 ÍNDICE

1. [Fase 1: Desenvolvimento Local](#fase-1-desenvolvimento-local)
2. [Fase 2: Containerização com Docker](#fase-2-containerização-com-docker)
3. [Fase 3: Controle de Versão e CI/CD](#fase-3-controle-de-versão-e-cicd)
4. [Fase 4: Infraestrutura AWS](#fase-4-infraestrutura-aws)
5. [Fase 5: Segurança e IAM](#fase-5-segurança-e-iam)
6. [Fase 6: Deploy e Monitoramento](#fase-6-deploy-e-monitoramento)

---

## 🏗️ FASE 1: DESENVOLVIMENTO LOCAL

### 1.1 Estrutura Inicial do Projeto

```bash
# Criar estrutura de diretórios
mkdir -p app/{api,core,models,services,utils}
mkdir -p tests
mkdir -p .github/workflows
```

### 1.2 Configuração do Ambiente Python

**Criar `requirements.txt`:**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
openai==1.3.0
python-dotenv==1.0.0
httpx==0.25.0
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
flake8==6.1.0
mypy==1.7.0
```

**Criar `requirements-dev.txt`:**
```
-r requirements.txt
pytest-cov==4.1.0
```

### 1.3 Configuração de Variáveis de Ambiente

**Criar `.env.example`:**
```
OPENAI_API_KEY=your_openai_api_key_here
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
LOG_LEVEL=INFO
```

**Criar `.env` (não versionar no Git):**
```
OPENAI_API_KEY=sua_chave_aqui
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### 1.4 Implementação do Backend FastAPI

**Estrutura de arquivos:**
- `app/main.py` - Ponto de entrada da aplicação
- `app/core/config.py` - Configurações centralizadas
- `app/api/routes.py` - Rotas da API
- `app/services/chat_service.py` - Serviço de integração com OpenAI
- `app/models/schemas.py` - Modelos Pydantic

---

## 🐳 FASE 2: CONTAINERIZAÇÃO COM DOCKER

### 2.1 Dockerfile Otimizado (Multi-stage Build)

**Criar `Dockerfile`:**
```dockerfile
# Stage 1: Build
FROM python:3.11-slim as builder

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copiar dependências instaladas do stage builder
COPY --from=builder /root/.local /root/.local

# Copiar código da aplicação
COPY ./app /app/app

# Adicionar binários ao PATH
ENV PATH=/root/.local/bin:$PATH

# Expor porta
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Comando de execução
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2.2 Docker Compose para Desenvolvimento

**Criar `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ENVIRONMENT=development
    volumes:
      - ./app:/app/app
    restart: unless-stopped
```

### 2.3 .dockerignore

**Criar `.dockerignore`:**
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv
.git
.gitignore
.env
*.md
tests/
.pytest_cache
.coverage
```

### 2.4 Teste Local do Container

```bash
# Build da imagem
docker build -t iscoolgpt:latest .

# Execução do container
docker run -p 8000:8000 --env-file .env iscoolgpt:latest

# Ou usando docker-compose
docker-compose up --build
```

---

## 🔄 FASE 3: CONTROLE DE VERSÃO E CI/CD

### 3.1 Inicialização do Repositório GitHub

```bash
# Inicializar Git
git init

# Criar .gitignore
cat > .gitignore << EOF
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv
.env
.idea/
.vscode/
*.log
.coverage
.pytest_cache/
dist/
build/
*.egg-info/
EOF

# Primeiro commit
git add .
git commit -m "Initial commit: Estrutura base do projeto"
```

### 3.2 Estrutura de Branches

```bash
# Criar branches principais
git checkout -b develop
git checkout -b staging
git checkout main
```

**Estratégia de branches:**
- `main` - Produção
- `staging` - Ambiente de testes
- `develop` - Desenvolvimento

### 3.3 GitHub Actions - Workflow CI/CD

**Criar `.github/workflows/ci.yml`:**
```yaml
name: CI Pipeline

on:
  pull_request:
    branches: [main, staging, develop]
  push:
    branches: [develop]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Lint with flake8
      run: |
        flake8 app --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 app --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Format check with black
      run: black --check app/
    
    - name: Type check with mypy
      run: mypy app/ || true
    
    - name: Run tests
      run: |
        pytest tests/ -v --cov=app --cov-report=xml
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: false

  build:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Build Docker image
      run: |
        docker build -t iscoolgpt:${{ github.sha }} .
        docker build -t iscoolgpt:latest .
```

**Criar `.github/workflows/deploy-staging.yml`:**
```yaml
name: Deploy to Staging

on:
  push:
    branches: [staging]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v1
    
    - name: Build, tag, and push image to Amazon ECR
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        ECR_REPOSITORY: iscoolgpt
        IMAGE_TAG: staging-${{ github.sha }}
      run: |
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
        docker tag $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG $ECR_REGISTRY/$ECR_REPOSITORY:staging-latest
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:staging-latest
    
    - name: Deploy to ECS
      run: |
        aws ecs update-service --cluster iscoolgpt-staging --service iscoolgpt-api-staging --force-new-deployment --region us-east-1
```

**Criar `.github/workflows/deploy-production.yml`:**
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v1
    
    - name: Build, tag, and push image to Amazon ECR
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        ECR_REPOSITORY: iscoolgpt
        IMAGE_TAG: ${{ github.sha }}
      run: |
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
        docker tag $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG $ECR_REGISTRY/$ECR_REPOSITORY:latest
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest
    
    - name: Deploy to ECS
      run: |
        aws ecs update-service --cluster iscoolgpt-production --service iscoolgpt-api-production --force-new-deployment --region us-east-1
```

### 3.4 Configuração de Secrets no GitHub

No repositório GitHub, adicionar os seguintes secrets:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `OPENAI_API_KEY`

---

## ☁️ FASE 4: INFRAESTRUTURA AWS

### 4.1 Configuração Inicial AWS

**Pré-requisitos:**
- Conta AWS ativa
- AWS CLI instalado e configurado
- Terraform ou CloudFormation (opcional, para IaC)

### 4.2 CodeCommit - Repositório Git

```bash
# Criar repositório CodeCommit
aws codecommit create-repository \
    --repository-name iscoolgpt \
    --repository-description "Repositório do projeto IsCoolGPT"

# Configurar credenciais Git para CodeCommit
git config --global credential.helper '!aws codecommit credential-helper $@'
git config --global credential.UseHttpPath true

# Adicionar remote CodeCommit
git remote add codecommit https://git-codecommit.us-east-1.amazonaws.com/v1/repos/iscoolgpt
```

### 4.3 ECR - Elastic Container Registry

```bash
# Criar repositório ECR
aws ecr create-repository \
    --repository-name iscoolgpt \
    --image-scanning-configuration scanOnPush=true \
    --region us-east-1

# Obter URI do repositório
aws ecr describe-repositories --repository-names iscoolgpt --region us-east-1

# Login no ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
```

### 4.4 ECS - Elastic Container Service

#### 4.4.1 Criar Cluster ECS

```bash
# Criar cluster para staging
aws ecs create-cluster \
    --cluster-name iscoolgpt-staging \
    --region us-east-1

# Criar cluster para produção
aws ecs create-cluster \
    --cluster-name iscoolgpt-production \
    --region us-east-1
```

#### 4.4.2 Criar Task Definition

**Criar `task-definition-staging.json`:**
```json
{
  "family": "iscoolgpt-staging",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "iscoolgpt-api",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/iscoolgpt:staging-latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "ENVIRONMENT",
          "value": "staging"
        }
      ],
      "secrets": [
        {
          "name": "OPENAI_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:<account-id>:secret:iscoolgpt/openai-api-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/iscoolgpt-staging",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

**Registrar Task Definition:**
```bash
aws ecs register-task-definition \
    --cli-input-json file://task-definition-staging.json \
    --region us-east-1
```

#### 4.4.3 Criar VPC e Networking

```bash
# Criar VPC (ou usar existente)
aws ec2 create-vpc --cidr-block 10.0.0.0/16

# Criar Subnets públicas
aws ec2 create-subnet --vpc-id <vpc-id> --cidr-block 10.0.1.0/24 --availability-zone us-east-1a
aws ec2 create-subnet --vpc-id <vpc-id> --cidr-block 10.0.2.0/24 --availability-zone us-east-1b

# Criar Internet Gateway
aws ec2 create-internet-gateway
aws ec2 attach-internet-gateway --vpc-id <vpc-id> --internet-gateway-id <igw-id>

# Criar Security Group
aws ec2 create-security-group \
    --group-name iscoolgpt-sg \
    --description "Security group for IsCoolGPT API" \
    --vpc-id <vpc-id>

# Adicionar regra para permitir tráfego HTTP
aws ec2 authorize-security-group-ingress \
    --group-id <sg-id> \
    --protocol tcp \
    --port 8000 \
    --cidr 0.0.0.0/0
```

#### 4.4.4 Criar Application Load Balancer (ALB)

```bash
# Criar ALB
aws elbv2 create-load-balancer \
    --name iscoolgpt-alb \
    --subnets <subnet-1> <subnet-2> \
    --security-groups <sg-id> \
    --scheme internet-facing \
    --type application

# Criar Target Group
aws elbv2 create-target-group \
    --name iscoolgpt-tg \
    --protocol HTTP \
    --port 8000 \
    --vpc-id <vpc-id> \
    --target-type ip \
    --health-check-path /health

# Criar Listener
aws elbv2 create-listener \
    --load-balancer-arn <alb-arn> \
    --protocol HTTP \
    --port 80 \
    --default-actions Type=forward,TargetGroupArn=<target-group-arn>
```

#### 4.4.5 Criar ECS Service

```bash
# Criar serviço ECS para staging
aws ecs create-service \
    --cluster iscoolgpt-staging \
    --service-name iscoolgpt-api-staging \
    --task-definition iscoolgpt-staging \
    --desired-count 2 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[<subnet-1>,<subnet-2>],securityGroups=[<sg-id>],assignPublicIp=ENABLED}" \
    --load-balancers "targetGroupArn=<target-group-arn>,containerName=iscoolgpt-api,containerPort=8000" \
    --region us-east-1
```

### 4.5 Secrets Manager - Armazenar Chaves

```bash
# Criar secret para OpenAI API Key
aws secretsmanager create-secret \
    --name iscoolgpt/openai-api-key \
    --secret-string "your-openai-api-key-here" \
    --region us-east-1
```

### 4.6 CloudWatch - Logs e Monitoramento

```bash
# Criar Log Groups
aws logs create-log-group --log-group-name /ecs/iscoolgpt-staging --region us-east-1
aws logs create-log-group --log-group-name /ecs/iscoolgpt-production --region us-east-1
```

---

## 🔒 FASE 5: SEGURANÇA E IAM

### 5.1 Criar Roles e Políticas IAM

#### 5.1.1 Role para ECS Task Execution

**Criar `ecs-task-execution-role-policy.json`:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "arn:aws:secretsmanager:*:*:secret:iscoolgpt/*"
    }
  ]
}
```

```bash
# Criar política
aws iam create-policy \
    --policy-name IsCoolGPT-ECSTaskExecutionPolicy \
    --policy-document file://ecs-task-execution-role-policy.json

# Criar role
aws iam create-role \
    --role-name IsCoolGPT-ECSTaskExecutionRole \
    --assume-role-policy-document '{
      "Version": "2012-10-17",
      "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "ecs-tasks.amazonaws.com"},
        "Action": "sts:AssumeRole"
      }]
    }'

# Anexar política à role
aws iam attach-role-policy \
    --role-name IsCoolGPT-ECSTaskExecutionRole \
    --policy-arn arn:aws:iam::<account-id>:policy/IsCoolGPT-ECSTaskExecutionPolicy
```

#### 5.1.2 Role para GitHub Actions

**Criar `github-actions-role-policy.json`:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload"
      ],
      "Resource": "arn:aws:ecr:*:*:repository/iscoolgpt"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecs:UpdateService",
        "ecs:DescribeServices"
      ],
      "Resource": "arn:aws:ecs:*:*:service/*/iscoolgpt-*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "codecommit:GitPush",
        "codecommit:GitPull",
        "codecommit:GetRepository"
      ],
      "Resource": "arn:aws:codecommit:*:*:iscoolgpt"
    }
  ]
}
```

```bash
# Criar política
aws iam create-policy \
    --policy-name IsCoolGPT-GitHubActionsPolicy \
    --policy-document file://github-actions-role-policy.json

# Criar usuário para GitHub Actions
aws iam create-user --user-name IsCoolGPT-GitHubActions

# Anexar política ao usuário
aws iam attach-user-policy \
    --user-name IsCoolGPT-GitHubActions \
    --policy-arn arn:aws:iam::<account-id>:policy/IsCoolGPT-GitHubActionsPolicy

# Criar access key (usar no GitHub Secrets)
aws iam create-access-key --user-name IsCoolGPT-GitHubActions
```

### 5.2 Atualizar Task Definition com Role

Adicionar `executionRoleArn` na task definition:
```json
{
  "executionRoleArn": "arn:aws:iam::<account-id>:role/IsCoolGPT-ECSTaskExecutionRole",
  ...
}
```

---

## 🚀 FASE 6: DEPLOY E MONITORAMENTO

### 6.1 Fluxo de Deploy Completo

#### Passo 1: Desenvolvimento Local
```bash
# Desenvolver feature
git checkout -b feature/nova-funcionalidade

# Testar localmente
docker-compose up --build

# Executar testes
pytest tests/ -v
```

#### Passo 2: Push para GitHub
```bash
# Commit e push
git add .
git commit -m "feat: adiciona nova funcionalidade"
git push origin feature/nova-funcionalidade

# Criar Pull Request no GitHub
```

#### Passo 3: Validação Automática
- GitHub Actions executa CI pipeline
- Testes, linting e build são validados
- Aguardar aprovação do PR

#### Passo 4: Deploy Staging
```bash
# Merge para staging
git checkout staging
git merge develop
git push origin staging

# GitHub Actions faz deploy automático para ECS staging
```

#### Passo 5: Validação em Staging
```bash
# Testar endpoint staging
curl https://staging-api.iscoolgpt.com/health

# Validar funcionalidades
# Executar testes de integração
```

#### Passo 6: Deploy Produção
```bash
# Merge para main
git checkout main
git merge staging
git push origin main

# GitHub Actions faz deploy automático para ECS produção
```

### 6.2 Monitoramento e Logs

#### CloudWatch Logs
```bash
# Visualizar logs do serviço
aws logs tail /ecs/iscoolgpt-production --follow --region us-east-1
```

#### CloudWatch Metrics
- CPU Utilization
- Memory Utilization
- Request Count
- Error Rate

#### Alertas CloudWatch
```bash
# Criar alarme para alta utilização de CPU
aws cloudwatch put-metric-alarm \
    --alarm-name iscoolgpt-high-cpu \
    --alarm-description "Alerta quando CPU > 80%" \
    --metric-name CPUUtilization \
    --namespace AWS/ECS \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 2
```

### 6.3 Rollback

```bash
# Reverter para versão anterior
aws ecs update-service \
    --cluster iscoolgpt-production \
    --service iscoolgpt-api-production \
    --task-definition iscoolgpt-production:<previous-revision> \
    --force-new-deployment
```

---

## 📝 CHECKLIST FINAL

### Desenvolvimento
- [ ] Estrutura do projeto criada
- [ ] FastAPI implementado
- [ ] Integração com OpenAI funcionando
- [ ] Testes unitários criados
- [ ] Dockerfile otimizado
- [ ] Docker Compose configurado

### Versionamento
- [ ] Repositório GitHub criado
- [ ] Branches (main, staging, develop) configuradas
- [ ] .gitignore configurado
- [ ] GitHub Actions workflows criados

### AWS - CodeCommit
- [ ] Repositório CodeCommit criado
- [ ] Credenciais configuradas

### AWS - ECR
- [ ] Repositório ECR criado
- [ ] Imagem Docker pushada

### AWS - ECS
- [ ] Clusters criados (staging e production)
- [ ] VPC e networking configurados
- [ ] Security Groups configurados
- [ ] ALB criado e configurado
- [ ] Task Definitions criadas
- [ ] Services criados e rodando

### AWS - Segurança
- [ ] Secrets Manager configurado
- [ ] IAM Roles criadas
- [ ] IAM Policies aplicadas
- [ ] CloudWatch Logs configurados

### Deploy
- [ ] Deploy staging funcionando
- [ ] Deploy produção funcionando
- [ ] Monitoramento configurado
- [ ] Alertas configurados

---

## 🆘 TROUBLESHOOTING

### Problema: Container não inicia
```bash
# Verificar logs
docker logs <container-id>

# Verificar variáveis de ambiente
docker exec <container-id> env
```

### Problema: ECS Task não inicia
```bash
# Verificar eventos do serviço
aws ecs describe-services \
    --cluster iscoolgpt-staging \
    --services iscoolgpt-api-staging

# Verificar logs do CloudWatch
aws logs tail /ecs/iscoolgpt-staging --follow
```

### Problema: Imagem não encontrada no ECR
```bash
# Verificar login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Verificar tags
aws ecr describe-images --repository-name iscoolgpt
```

---

## 📚 RECURSOS ADICIONAIS

- [Documentação FastAPI](https://fastapi.tiangolo.com/)
- [Documentação Docker](https://docs.docker.com/)
- [Documentação AWS ECS](https://docs.aws.amazon.com/ecs/)
- [Documentação GitHub Actions](https://docs.github.com/en/actions)
- [Documentação OpenAI API](https://platform.openai.com/docs/)

---

## 🎯 PRÓXIMOS PASSOS

1. Implementar autenticação e autorização
2. Adicionar rate limiting
3. Implementar cache (Redis/ElastiCache)
4. Adicionar banco de dados (RDS)
5. Implementar CI/CD completo com testes automatizados
6. Adicionar monitoramento avançado (Datadog, New Relic)
7. Implementar backup e disaster recovery

---

**Boa sorte com seu projeto! 🚀**

