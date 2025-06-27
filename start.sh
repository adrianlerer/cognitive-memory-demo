#!/bin/bash
echo "Starting Cognitive Memory System..."
echo "Port: $PORT"
echo "Copyright (c) 2025 IntegridAI. MAHOUT™ is a registered trademark."
python -m uvicorn main:app --host 0.0.0.0 --port $PORT