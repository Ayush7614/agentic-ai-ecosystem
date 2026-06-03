#!/usr/bin/env bash
# Local smoke test: Gemma in Ollama + RAG API + agentic-rag scripts.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$ROOT/../.." && pwd)"
RAG_DIR="${REPO}/guides/qwen-agentic-rag"
export RAG_API_URL="${RAG_API_URL:-http://127.0.0.1:8001}"

echo "==> 1. Check gemma4:e2b in Ollama"
if ! ollama list | grep -q 'gemma4:e2b'; then
  echo "Pulling gemma4:e2b (~7.2GB)..."
  ollama pull gemma4:e2b
fi
ollama run gemma4:e2b "Say OK in two words." --nowordwrap 2>/dev/null | head -3

echo "==> 2. RAG .env (Gemma crew model)"
if [[ ! -f "${RAG_DIR}/.env" ]]; then
  cp "${ROOT}/env.rag.example" "${RAG_DIR}/.env"
  echo "Created ${RAG_DIR}/.env"
fi
grep OLLAMA_MODEL "${RAG_DIR}/.env" || true

echo "==> 3. RAG API health"
if ! "${ROOT}/skills/agentic-rag/scripts/rag_health.sh"; then
  echo "Start RAG in another terminal:"
  echo "  cd ${RAG_DIR} && source .venv/bin/activate && python server.py"
  exit 1
fi

echo "==> 4. RAG query via skill script"
"${ROOT}/skills/agentic-rag/scripts/rag_query.sh" "What is cross-validation? Answer in 2 sentences."

echo "==> 5. OpenClaw (optional)"
if command -v openclaw >/dev/null 2>&1; then
  export OLLAMA_API_KEY="${OLLAMA_API_KEY:-ollama-local}"
  openclaw models set ollama/gemma4:e2b 2>/dev/null || true
  echo "Run: openclaw agent --message 'Use agentic RAG: what is overfitting?' --thinking low"
else
  echo "OpenClaw not installed; skip step 5."
fi

echo "Done."
