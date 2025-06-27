#!/bin/sh
echo "Starting Cognitive Memory System..."
echo "Port: $PORT"
python -m uvicorn main:app --host 0.0.0.0 --port $PORT