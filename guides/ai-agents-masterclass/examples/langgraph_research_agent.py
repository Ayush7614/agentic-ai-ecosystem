#!/usr/bin/env python3
"""LangGraph-style research agent (requires: pip install langgraph langchain-core)."""
from __future__ import annotations

import os
from typing import TypedDict

try:
    from langgraph.graph import END, StateGraph
except ImportError:
    print("Install: pip install langgraph langchain-core")
    raise


class ResearchState(TypedDict):
    topic: str
    notes: list[str]
    report: str


def plan(state: ResearchState) -> ResearchState:
    state["notes"].append(f"Plan: outline for {state['topic']}")
    return state


def research(state: ResearchState) -> ResearchState:
    state["notes"].append("Research: gathered 3 sources (stub)")
    return state


def synthesize(state: ResearchState) -> ResearchState:
    state["report"] = f"# Report: {state['topic']}\n\nFindings from {len(state['notes'])} steps."
    with open("report.md", "w") as f:
        f.write(state["report"])
    return state


def build_graph():
    g = StateGraph(ResearchState)
    g.add_node("plan", plan)
    g.add_node("research", research)
    g.add_node("synthesize", synthesize)
    g.set_entry_point("plan")
    g.add_edge("plan", "research")
    g.add_edge("research", "synthesize")
    g.add_edge("synthesize", END)
    return g.compile()


def main() -> None:
    topic = os.environ.get("RESEARCH_TOPIC", "AI agent governance")
    app = build_graph()
    result = app.invoke({"topic": topic, "notes": [], "report": ""})
    print(f"✓ LangGraph agent finished · {result['report'][:60]}…")


if __name__ == "__main__":
    main()
