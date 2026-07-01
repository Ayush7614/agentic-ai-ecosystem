#!/usr/bin/env bash
# 16 GB laptop — balanced chat, vision, coding, embeddings
set -euo pipefail

echo "=== Ollama 16 GB pack ==="
ollama pull qwen3.5:4b
ollama pull gemma4:e2b
ollama pull minicpm-v4.6
ollama pull north-mini-code-1.0
ollama pull glm-4.7-flash
ollama pull nomic-embed-text

echo ""
echo "Done. Try:"
echo "  ollama run gemma4:e2b"
echo "  ollama run north-mini-code-1.0"
