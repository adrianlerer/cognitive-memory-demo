#!/bin/sh
echo "Starting Cognitive Memory System..."
echo "Installing dependencies..."
pip install openai tiktoken tenacity fastapi uvicorn asyncpg numpy pydantic python-multipart httpx python-dotenv
echo "Dependencies installed. Starting server..."
python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}