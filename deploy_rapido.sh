#!/bin/bash
# Deploy rápido para comunidad dev - 15 minutos máximo

echo "🚀 Deploy Rápido - Cognitive Memory System"
echo "========================================="
echo ""

# Check if railway is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Instalando Railway CLI..."
    npm install -g @railway/cli
fi

echo "🔐 Necesitas:"
echo "1. Una cuenta en Railway (gratis)"
echo "2. Tu OPENAI_API_KEY con límite de $10"
echo ""
echo "Presiona Enter cuando tengas ambas cosas..."
read

# Login to Railway
echo "🚂 Conectando con Railway..."
railway login

# Initialize project
echo "📁 Inicializando proyecto..."
railway init cognitive-memory-demo

# Deploy
echo "🚀 Desplegando (esto toma ~5 min)..."
railway up

# Add PostgreSQL
echo "🗄️ Agregando PostgreSQL..."
railway add

# Set environment variables
echo "🔧 Configurando variables..."
echo "Pega tu OPENAI_API_KEY:"
read OPENAI_KEY

railway variables set OPENAI_API_KEY=$OPENAI_KEY
railway variables set MAX_REQUESTS_PER_IP_DAY=50
railway variables set DEMO_EXPIRES=2025-07-31
railway variables set ENVIRONMENT=demo

# Get URL
echo "✅ Obteniendo URL..."
railway open

echo ""
echo "🎉 LISTO!"
echo ""
echo "📋 Para compartir con la comunidad:"
echo "1. Copia la URL de Railway"
echo "2. Usa este mensaje:"
echo ""
cat << 'EOF'
Gente, el abogado dev aquí 😅

Antes de irme de viaje: sistema de memoria para LLMs que mejora coherencia ~35%

Demo: [TU_URL_RAILWAY]
Límite: 50 req/día
Código: github.com/tu-user/cognitive-memory

¿Feedback? ¿Lo usarían para algo?

Vuelvo fin de julio 🛫
EOF
echo ""
echo "3. Pega en el grupo y VETE DE VIAJE!"