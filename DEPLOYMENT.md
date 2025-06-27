# Deployment Guide - Cognitive Memory SaaS MVP

## Arquitectura de Deployment

```
                    ┌─────────────────┐
                    │   Cloudflare    │
                    │  (CDN + WAF)    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   Load Balancer │
                    │   (AWS ALB)     │
                    └────────┬────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
        ┌───────▼────────┐     ┌─────────▼────────┐
        │  API Server 1  │     │  API Server 2    │
        │  (ECS Fargate) │     │  (ECS Fargate)   │
        └───────┬────────┘     └─────────┬────────┘
                │                         │
                └───────────┬─────────────┘
                            │
                  ┌─────────▼──────────┐
                  │   PostgreSQL RDS   │
                  │   with pgvector    │
                  └────────────────────┘
```

## Opción 1: AWS ECS Deployment (Recomendado)

### 1. Preparar Imagen Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health')"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Configurar RDS PostgreSQL

```sql
-- Conectar como admin y ejecutar:
CREATE EXTENSION IF NOT EXISTS vector;

-- Crear usuario para aplicación
CREATE USER cognitive_app WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE cognitive_memory TO cognitive_app;
```

### 3. Task Definition ECS

```json
{
  "family": "cognitive-memory-saas",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "your-ecr-repo/cognitive-memory:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:db-url"
        },
        {
          "name": "LLM_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:llm-key"
        },
        {
          "name": "EMBEDDING_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:embed-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/cognitive-memory",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "api"
        }
      }
    }
  ]
}
```

## Opción 2: Heroku Deployment (Más Simple)

### 1. Procfile
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 2. runtime.txt
```
python-3.11.6
```

### 3. Deploy Commands
```bash
# Login to Heroku
heroku login

# Create app
heroku create cognitive-memory-saas

# Add PostgreSQL with pgvector
heroku addons:create heroku-postgresql:standard-0
heroku pg:psql < setup_database.sql

# Set environment variables
heroku config:set LLM_API_ENDPOINT=https://api.provider.com/v1/chat
heroku config:set LLM_API_KEY=your-key
heroku config:set EMBEDDING_API_ENDPOINT=https://api.provider.com/v1/embeddings
heroku config:set EMBEDDING_API_KEY=your-key
heroku config:set MAHOUT_ENABLED=true

# Deploy
git push heroku main
```

## Configuración de Seguridad

### 1. API Keys para Clientes

```python
# Generar API keys seguras
import secrets

def generate_api_key():
    return f"cms_{secrets.token_urlsafe(32)}"

# Ejemplo: cms_KJ3nX9pQ2mZvY8wR5tN7sF4hG6dL1aB0
```

### 2. Rate Limiting

```nginx
# nginx.conf
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

server {
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://backend;
    }
}
```

### 3. CORS Configuration

```python
# En producción, especificar dominios exactos
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://app.yourdomain.com",
        "https://yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)
```

## Monitoreo y Logging

### 1. CloudWatch Metrics
```python
# Métricas custom
import boto3
cloudwatch = boto3.client('cloudwatch')

def log_metric(metric_name, value, unit='Count'):
    cloudwatch.put_metric_data(
        Namespace='CognitiveMemory',
        MetricData=[
            {
                'MetricName': metric_name,
                'Value': value,
                'Unit': unit
            }
        ]
    )
```

### 2. Alarmas Críticas
- Response time > 2 segundos
- Error rate > 5%
- Database connections > 80%
- Memory usage > 90%

## Costos Estimados AWS

| Componente | Especificaciones | Costo/Mes |
|------------|------------------|-----------|
| ECS Fargate | 2x (0.5 vCPU, 1GB) | $36 |
| RDS PostgreSQL | db.t3.small + 100GB | $85 |
| ALB | 1 ALB + tráfico | $25 |
| CloudWatch | Logs + Metrics | $20 |
| Secrets Manager | 5 secrets | $2 |
| **Total** | | **~$168** |

## Checklist de Producción

- [ ] Variables de entorno configuradas en Secrets Manager
- [ ] PostgreSQL con pgvector extension instalada
- [ ] SSL/TLS configurado (ACM certificate)
- [ ] Backups automáticos de RDS activados
- [ ] Monitoreo CloudWatch configurado
- [ ] Rate limiting implementado
- [ ] Health checks funcionando
- [ ] Logs centralizados
- [ ] Alarmas configuradas
- [ ] Documentación API actualizada

## Comandos Útiles

```bash
# Ver logs en tiempo real
aws logs tail /ecs/cognitive-memory --follow

# Escalar servicio
aws ecs update-service --cluster prod --service cognitive-memory --desired-count 3

# Backup manual de DB
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Test de carga
artillery quick --count 50 --num 100 https://api.yourdomain.com/health
```

---

**IMPORTANTE**: Nunca commits las API keys reales. Usar siempre Secrets Manager o variables de entorno.
