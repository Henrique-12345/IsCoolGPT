# 🏗️ Como Criar Infraestrutura ECS - Guia Passo a Passo

Guia simplificado para criar a infraestrutura ECS na AWS.

## 📋 Pré-requisitos

- AWS CLI instalado e configurado
- Credenciais AWS configuradas
- Permissões IAM adequadas

## 🚀 Passo 1: Criar Clusters ECS

Execute no terminal:

```bash
# Criar cluster staging
aws ecs create-cluster \
    --cluster-name iscoolgpt-staging \
    --region us-east-1

# Criar cluster production
aws ecs create-cluster \
    --cluster-name iscoolgpt-production \
    --region us-east-1
```

Ou use o script:

```bash
bash scripts/criar-infraestrutura-ecs.sh
```

## 🌐 Passo 2: Configurar VPC e Networking

### 2.1 Obter VPC Default (mais fácil)

```bash
# Listar VPCs existentes
aws ec2 describe-vpcs --region us-east-1

# Anotar o VPC ID (geralmente começa com vpc-)
VPC_ID="vpc-xxxxxxxxx"
```

### 2.2 Obter Subnets Públicas

```bash
# Listar subnets públicas
aws ec2 describe-subnets \
    --filters "Name=vpc-id,Values=$VPC_ID" \
    --query 'Subnets[?MapPublicIpOnLaunch==`true`].[SubnetId,AvailabilityZone]' \
    --output table \
    --region us-east-1

# Anotar pelo menos 2 Subnet IDs de zonas diferentes
SUBNET_1="subnet-xxxxxxxxx"  # us-east-1a
SUBNET_2="subnet-yyyyyyyyy"  # us-east-1b
```

### 2.3 Criar Security Group

```bash
# Criar Security Group
SG_ID=$(aws ec2 create-security-group \
    --group-name iscoolgpt-sg \
    --description "Security group for IsCoolGPT API" \
    --vpc-id $VPC_ID \
    --region us-east-1 \
    --query 'GroupId' \
    --output text)

echo "Security Group ID: $SG_ID"

# Permitir tráfego HTTP na porta 8000
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 8000 \
    --cidr 0.0.0.0/0 \
    --region us-east-1
```

## ⚖️ Passo 3: Criar Application Load Balancer (ALB)

```bash
# Criar ALB
ALB_ARN=$(aws elbv2 create-load-balancer \
    --name iscoolgpt-alb \
    --subnets $SUBNET_1 $SUBNET_2 \
    --security-groups $SG_ID \
    --scheme internet-facing \
    --type application \
    --region us-east-1 \
    --query 'LoadBalancers[0].LoadBalancerArn' \
    --output text)

echo "ALB ARN: $ALB_ARN"

# Obter DNS do ALB
ALB_DNS=$(aws elbv2 describe-load-balancers \
    --load-balancer-arns $ALB_ARN \
    --region us-east-1 \
    --query 'LoadBalancers[0].DNSName' \
    --output text)

echo "ALB DNS: $ALB_DNS"
```

### 3.1 Criar Target Group

```bash
# Criar Target Group
TG_ARN=$(aws elbv2 create-target-group \
    --name iscoolgpt-tg \
    --protocol HTTP \
    --port 8000 \
    --vpc-id $VPC_ID \
    --target-type ip \
    --health-check-path /health \
    --region us-east-1 \
    --query 'TargetGroups[0].TargetGroupArn' \
    --output text)

echo "Target Group ARN: $TG_ARN"
```

### 3.2 Criar Listener

```bash
# Criar Listener HTTP
aws elbv2 create-listener \
    --load-balancer-arn $ALB_ARN \
    --protocol HTTP \
    --port 80 \
    --default-actions Type=forward,TargetGroupArn=$TG_ARN \
    --region us-east-1
```

## 📝 Passo 4: Preparar Task Definitions

### 4.1 Obter Account ID

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "Account ID: $ACCOUNT_ID"
```

### 4.2 Atualizar Task Definitions

Edite os arquivos `task-definition-staging.json` e `task-definition-production.json`:

- Substitua `ACCOUNT_ID` pelo seu Account ID real
- Verifique se o ARN do secret está correto

### 4.3 Registrar Task Definitions

```bash
# Registrar task definition staging
aws ecs register-task-definition \
    --cli-input-json file://task-definition-staging.json \
    --region us-east-1

# Registrar task definition production
aws ecs register-task-definition \
    --cli-input-json file://task-definition-production.json \
    --region us-east-1
```

## 🚀 Passo 5: Criar ECS Services

### 5.1 Criar Service Staging

```bash
aws ecs create-service \
    --cluster iscoolgpt-staging \
    --service-name iscoolgpt-api-staging \
    --task-definition iscoolgpt-staging:1 \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_1,$SUBNET_2],securityGroups=[$SG_ID],assignPublicIp=ENABLED}" \
    --load-balancers "targetGroupArn=$TG_ARN,containerName=iscoolgpt-api,containerPort=8000" \
    --region us-east-1
```

### 5.2 Criar Service Production

```bash
aws ecs create-service \
    --cluster iscoolgpt-production \
    --service-name iscoolgpt-api-production \
    --task-definition iscoolgpt-production:1 \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_1,$SUBNET_2],securityGroups=[$SG_ID],assignPublicIp=ENABLED}" \
    --load-balancers "targetGroupArn=$TG_ARN,containerName=iscoolgpt-api,containerPort=8000" \
    --region us-east-1
```

## ✅ Verificar Status

```bash
# Verificar serviços
aws ecs describe-services \
    --cluster iscoolgpt-staging \
    --services iscoolgpt-api-staging \
    --region us-east-1

# Verificar tasks
aws ecs list-tasks \
    --cluster iscoolgpt-staging \
    --region us-east-1
```

## 🌐 Acessar a API

Depois que o serviço estiver rodando, acesse:

```
http://$ALB_DNS/api/v1/health
```

## 🆘 Troubleshooting

### Service não inicia

```bash
# Ver eventos do serviço
aws ecs describe-services \
    --cluster iscoolgpt-staging \
    --services iscoolgpt-api-staging \
    --region us-east-1 \
    --query 'services[0].events[:5]'
```

### Ver logs

```bash
# Ver logs no CloudWatch
aws logs tail /ecs/iscoolgpt-staging --follow --region us-east-1
```

## 📚 Próximos Passos

1. ✅ Configure domínio personalizado (opcional)
2. ✅ Configure HTTPS/SSL (opcional)
3. ✅ Configure auto-scaling
4. ✅ Configure monitoramento avançado

---

**Dica**: Salve todos os IDs (VPC, Subnets, Security Group, ALB, Target Group) em um arquivo para referência futura!

