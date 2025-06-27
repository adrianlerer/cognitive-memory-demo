#!/bin/sh
echo "Starting Cognitive Memory System..."
echo "Port: ${PORT:-8000}"
echo "Database URL configured: ${DATABASE_URL:0:30}..."
python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}