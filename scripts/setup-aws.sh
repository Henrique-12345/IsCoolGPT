#!/bin/bash
# Script para configuração inicial da infraestrutura AWS

set -e

echo "🚀 Configurando infraestrutura AWS para IsCoolGPT..."

# Variáveis (ajustar conforme necessário)
REGION="us-east-1"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPO_NAME="iscoolgpt"

echo "📦 Criando repositório ECR..."
aws ecr create-repository \
    --repository-name $REPO_NAME \
    --image-scanning-configuration scanOnPush=true \
    --region $REGION \
    || echo "Repositório ECR já existe"

echo "📝 Criando repositório CodeCommit..."
aws codecommit create-repository \
    --repository-name $REPO_NAME \
    --repository-description "Repositório do projeto IsCoolGPT" \
    --region $REGION \
    || echo "Repositório CodeCommit já existe"

echo "🔐 Criando secret no Secrets Manager..."
aws secretsmanager create-secret \
    --name iscoolgpt/openai-api-key \
    --secret-string "CHANGE_ME" \
    --region $REGION \
    || echo "Secret já existe (atualize manualmente com: aws secretsmanager put-secret-value --secret-id iscoolgpt/openai-api-key --secret-string 'sua-chave-aqui')"

echo "📊 Criando Log Groups..."
aws logs create-log-group --log-group-name /ecs/iscoolgpt-staging --region $REGION || echo "Log group staging já existe"
aws logs create-log-group --log-group-name /ecs/iscoolgpt-production --region $REGION || echo "Log group production já existe"

echo "✅ Configuração inicial concluída!"
echo ""
echo "Próximos passos:"
echo "1. Configure o secret da OpenAI: aws secretsmanager put-secret-value --secret-id iscoolgpt/openai-api-key --secret-string 'sua-chave'"
echo "2. Crie os clusters ECS: aws ecs create-cluster --cluster-name iscoolgpt-staging"
echo "3. Configure VPC, Security Groups e ALB"
echo "4. Crie as Task Definitions e Services"

