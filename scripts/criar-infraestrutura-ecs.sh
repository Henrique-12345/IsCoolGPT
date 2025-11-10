#!/bin/bash
# Script para criar infraestrutura ECS básica
# Execute: bash scripts/criar-infraestrutura-ecs.sh

set -e

REGION="us-east-1"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "🚀 Criando infraestrutura ECS para IsCoolGPT..."
echo ""

# 1. Criar clusters ECS
echo "📦 Criando clusters ECS..."
aws ecs create-cluster \
    --cluster-name iscoolgpt-staging \
    --region $REGION \
    || echo "Cluster staging já existe"

aws ecs create-cluster \
    --cluster-name iscoolgpt-production \
    --region $REGION \
    || echo "Cluster production já existe"

echo "✅ Clusters criados!"
echo ""

# 2. Obter URI do ECR
ECR_URI="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/iscoolgpt"
echo "📦 URI do ECR: $ECR_URI"
echo ""

echo "✅ Infraestrutura básica criada!"
echo ""
echo "⚠️  PRÓXIMOS PASSOS MANUAIS:"
echo ""
echo "1. Configure VPC e Networking:"
echo "   - Crie ou use uma VPC existente"
echo "   - Crie subnets públicas em pelo menos 2 AZs"
echo "   - Configure Internet Gateway e Route Tables"
echo ""
echo "2. Crie Security Group:"
echo "   - Permita tráfego HTTP na porta 8000"
echo ""
echo "3. Crie Application Load Balancer (ALB):"
echo "   - Configure Target Group apontando para porta 8000"
echo ""
echo "4. Crie Task Definitions:"
echo "   - Use os arquivos: task-definition-staging.json e task-definition-production.json"
echo "   - Ajuste ACCOUNT_ID nos arquivos antes de registrar"
echo ""
echo "5. Crie ECS Services:"
echo "   - Configure para usar Fargate"
echo "   - Conecte ao ALB"
echo ""
echo "📚 Consulte GUIA_PASSO_A_PASSO.md para detalhes completos"

