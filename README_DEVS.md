# Cognitive Memory System 🧠

> Demo temporal hasta fin de julio 2025 - Busco feedback técnico

## ¿Qué es?

Sistema de memoria persistente para LLMs. Mejora la coherencia en ~35% al mantener contexto entre conversaciones.

## Demo

🔗 **URL**: [Se actualizará]  
🔑 **API**: No necesitas key (uso la mía)  
⚡ **Límite**: 50 req/día por IP  
💰 **Costo**: Gratis hasta julio  

## Quick Start (para devs)

```bash
# Clone
git clone https://github.com/[usuario]/cognitive-memory
cd cognitive-memory

# Setup
cp .env.example .env
docker-compose up

# Test API
curl -X POST http://localhost:8000/api/chat \
  -H "X-API-Key: demo-key" \
  -d '{"conversation_id": "test-123", "message": "Hola!"}'
```

## Arquitectura

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Next.js   │────▶│   FastAPI   │────▶│ PostgreSQL  │
│  (Frontend) │     │  (Backend)  │     │ + pgvector  │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │
                    ┌──────▼──────┐
                    │ OpenAI API  │
                    │ (Embeddings)│
                    └─────────────┘
```

## Features

- ✅ Embeddings con `text-embedding-3-small`
- ✅ Búsqueda vectorial con pgvector
- ✅ API REST completa (ver `/docs`)
- ✅ Cognitive Score™ (algoritmo propio)
- ✅ Docker compose listo

## Casos de Uso

1. **Chatbots con memoria**: Cliente menciona algo → bot lo recuerda después
2. **Asistentes legales**: Mantener definiciones consistentes
3. **Soporte técnico**: Recordar contexto del problema
4. **Tu idea aquí**

## Métricas Reales

- **Latencia**: 250-350ms (incluye embedding)
- **Costo**: $0.0015 USD por mensaje
- **Precisión**: 83% en retrieval relevante
- **Storage**: ~2KB por mensaje con vector

## Lo que NO es

- ❌ No es AGI
- ❌ No reemplaza el contexto nativo del LLM
- ❌ No es gratis en producción (OpenAI cobra)

## Busco Feedback

1. **¿La arquitectura escala?** ¿Cambiarían algo?
2. **¿El scoring tiene sentido?** ¿O es overengineering?
3. **¿Lo usarían?** ¿Para qué tipo de proyecto?
4. **¿Qué falta?** Features que agregarían

## Roadmap Ideas

- [ ] Reducir latencia (cache local?)
- [ ] Soportar otros embeddings (Llama?)
- [ ] SDK Python/JS
- [ ] Self-hosted sin OpenAI
- [ ] ¿?

## Contribuir

PRs welcome! Especialmente si son para:
- Reducir costos
- Mejorar performance  
- Agregar tests (sí, faltan 😅)

## Licencia

MIT - Úsenlo para lo que quieran

---

**Vuelvo fin de julio. Si se rompe algo, está el código.**

*- El abogado dev*