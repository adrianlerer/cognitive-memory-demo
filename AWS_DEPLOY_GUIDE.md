# 🚀 OPCIÓN SIMPLIFICADA: AWS Elastic Beanstalk

## Para Deploy Rápido (5 minutos)

### 1. Preparar aplicación para Beanstalk

```bash
# En tu directorio local
cd /Users/adria1/Downloads/cognitive-memory-saas/

# Crear archivo de configuración Beanstalk
mkdir .ebextensions
```

### 2. Crear configuración

```yaml
# .ebextensions/01_python.config
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: main.py
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: "/var/app/current:$PYTHONPATH"
    PORT: 8000
```

### 3. Deploy con EB CLI

```bash
# Instalar EB CLI
pip install awsebcli

# Inicializar
eb init -p python-3.11 cognitive-memory-app --region us-east-1

# Crear environment
eb create cognitive-memory-env

# Deploy
eb deploy
```

## 💰 COSTOS FINALES PARA TU PRUEBA

### Escenario: 3 productos gratis, 100 developers

#### Infraestructura AWS (por mes)
- **Elastic Beanstalk** (t3.micro): $8.50
- **RDS PostgreSQL** (db.t3.micro): $15
- **Route 53**: $0.50
- **Total Infra**: **$24/mes**

#### APIs Externas (por uso)
Asumiendo 100 devs × 10 chats/día × 30 días = 30,000 interacciones

- **LLM (Claude/GPT)**: ~$300
- **Embeddings**: ~$4
- **Total APIs**: **$304/mes**

### 🎯 COSTO TOTAL: ~$328/mes

### Para reducir costos en la prueba:

1. **Límite por developer**: 100 interacciones gratis
2. **Total máximo**: 300 productos (3 × 100 devs)
3. **Costo máximo APIs**: ~$40

**COSTO PRUEBA LIMITADA: ~$64 primer mes**

## 🔧 CONFIGURACIÓN DE DOMINIO

### Opción A: Subdominio en Route 53
```
demo.mahout.ai → CloudFront → Beanstalk
api.mahout.ai → ALB → Beanstalk
```

### Opción B: Path-based
```
mahout.ai/demo → Frontend
mahout.ai/api → Backend
```

## 📊 DASHBOARD DE CONTROL DE COSTOS

```python
# Agregar a main.py
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Límite por API key
    api_key = request.headers.get("X-API-Key")
    
    # Check en Redis
    usage = await redis_client.get(f"usage:{api_key}")
    if usage and int(usage) > 100:  # 100 calls límite
        return JSONResponse(
            status_code=429,
            content={"error": "Free tier limit reached"}
        )
    
    # Incrementar contador
    await redis_client.incr(f"usage:{api_key}")
    await redis_client.expire(f"usage:{api_key}", 2592000)  # 30 días
    
    response = await call_next(request)
    return response
```

## 🎁 ESTRATEGIA PARA DEVELOPERS

### Landing Page
```
🚀 Prueba GRATIS Cognitive Memory System
Powered by MAHOUT™

✅ 100 interacciones gratis
✅ Sin tarjeta de crédito
✅ SDK en Python/JS
✅ Documentación completa

[Get API Key] → Instantly
```

### Onboarding Flow
1. Developer entra email
2. Recibe API key instant
3. Copia código ejemplo
4. Primera llamada en <1 min

## COMANDOS PARA EMPEZAR YA

```bash
# Desde tu Mac
cd /Users/adria1/Downloads/cognitive-memory-saas/

# Opción 1: Elastic Beanstalk (más fácil)
eb init
eb create
eb open

# Opción 2: ECS (más control)
chmod +x aws-deploy.sh
./aws-deploy.sh
```

---

**RESUMEN DE COSTOS**:
- **Prueba limitada (100 devs, 100 calls c/u)**: ~$64
- **Producción pequeña (1K usuarios)**: ~$328/mes
- **Free tier AWS**: Primeros 12 meses con descuentos

¿Procedemos con Elastic Beanstalk para empezar rápido?
