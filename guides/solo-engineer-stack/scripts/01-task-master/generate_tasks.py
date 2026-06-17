#!/usr/bin/env python3
"""Generate artifacts/01-task-master/tasks.json from the PulseFeedback PRD (no Task Master install required)."""

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRD = ROOT / "examples" / "prd-pulsefeedback.md"
OUT = ROOT / "artifacts" / "01-task-master" / "tasks.json"

EPICS = [
    {"id": "E1", "tool": "crewai", "title": "Run research crew", "description": "Produce brief.md, spec.md, test-plan.md"},
    {"id": "E2", "tool": "langgraph", "title": "Approve Deca-Loop gate", "description": "Human sign-off before code generation"},
    {"id": "E3", "tool": "openhands", "title": "Scaffold PulseFeedback repo", "description": "FastAPI + frontend + CI skeleton"},
    {"id": "E4", "tool": "aider", "title": "Implement feedback API", "description": "POST/GET/PATCH /api/feedback with tests"},
    {"id": "E5", "tool": "cline", "title": "Build triage dashboard UI", "description": "Submit form + status badges + browser verify"},
    {"id": "E6", "tool": "n8n", "title": "Wire ops workflows", "description": "Deploy notify + CSAT loop webhooks"},
    {"id": "E7", "tool": "coolify", "title": "Deploy to HTTPS", "description": "Git push deploy for app + n8n"},
    {"id": "E8", "tool": "posthog", "title": "Instrument analytics", "description": "feedback_submitted funnel + feature flag"},
    {"id": "E9", "tool": "chatwoot", "title": "Embed support widget", "description": "Inbox + Captain bot on marketing page"},
    {"id": "E10", "tool": "task_master", "title": "Close CSAT loop", "description": "Low score creates next sprint tasks"},
]


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "project": "PulseFeedback",
        "source_prd": str(PRD.relative_to(ROOT)),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator": "scripts/01-task-master/generate_tasks.py",
        "note": "Run claude-task-master parse-prd for LLM-generated tasks; this file is the demo baseline.",
        "epics": EPICS,
    }
    OUT.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {OUT} ({len(EPICS)} epics)")


if __name__ == "__main__":
    main()
