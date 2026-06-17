#!/usr/bin/env python3
"""
PulseFeedback Deca-Loop — LangGraph orchestrator (Stage 3 of 10).

Each node represents one equal stage. Stages 4–10 trigger external tools
via webhooks (n8n) or human checkpoints. Run with --dry-run to print the path.

Usage:
  python orchestrator/graph.py --dry-run
  python orchestrator/graph.py --stage crewai
"""

from __future__ import annotations

import argparse
from typing import Literal, TypedDict

Stage = Literal[
    "task_master",
    "crewai",
    "langgraph",
    "openhands",
    "aider",
    "cline",
    "n8n",
    "coolify",
    "posthog",
    "chatwoot",
    "done",
]

STAGES: list[Stage] = [
    "task_master",
    "crewai",
    "langgraph",
    "openhands",
    "aider",
    "cline",
    "n8n",
    "coolify",
    "posthog",
    "chatwoot",
]

STAGE_ARTIFACTS: dict[Stage, str] = {
    "task_master": "tasks.json — 10 epics from PRD",
    "crewai": "brief.md + spec.md + test-plan.md",
    "langgraph": "orchestrator approval + state snapshot",
    "openhands": "GitHub repo scaffold + CI",
    "aider": "FastAPI routes + commits",
    "cline": "React dashboard + Playwright pass",
    "n8n": "workflows: deploy, notify, csat-loop",
    "coolify": "HTTPS URLs for app + services",
    "posthog": "events + feature flags live",
    "chatwoot": "inbox + widget embedded",
    "done": "PulseFeedback loop closed",
}


def print_dry_run():
    print("PulseFeedback Deca-Loop — 10 equal stages\n")
    for i, stage in enumerate(STAGES, 1):
        print(f"  {i:2}. {stage:12} → {STAGE_ARTIFACTS[stage]}")
    print("\n  CSAT ≤ 2 loops back to task_master")


class LoopState(TypedDict, total=False):
    stage: Stage
    artifacts: list[str]
    human_approved: bool
    csat_score: float | None


def _advance(state: LoopState, next_stage: Stage) -> LoopState:
    artifact = STAGE_ARTIFACTS.get(state.get("stage", "task_master"), "")
    artifacts = list(state.get("artifacts", []))
    if artifact and artifact not in artifacts:
        artifacts.append(artifact)
    return {"stage": next_stage, "artifacts": artifacts}


def node_task_master(state: LoopState) -> LoopState:
    return _advance({**state, "stage": "task_master"}, "crewai")


def node_crewai(state: LoopState) -> LoopState:
    return _advance({**state, "stage": "crewai"}, "langgraph")


def node_langgraph_gate(state: LoopState) -> LoopState:
    if not state.get("human_approved", True):
        return {"stage": "langgraph", "artifacts": state.get("artifacts", [])}
    return _advance({**state, "stage": "langgraph"}, "openhands")


def node_openhands(state: LoopState) -> LoopState:
    return _advance({**state, "stage": "openhands"}, "aider")


def node_aider(state: LoopState) -> LoopState:
    return _advance({**state, "stage": "aider"}, "cline")


def node_cline(state: LoopState) -> LoopState:
    return _advance({**state, "stage": "cline"}, "n8n")


def node_n8n(state: LoopState) -> LoopState:
    return _advance({**state, "stage": "n8n"}, "coolify")


def node_coolify(state: LoopState) -> LoopState:
    return _advance({**state, "stage": "coolify"}, "posthog")


def node_posthog(state: LoopState) -> LoopState:
    return _advance({**state, "stage": "posthog"}, "chatwoot")


def node_chatwoot(state: LoopState) -> LoopState:
    score = state.get("csat_score")
    if score is not None and score <= 2.0:
        return {
            "stage": "task_master",
            "artifacts": state.get("artifacts", []),
            "csat_score": None,
            "human_approved": False,
        }
    return _advance({**state, "stage": "chatwoot"}, "done")


def build_graph():
    from langgraph.graph import END, START, StateGraph

    builder = StateGraph(LoopState)
    builder.add_node("task_master", node_task_master)
    builder.add_node("crewai", node_crewai)
    builder.add_node("langgraph_gate", node_langgraph_gate)
    builder.add_node("openhands", node_openhands)
    builder.add_node("aider", node_aider)
    builder.add_node("cline", node_cline)
    builder.add_node("n8n", node_n8n)
    builder.add_node("coolify", node_coolify)
    builder.add_node("posthog", node_posthog)
    builder.add_node("chatwoot", node_chatwoot)

    builder.add_edge(START, "task_master")
    builder.add_edge("task_master", "crewai")
    builder.add_edge("crewai", "langgraph_gate")
    builder.add_edge("langgraph_gate", "openhands")
    builder.add_edge("openhands", "aider")
    builder.add_edge("aider", "cline")
    builder.add_edge("cline", "n8n")
    builder.add_edge("n8n", "coolify")
    builder.add_edge("coolify", "posthog")
    builder.add_edge("posthog", "chatwoot")
    builder.add_conditional_edges(
        "chatwoot",
        lambda s: "loop" if s.get("stage") == "task_master" else "done",
        {"loop": "task_master", "done": END},
    )
    return builder.compile()


def main():
    parser = argparse.ArgumentParser(description="PulseFeedback Deca-Loop orchestrator")
    parser.add_argument("--dry-run", action="store_true", help="Print all 10 stages")
    parser.add_argument("--csat", type=float, default=None, help="Simulate CSAT score at end")
    args = parser.parse_args()

    if args.dry_run:
        print_dry_run()
        return

    graph = build_graph()
    result = graph.invoke(
        {"human_approved": True, "artifacts": [], "csat_score": args.csat}
    )
    print("Final stage:", result.get("stage"))
    print("Artifacts:")
    for a in result.get("artifacts", []):
        print(" ", a)


if __name__ == "__main__":
    main()
