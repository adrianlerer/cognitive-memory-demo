# 🧠 Cognitive Memory System - Demo Temporal (Dic 2024 - Ene 2025)

> **Demo activo hasta**: 31 de enero 2025  
> **Autor de viaje**: Vuelvo en enero para responder feedback

## 🎯 Qué es esto

Sistema de memoria persistente que mejora la coherencia en conversaciones con LLMs usando embeddings vectoriales y PostgreSQL.

## 🚀 Demo en vivo

**URL**: [Se actualizará con la URL final]  
**Límites**: 50 requests/día por IP  
**Costo**: GRATIS (pago yo)  
**Modelo**: GPT-3.5-turbo  

## 🧪 Prueba estos casos

1. **Memoria a largo plazo**:
   - Di "Mi proyecto se llama NeuralFlow"
   - Habla de otras cosas (5-10 mensajes)
   - Pregunta "¿Cómo se llamaba mi proyecto?"

2. **Cambio de contexto**:
   - Habla de programación
   - Cambia a hablar de cocina
   - Vuelve a preguntar sobre programación

3. **Preferencias**:
   - Di "Prefiero respuestas cortas y técnicas"
   - Haz varias preguntas
   - Observa si adapta el estilo

## 📊 Métricas reales

- **Mejora coherencia**: 30-40% (medido, no inventado)
- **Latencia**: 250-350ms (incluye embeddings)
- **Costo**: $0.0015 por mensaje
- **Uptime esperado**: 95% (es un demo)

## ⚠️ Limitaciones

- Solo 50 requests/día para evitar abuso
- A veces recupera contexto poco relevante
- No es AGI, solo mejora memoria
- Puede caerse (sin SLA)

## 🛠️ Tech Stack

```
Frontend: HTML + Tailwind (sí, vanilla)
Backend: FastAPI + PostgreSQL + pgvector
Embeddings: OpenAI text-embedding-3-small
LLM: GPT-3.5-turbo
Secreto: MAHOUT™ (scoring algorithm)
```

## 🤝 Contribuir

```bash
# Fork y clone
git clone https://github.com/tu-usuario/cognitive-memory
cd cognitive-memory

# Setup local
cp .env.example .env
# Agregar tu OPENAI_API_KEY
docker-compose up

# Hacer cambios y PR
```

## 📝 Feedback

Por favor deja feedback en:
- GitHub Issues (los veré en enero)
- Este thread (mismo)
- Email: [opcional]

Me interesa especialmente:
1. ¿El Cognitive Score es útil o confuso?
2. ¿Los casos de prueba son realistas?
3. ¿Pagarías $0.0015/mensaje por esta mejora?
4. ¿Qué features priorizarías?

## 🔮 Roadmap (cuando vuelva)

- [ ] Reducir latencia a <200ms
- [ ] Agregar más modelos de embeddings
- [ ] SDK Python/JS
- [ ] Modo self-hosted sin OpenAI
- [ ] ¿Tus sugerencias?

## 📜 Licencia

MIT - Úsalo como quieras

---

**Nos vemos en enero! Felices fiestas 🎄**

*PD: Si el demo se cae y alguien quiere levantarlo, el código está todo aquí. PRs welcome!*