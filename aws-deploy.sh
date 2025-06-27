#!/bin/bash

# AWS Quick Deploy Script for Cognitive Memory System
# Ejecutar desde AWS CloudShell o local con AWS CLI configurado

echo "🚀 Deploying Cognitive Memory System to AWS"
echo "=========================================="

# Variables
REGION="us-east-1"
PROJECT_NAME="cognitive-memory"
DOMAIN="demo.mahout.ai"

# 1. Crear ECR Repository para Docker
echo "📦 Creating ECR Repository..."
aws ecr create-repository \
    --repository-name $PROJECT_NAME \
    --region $REGION

# 2. Obtener URL del repositorio
ECR_URL=$(aws ecr describe-repositories \
    --repository-names $PROJECT_NAME \
    --region $REGION \
    --query 'repositories[0].repositoryUri' \
    --output text)

echo "ECR URL: $ECR_URL"

# 3. Login a ECR
echo "🔐 Logging into ECR..."
aws ecr get-login-password --region $REGION | \
    docker login --username AWS --password-stdin $ECR_URL

# 4. Build y Push Docker Image
echo "🏗️ Building Docker image..."
docker build -t $PROJECT_NAME .
docker tag $PROJECT_NAME:latest $ECR_URL:latest
docker push $ECR_URL:latest

# 5. Crear Task Definition
echo "📋 Creating ECS Task Definition..."
cat > task-definition.json << EOF
{
  "family": "$PROJECT_NAME",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [{
    "name": "api",
    "image": "$ECR_URL:latest",
    "portMappings": [{
      "containerPort": 8000,
      "protocol": "tcp"
    }],
    "essential": true,
    "environment": [
      {"name": "DATABASE_URL", "value": "TO_BE_UPDATED"},
      {"name": "LLM_API_ENDPOINT", "value": "TO_BE_UPDATED"},
      {"name": "MAHOUT_ENABLED", "value": "true"}
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/$PROJECT_NAME",
        "awslogs-region": "$REGION",
        "awslogs-stream-prefix": "ecs"
      }
    }
  }]
}
EOF

aws ecs register-task-definition \
    --cli-input-json file://task-definition.json \
    --region $REGION

# 6. Crear S3 Bucket para Frontend
echo "🪣 Creating S3 Bucket..."
aws s3 mb s3://$PROJECT_NAME-frontend-$RANDOM \
    --region $REGION

# 7. Subir Frontend
echo "⬆️ Uploading frontend..."
aws s3 cp index.html s3://$PROJECT_NAME-frontend/ \
    --content-type "text/html"

echo "✅ Infrastructure created!"
echo ""
echo "Next steps:"
echo "1. Create RDS PostgreSQL instance with pgvector"
echo "2. Update Task Definition with database URL"
echo "3. Create ECS Service"
echo "4. Configure CloudFront distribution"
echo "5. Set up Route 53 for $DOMAIN"
