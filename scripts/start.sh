#!/bin/bash
# MentorBoxAI - Local Development Startup Script

set -e

echo "🚀 Starting MentorBoxAI..."

# Load .env if it exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
    echo "✅ Loaded .env"
else
    echo "⚠️  .env not found. Copy .env.example to .env and fill in values."
    exit 1
fi

# Ping Groq keys before starting
echo "🔑 Validating Groq API keys..."
python bedrock_ping_test.py

# Start FastAPI
echo "🌐 Starting FastAPI server on port ${PORT:-8000}..."
uvicorn src.app.main:app --host 0.0.0.0 --port ${PORT:-8000} --reload
