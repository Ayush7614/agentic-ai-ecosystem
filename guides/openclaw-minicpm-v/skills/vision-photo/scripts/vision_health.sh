#!/usr/bin/env bash
set -euo pipefail
BASE="${VISION_API_URL:-http://127.0.0.1:8002}"
BASE="${BASE%/}"
curl -sS -o /dev/null -w "%{http_code}" -X POST "${BASE}/predict" \
  -H 'Content-Type: application/json' \
  -d '{"query":"ping","image_path":"/tmp/nonexistent.png"}' 2>/dev/null || echo "000"
