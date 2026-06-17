#!/usr/bin/env bash
# Live demo — run PulseFeedback + generate stack artifacts + smoke test all tabs.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "══════════════════════════════════════════════════════════"
echo "  PulseFeedback — Solo Engineer Stack LIVE DEMO"
echo "══════════════════════════════════════════════════════════"

# Stage 1–2 artifacts
python3 scripts/01-task-master/generate_tasks.py
python3 scripts/02-crewai/run_crew.py --mock

# Stage 3 LangGraph
python3 orchestrator/graph.py --dry-run
python3 scripts/03-langgraph/approve_gate.py || true
echo ""

# Backend deps
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -q -r pulsefeedback/backend/requirements.txt

PORT="${PORT:-8080}"
export PORT

# Start API if not running
if ! curl -sf "http://127.0.0.1:${PORT}/health" >/dev/null 2>&1; then
  echo "Starting PulseFeedback on http://127.0.0.1:${PORT} ..."
  (cd pulsefeedback/backend && uvicorn main:app --host 127.0.0.1 --port "$PORT") &
  APP_PID=$!
  trap 'kill $APP_PID 2>/dev/null || true' EXIT
  for _ in $(seq 1 20); do
    curl -sf "http://127.0.0.1:${PORT}/health" >/dev/null && break
    sleep 0.3
  done
fi

echo ""
echo "── Smoke test (API) ──"
curl -sf "http://127.0.0.1:${PORT}/health" | python3 -m json.tool
curl -sf -X POST "http://127.0.0.1:${PORT}/api/feedback" \
  -H 'Content-Type: application/json' \
  -d '{"title":"Demo feedback","body":"Live demo from scripts/demo.sh"}' | python3 -m json.tool
curl -sf "http://127.0.0.1:${PORT}/api/feedback" | python3 -m json.tool | head -20

echo ""
echo "── CSAT loop (score=1 → Task Master artifact) ──"
curl -sf -X POST "http://127.0.0.1:${PORT}/api/webhooks/csat" \
  -H 'Content-Type: application/json' \
  -d '{"score":1,"comment":"Demo unhappy user"}' | python3 -m json.tool
cat artifacts/11-csat-loop/new-task.json 2>/dev/null || true

echo ""
echo "── 10-tool status ──"
curl -sf "http://127.0.0.1:${PORT}/api/stack" | python3 -m json.tool

echo ""
echo "══════════════════════════════════════════════════════════"
echo "  OPEN IN BROWSER: http://127.0.0.1:${PORT}"
echo "  Tabs to demo: Submit → Dashboard → Analytics → Support → 10 Tools"
echo "  Optional: docker compose up -d n8n  →  http://localhost:5678"
echo "══════════════════════════════════════════════════════════"

if [[ -n "${APP_PID:-}" ]]; then
  echo "Press Ctrl+C to stop the server."
  wait "$APP_PID"
fi
