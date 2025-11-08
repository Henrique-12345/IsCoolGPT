#!/bin/bash
# Script para criar clusters ECS

set -e

REGION="us-east-1"

echo "🏗️ Criando clusters ECS..."

echo "📦 Criando cluster staging..."
aws ecs create-cluster \
    --cluster-name iscoolgpt-staging \
    --region $REGION \
    || echo "Cluster staging já existe"

echo "📦 Criando cluster production..."
aws ecs create-cluster \
    --cluster-name iscoolgpt-production \
    --region $REGION \
    || echo "Cluster production já existe"

echo "✅ Clusters criados com sucesso!"

