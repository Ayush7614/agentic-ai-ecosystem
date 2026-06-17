#!/usr/bin/env bash
# Verify all 10 stack stages have real artifacts in this repo.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PASS=0
FAIL=0

check() {
  if [[ -e "$1" ]]; then
    echo "  ✓ $2"
    PASS=$((PASS + 1))
  else
    echo "  ✗ $2 (missing: $1)"
    FAIL=$((FAIL + 1))
  fi
}

echo "Solo Engineer Stack — artifact verification"
echo ""

echo "1  Task Master"
check artifacts/01-task-master/tasks.json "tasks.json"

echo "2  CrewAI"
check artifacts/02-crewai/brief.md "brief.md"
check artifacts/02-crewai/spec.md "spec.md"
check artifacts/02-crewai/test-plan.md "test-plan.md"

echo "3  LangGraph"
check orchestrator/graph.py "orchestrator/graph.py"
if python3 orchestrator/graph.py --dry-run >/dev/null; then
  echo "  ✓ dry-run OK"
  PASS=$((PASS + 1))
else
  echo "  ✗ dry-run failed"
  FAIL=$((FAIL + 1))
fi
check artifacts/03-langgraph/state-approved.json "state-approved.json (run approve_gate.py)"

echo "4–6  OpenHands / Aider / Cline → PulseFeedback app"
check pulsefeedback/backend/main.py "FastAPI backend"
check pulsefeedback/frontend/index.html "frontend UI"
check tests/test_api.py "API tests"

echo "7  n8n"
check n8n/workflows/csat-loop.json "CSAT workflow JSON"

echo "8  Coolify"
check pulsefeedback/Dockerfile "Dockerfile"
check docker-compose.yml "docker-compose.yml"

echo "9  PostHog (local event API)"
check pulsefeedback/backend/main.py "POST /api/events in main.py"

echo "10 Chatwoot (CSAT webhook)"
check pulsefeedback/backend/main.py "POST /api/webhooks/csat in main.py"

echo ""
if [[ "$FAIL" -eq 0 ]]; then
  echo "All checks passed ($PASS). Run ./scripts/demo.sh for live demo."
  exit 0
else
  echo "$FAIL check(s) failed. Run ./scripts/demo.sh to regenerate artifacts."
  exit 1
fi
