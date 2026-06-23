#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
export VISION_API_URL="${VISION_API_URL:-http://127.0.0.1:8002}"

echo "==> 1. MiniCPM-V 4.6 in Ollama"
if ! ollama list 2>/dev/null | grep -q 'minicpm-v4.6'; then
  echo "Pulling minicpm-v4.6 (~1.6GB)..."
  ollama pull minicpm-v4.6
fi

echo "==> 2. Sample image"
if [[ ! -f "${ROOT}/samples/receipt.png" ]]; then
  python3 "${ROOT}/generate_sample.py"
fi

echo "==> 3. Vision API health"
CODE="$("${ROOT}/skills/vision-photo/scripts/vision_health.sh" || true)"
if [[ "$CODE" != "200" ]]; then
  echo "Start vision_server.py in another terminal:"
  echo "  cd ${ROOT} && source .venv/bin/activate && python vision_server.py"
  exit 1
fi

echo "==> 4. Vision query via skill"
"${ROOT}/skills/vision-photo/scripts/vision_query.sh" \
  "${ROOT}/samples/receipt.png" "What is the total on this receipt?"

echo "Done."
