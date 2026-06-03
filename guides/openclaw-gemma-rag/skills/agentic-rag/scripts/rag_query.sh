#!/usr/bin/env bash
# POST a query to the local Agentic RAG LitServe API and print the answer.
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: rag_query.sh \"your question\"" >&2
  exit 1
fi

QUERY="$1"
BASE="${RAG_API_URL:-http://127.0.0.1:8001}"
BASE="${BASE%/}"

if ! command -v curl >/dev/null 2>&1; then
  echo "curl is required" >&2
  exit 1
fi
if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required" >&2
  exit 1
fi

BODY="$(jq -n --arg q "$QUERY" '{query: $q}')"

RESPONSE="$(curl -sS -X POST "${BASE}/predict" \
  -H 'Content-Type: application/json' \
  -d "$BODY" \
  --max-time 600 \
  -w '\n%{http_code}')"

HTTP_CODE="${RESPONSE##*$'\n'}"
BODY_OUT="${RESPONSE%$'\n'*}"

if [[ "$HTTP_CODE" != "200" ]]; then
  echo "RAG API error (HTTP ${HTTP_CODE}): ${BODY_OUT}" >&2
  exit 1
fi

echo "$BODY_OUT" | jq -r '.output // .error // .'
