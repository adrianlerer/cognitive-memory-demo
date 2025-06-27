# Cognitive Memory System for LLMs

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MAHOUT™: Proprietary](https://img.shields.io/badge/MAHOUT™-Proprietary-red.svg)](LEGAL_NOTICE.md)

Sistema de memoria persistente para IA conversacional con análisis cognitivo avanzado.

## ⚖️ IMPORTANT LEGAL NOTICE

**This repository contains INTERFACES to proprietary MAHOUT™ technology. The actual MAHOUT™ algorithms are NOT included and are protected by trade secret and patent law. See [LEGAL_NOTICE.md](LEGAL_NOTICE.md) for details.**

## 🎯 What This Repository Contains

### ✅ Open Source (MIT License)
- FastAPI application wrapper
- PostgreSQL + pgvector integration  
- Web interface for testing
- Docker deployment configuration
- API endpoint definitions
- Basic demo scoring (NOT real MAHOUT™)

### ❌ NOT Included (Proprietary)
- MAHOUT™ cognitive analysis algorithms
- Neural pattern matching implementation
- Temporal decay calculations
- Production scoring methodologies
- Any proprietary IntegridAI technology

## 🚀 Features

- **Persistent Memory**: PostgreSQL with pgvector for semantic search
- **MAHOUT™ Integration**: Interface to proprietary cognitive analysis (requires license)
- **Real-time Analysis**: Sub-300ms response times
- **Semantic Search**: Find relevant past conversations
- **RESTful API**: Easy integration with any LLM

## 📋 Requirements

- Python 3.9+
- PostgreSQL 14+ with pgvector extension
- OpenAI API key (for embeddings)
- MAHOUT™ API license (for production scoring)

## 🛠️ Installation

### Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/cognitive-memory-demo.git
cd cognitive-memory-demo

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://localhost/cognitive_memory"
export OPENAI_API_KEY="your-openai-key"
export MAHOUT_API_KEY="demo-key"  # Request production key from IntegridAI

# Run application
python main.py
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Initialize database
docker-compose exec web python -c "from main import init_db; import asyncio; asyncio.run(init_db())"
```

## 📡 API Endpoints

### Chat Endpoint
```http
POST /api/chat
X-API-Key: your-api-key

{
  "conversation_id": "uuid",
  "message": "Hello, how are you?",
  "max_contexts": 10
}
```

### Search Endpoint  
```http
POST /api/search
X-API-Key: your-api-key

{
  "query": "previous discussions about Python",
  "conversation_id": "uuid",  # Optional
  "limit": 10
}
```

## 💰 MAHOUT™ Licensing

The demo includes basic scoring. For production use with real MAHOUT™ analysis:

- **Demo**: Limited functionality, basic scoring
- **Startup**: $299/month - 100K requests
- **Enterprise**: Custom pricing - unlimited requests

Contact sales@integridai.com for licensing.

## 🔒 Security Considerations

- Always use environment variables for sensitive data
- Implement rate limiting in production
- Use HTTPS for all API communications
- Rotate API keys regularly
- Monitor for unauthorized access attempts

## ⚖️ Legal

- Open source components: MIT License
- MAHOUT™ technology: Proprietary (see [LEGAL_NOTICE.md](LEGAL_NOTICE.md))
- Patents pending (6 applications filed)
- © 2025 IntegridAI. All rights reserved.

## 🤝 Contributing

We welcome contributions to the open source components! Please:

1. Read [LEGAL_NOTICE.md](LEGAL_NOTICE.md) first
2. Only contribute to open source parts
3. Don't attempt to reverse engineer MAHOUT™
4. Sign CLA before major contributions

## 📧 Contact

- Technical Support: support@integridai.com
- Licensing: sales@integridai.com
- Legal: legal@integridai.com
- Security: security@integridai.com

---

**Remember**: This is a demonstration of integration capabilities. The real MAHOUT™ technology that provides advanced cognitive analysis is proprietary and requires a commercial license.
