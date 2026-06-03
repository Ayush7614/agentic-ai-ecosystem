#!/usr/bin/env bash
# Quick health check for the Agentic RAG LitServe API.
set -euo pipefail

BASE="${RAG_API_URL:-http://127.0.0.1:8001}"
BASE="${BASE%/}"

if curl -sS -o /dev/null -w "%{http_code}" --max-time 5 \
  -X POST "${BASE}/predict" \
  -H 'Content-Type: application/json' \
  -d '{"query":"health"}' | grep -qE '^(200|422|400)$'; then
  echo "ok: RAG API reachable at ${BASE}"
  exit 0
fi

echo "fail: cannot reach RAG API at ${BASE}" >&2
exit 1
