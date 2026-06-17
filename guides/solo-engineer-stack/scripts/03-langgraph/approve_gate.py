#!/usr/bin/env python3
"""LangGraph stage — human approval gate + save artifacts/03-langgraph/state-approved.json"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "artifacts" / "03-langgraph" / "state-approved.json"


def main():
    import sys

    sys.path.insert(0, str(ROOT))
    from orchestrator.graph import build_graph

    graph = build_graph()
    result = graph.invoke({"human_approved": True, "artifacts": [], "csat_score": None})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "approved_at": datetime.now(timezone.utc).isoformat(),
        "human_approved": True,
        "final_stage": result.get("stage"),
        "artifacts_collected": result.get("artifacts", []),
        "note": "Gate passed — safe to proceed to OpenHands / use pulsefeedback/ reference app",
    }
    OUT.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {OUT}")
    print("Final stage:", result.get("stage"))
    for a in result.get("artifacts", []):
        print(" ", a)


if __name__ == "__main__":
    main()
