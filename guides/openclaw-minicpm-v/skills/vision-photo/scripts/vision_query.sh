#!/usr/bin/env bash
# POST image + question to the local MiniCPM-V vision LitServe API.
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: vision_query.sh /path/to/image.jpg \"your question\"" >&2
  exit 1
fi

IMAGE="$1"
QUERY="$2"
BASE="${VISION_API_URL:-http://127.0.0.1:8002}"
BASE="${BASE%/}"

if [[ ! -f "$IMAGE" ]]; then
  echo "Image not found: $IMAGE" >&2
  exit 1
fi
if ! command -v curl >/dev/null 2>&1; then echo "curl required" >&2; exit 1; fi
if ! command -v jq >/dev/null 2>&1; then echo "jq required" >&2; exit 1; fi

BODY="$(jq -n --arg q "$QUERY" --arg p "$IMAGE" '{query: $q, image_path: $p}')"

RESPONSE="$(curl -sS -X POST "${BASE}/predict" \
  -H 'Content-Type: application/json' \
  -d "$BODY" \
  --max-time 300 \
  -w '\n%{http_code}')"

HTTP_CODE="${RESPONSE##*$'\n'}"
BODY_OUT="${RESPONSE%$'\n'*}"

if [[ "$HTTP_CODE" != "200" ]]; then
  echo "Vision API error (HTTP ${HTTP_CODE}): ${BODY_OUT}" >&2
  exit 1
fi

echo "$BODY_OUT" | jq -r '.output // .error // .'
