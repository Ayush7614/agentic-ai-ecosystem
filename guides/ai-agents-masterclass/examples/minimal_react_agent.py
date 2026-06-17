#!/usr/bin/env python3
"""Minimal ReAct-style agent loop — no framework deps beyond stdlib + optional OpenAI."""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field


@dataclass
class AgentState:
    goal: str
    steps: list[str] = field(default_factory=list)
    done: bool = False


def search_web(query: str) -> str:
    """Stub tool — replace with real search API."""
    return json.dumps({"query": query, "snippet": "High tide + sunny weeks: late June–July (stub data)"})


def weather_db(location: str) -> str:
    return json.dumps({"location": location, "years": 5, "avg_sunny_days_july": 28})


TOOLS = {
    "search_web": search_web,
    "weather_db": weather_db,
}


def think_and_act(state: AgentState, turn: int) -> None:
    """Deterministic demo loop mimicking Think → Act → Observe."""
    if turn == 0:
        state.steps.append("Think: need historical weather for Greece")
        out = TOOLS["weather_db"]("Greece")
        state.steps.append(f"Act: weather_db → {out}")
    elif turn == 1:
        state.steps.append("Think: need surfing conditions (high tide)")
        out = TOOLS["search_web"]("best surfing tide Greece")
        state.steps.append(f"Act: search_web → {out}")
    elif turn == 2:
        state.steps.append("Observe: combine tide + sunny patterns")
        state.steps.append("Act: recommend week of July 12–19 (demo)")
        state.done = True
    else:
        state.done = True


def run(goal: str, max_turns: int = 8) -> AgentState:
    state = AgentState(goal=goal)
    for turn in range(max_turns):
        if state.done:
            break
        think_and_act(state, turn)
    return state


def main() -> None:
    goal = os.environ.get("AGENT_GOAL", "Best week for surfing in Greece next year")
    print(f"Goal: {goal!r}")
    state = run(goal)
    for line in state.steps:
        print(line)
    print("✓ ReAct loop completed" if state.done else "… max turns reached")


if __name__ == "__main__":
    main()
