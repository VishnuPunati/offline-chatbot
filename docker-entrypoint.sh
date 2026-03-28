#!/bin/sh
set -eu

OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-http://ollama:11434}"
OLLAMA_MODEL="${OLLAMA_MODEL:-llama3.2:3b}"

echo "Waiting for Ollama at ${OLLAMA_BASE_URL}..."
until wget -q -O - "${OLLAMA_BASE_URL}/api/tags" >/dev/null 2>&1; do
  sleep 2
done

echo "Ensuring model ${OLLAMA_MODEL} is available..."
wget -q -O - \
  --header="Content-Type: application/json" \
  --post-data="{\"name\":\"${OLLAMA_MODEL}\"}" \
  "${OLLAMA_BASE_URL}/api/pull" >/dev/null 2>&1 || true

echo "Running chatbot evaluation..."
python /app/chatbot.py
