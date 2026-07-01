#!/usr/bin/env bash
# 8 GB laptop — minimal Ollama stack (chat + vision + embeddings)
set -euo pipefail

echo "=== Ollama 8 GB pack ==="
ollama pull qwen3.5:0.8b
ollama pull lfm2.5-thinking:1.2b
ollama pull minicpm-v4.6
ollama pull nomic-embed-text

echo ""
echo "Done. Try:"
echo "  ollama run qwen3.5:0.8b"
echo "  ollama run minicpm-v4.6"
