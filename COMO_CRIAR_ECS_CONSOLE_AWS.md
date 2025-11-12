# 🏗️ Como Criar Infraestrutura ECS pelo Console AWS

Guia passo a passo usando apenas o Console Web da AWS (sem linha de comando).

---

## 📋 PASSO 1: Criar Clusters ECS

### 1.1 Acessar ECS

1. Acesse: https://console.aws.amazon.com/ecs/
2. Certifique-se de que está na região **us-east-1** (canto superior direito)
3. No menu lateral esquerdo, clique em **"Clusters"**

### 1.2 Criar Cluster Staging

1. Clique no botão **"Create Cluster"** (Criar Cluster)
2. **Cluster name**: `iscoolgpt-staging`
3. **Infrastructure**: Selecione **"AWS Fargate (serverless)"**
4. Deixe as outras opções padrão
5. Clique em **"Create"** (Criar)
6. Aguarde alguns segundos até aparecer "Active"

### 1.3 Criar Cluster Production

1. Clique novamente em **"Create Cluster"**
2. **Cluster name**: `iscoolgpt-production`
3. **Infrastructure**: Selecione **"AWS Fargate (serverless)"**
4. Deixe as outras opções padrão
5. Clique em **"Create"**
6. Aguarde alguns segundos até aparecer "Active"

✅ **Você agora tem 2 clusters criados!**

---

## 🌐 PASSO 2: Configurar VPC e Networking

### 2.1 Acessar VPC

1. Acesse: https://console.aws.amazon.com/vpc/
2. Certifique-se de que está na região **us-east-1**

### 2.2 Usar VPC Default (Mais Fácil)

1. No menu lateral, clique em **"Your VPCs"** (Suas VPCs)
2. Procure por uma VPC chamada **"default"** ou que tenha **"172.31.0.0/16"** ou **"10.0.0.0/16"**
3. **Anote o VPC ID** (começa com `vpc-`)
   - Exemplo: `vpc-0a1b2c3d4e5f6g7h8`

### 2.3 Encontrar Subnets Públicas

1. No menu lateral, clique em **"Subnets"** (Sub-redes)
2. Filtre pela VPC que você anotou
3. Procure por subnets que tenham **"Auto-assign public IPv4 address"** = **Yes**
4. **Anote pelo menos 2 Subnet IDs** de zonas diferentes (Availability Zones diferentes)
   - Exemplo: 
     - `subnet-abc123` (us-east-1a)
     - `subnet-def456` (us-east-1b)

---

## 🔒 PASSO 3: Criar Security Group

### 3.1 Criar Security Group

1. No menu lateral VPC, clique em **"Security Groups"** (Grupos de Segurança)
2. Clique em **"Create security group"** (Criar grupo de segurança)

### 3.2 Configurar Security Group

**Basic details:**
- **Security group name**: `iscoolgpt-sg`
- **Description**: `Security group for IsCoolGPT API`
- **VPC**: Selecione a VPC que você anotou (default)

**Inbound rules (Regras de entrada):**
1. Clique em **"Add rule"** (Adicionar regra)
2. **Type**: HTTP
3. **Port**: `8000`
4. **Source**: `0.0.0.0/0` (permite acesso de qualquer lugar)
5. **Description**: `Allow HTTP on port 8000`

**Outbound rules (Regras de saída):**
- Deixe o padrão (All traffic)

6. Clique em **"Create security group"**
7. **Anote o Security Group ID** (começa com `sg-`)
   - Exemplo: `sg-0a1b2c3d4e5f6g7h8`

✅ **Security Group criado!**

---

## ⚖️ PASSO 4: Criar Application Load Balancer (ALB)

### 4.1 Acessar Load Balancers

1. Acesse: https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#LoadBalancers:
2. Certifique-se de que está na região **us-east-1**
3. Clique em **"Create Load Balancer"** (Criar Load Balancer)

### 4.2 Escolher Tipo

1. Selecione **"Application Load Balancer"**
2. Clique em **"Create"**

### 4.3 Configurar Load Balancer

**Basic configuration:**
- **Name**: `iscoolgpt-alb`
- **Scheme**: **Internet-facing** (voltado para internet)
- **IP address type**: **IPv4**

**Network mapping:**
- **VPC**: Selecione a VPC que você anotou
- **Mappings**: 
  - Marque **pelo menos 2 Availability Zones**
  - Para cada zona, selecione uma das subnets públicas que você anotou
  - Exemplo:
    - `us-east-1a` → selecione `subnet-abc123`
    - `us-east-1b` → selecione `subnet-def456`

**Security groups:**
- Desmarque o security group padrão
- Selecione o security group que você criou: `iscoolgpt-sg`

**Listeners and routing:**
- **Protocol**: HTTP
- **Port**: 80
- **Default action**: Clique em **"Create target group"** (vamos criar depois)

### 4.4 Criar Target Group (Agora)

Uma nova aba/janela vai abrir:

**Basic configuration:**
- **Target type**: **IP addresses**
- **Target group name**: `iscoolgpt-tg`
- **Protocol**: HTTP
- **Port**: 8000
- **VPC**: Selecione a mesma VPC

**Health checks:**
- **Health check path**: `/health`
- Deixe o resto padrão

Clique em **"Next"** e depois **"Create target group"**

### 4.5 Voltar e Finalizar ALB

1. Volte para a aba do Load Balancer
2. Em **"Default action"**, selecione o Target Group que você acabou de criar: `iscoolgpt-tg`
3. Clique em **"Create load balancer"**
4. Aguarde alguns minutos até o status mudar para **"Active"**
5. **Anote o DNS name** do Load Balancer (aparece na lista)
   - Exemplo: `iscoolgpt-alb-123456789.us-east-1.elb.amazonaws.com`

✅ **Load Balancer criado!**

---

## 📝 PASSO 5: Criar Task Definitions

### 5.1 Obter Account ID

1. Clique no seu nome de usuário no canto superior direito
2. **Anote o Account ID** (número de 12 dígitos)
   - Exemplo: `123456789012`

### 5.2 Preparar Task Definition Staging

1. Abra o arquivo `task-definition-staging.json` no seu projeto
2. Substitua todas as ocorrências de `ACCOUNT_ID` pelo seu Account ID real
3. Substitua todas as ocorrências de `us-east-1` se necessário (já deve estar correto)

**Exemplo:**
- Antes: `"arn:aws:iam::ACCOUNT_ID:role/..."`
- Depois: `"arn:aws:iam::123456789012:role/..."`

### 5.3 Verificar/Criar Secret no Secrets Manager

1. Acesse: https://console.aws.amazon.com/secretsmanager/
2. Certifique-se de que está na região **us-east-1**
3. Procure por um secret chamado `iscoolgpt/openai-api-key`
4. Se não existir:
   - Clique em **"Store a new secret"**
   - **Secret type**: **Other type of secret**
   - **Key/value**: 
     - Key: `OPENAI_API_KEY`
     - Value: (cole sua chave OpenAI)
   - **Secret name**: `iscoolgpt/openai-api-key`
   - Clique em **"Next"** → **"Store"**

### 5.4 Verificar/Criar IAM Role para ECS

1. Acesse: https://console.aws.amazon.com/iam/
2. No menu lateral, clique em **"Roles"**
3. Procure por `IsCoolGPT-ECSTaskExecutionRole`
4. Se não existir, você precisa criar (veja o guia de IAM no projeto)

### 5.5 Registrar Task Definition Staging

1. Volte para: https://console.aws.amazon.com/ecs/
2. No menu lateral, clique em **"Task definitions"**
3. Clique em **"Create new task definition"** → **"Create new task definition with JSON"**
4. **Cole o conteúdo completo** do arquivo `task-definition-staging.json` (já com Account ID corrigido)
5. Clique em **"Create"**

### 5.6 Registrar Task Definition Production

1. Clique novamente em **"Create new task definition"** → **"Create new task definition with JSON"**
2. **Cole o conteúdo completo** do arquivo `task-definition-production.json` (já com Account ID corrigido)
3. Clique em **"Create"**

✅ **Task Definitions criadas!**

---

## 🚀 PASSO 6: Criar ECS Services

### 6.1 Criar Service Staging

1. Acesse: https://console.aws.amazon.com/ecs/
2. Clique em **"Clusters"** → clique no cluster **"iscoolgpt-staging"**
3. Na aba **"Services"**, clique em **"Create"**

**Configure service:**
- **Compute configuration**: **Launch type** = **Fargate**
- **Task definition**:
  - **Family**: Selecione `iscoolgpt-staging`
  - **Revision**: Selecione a mais recente (geralmente `1`)
- **Service name**: `iscoolgpt-api-staging`
- **Desired tasks**: `1`

**Networking:**
- **VPC**: Selecione a VPC que você anotou
- **Subnets**: Selecione as 2 subnets públicas que você anotou
- **Security groups**: Selecione `iscoolgpt-sg`
- **Auto-assign public IP**: **ENABLED**

**Load balancing:**
- **Load balancer type**: **Application Load Balancer**
- **Load balancer name**: Selecione `iscoolgpt-alb`
- **Container to load balance**: Clique em **"Add to load balancer"**
  - **Target group name**: Selecione `iscoolgpt-tg`
  - **Container name**: `iscoolgpt-api`
  - **Container port**: `8000`

**Service auto scaling:**
- Deixe desabilitado por enquanto

Clique em **"Create"**

### 6.2 Criar Service Production

1. Volte para **"Clusters"** → clique no cluster **"iscoolgpt-production"**
2. Na aba **"Services"**, clique em **"Create"**
3. Repita os mesmos passos acima, mas:
   - **Service name**: `iscoolgpt-api-production`
   - **Task definition**: Selecione `iscoolgpt-production`

Clique em **"Create"**

✅ **Services criados!**

---

## ✅ PASSO 7: Verificar se Está Funcionando

### 7.1 Verificar Status do Service

1. No cluster, vá na aba **"Services"**
2. Clique no serviço `iscoolgpt-api-staging`
3. Na aba **"Tasks"**, você deve ver tasks com status **"Running"**
4. Se estiver "Pending" ou "Stopped", clique na task para ver os logs

### 7.2 Testar a API

1. Volte para o Load Balancer e copie o **DNS name**
2. Abra no navegador:
   ```
   http://SEU-DNS-DO-ALB/health
   ```
   Exemplo: `http://iscoolgpt-alb-123456789.us-east-1.elb.amazonaws.com/health`

3. Você deve ver:
   ```json
   {"status":"healthy","service":"iscoolgpt-api"}
   ```

✅ **Tudo funcionando!**

---

## 🆘 Troubleshooting

### Service não inicia

1. No ECS, clique no serviço → aba **"Events"**
2. Veja as mensagens de erro
3. Problemas comuns:
   - **Task role não encontrada**: Crie a IAM role `IsCoolGPT-ECSTaskExecutionRole`
   - **Secret não encontrado**: Verifique se o secret existe no Secrets Manager
   - **Imagem não encontrada**: Verifique se a imagem foi enviada para o ECR

### Ver logs

1. No ECS, clique no serviço → aba **"Tasks"** → clique na task
2. Na aba **"Logs"**, você verá os logs do container
3. Ou acesse CloudWatch Logs diretamente

---

## 📝 Resumo dos IDs que Você Precisa Anotar

Durante o processo, anote:

- ✅ **VPC ID**: `vpc-xxxxx`
- ✅ **Subnet 1**: `subnet-xxxxx` (us-east-1a)
- ✅ **Subnet 2**: `subnet-yyyyy` (us-east-1b)
- ✅ **Security Group ID**: `sg-xxxxx`
- ✅ **ALB DNS**: `iscoolgpt-alb-xxxxx.us-east-1.elb.amazonaws.com`
- ✅ **Target Group ARN**: (aparece na lista de Target Groups)
- ✅ **Account ID**: `123456789012`

---

**Pronto! Sua infraestrutura está configurada! 🎉**

Agora, quando você fizer push para `main` ou `staging`, o GitHub Actions vai fazer deploy automaticamente!

