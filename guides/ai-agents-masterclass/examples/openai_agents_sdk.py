#!/usr/bin/env python3
"""OpenAI Agents SDK handoff pattern (requires: pip install openai-agents + OPENAI_API_KEY)."""
from __future__ import annotations

import asyncio
import os


async def run_demo() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        print("✓ Agent handoff: triage → specialist (demo — set OPENAI_API_KEY)")
        return

    try:
        from agents import Agent, Runner
    except ImportError:
        print("Install: pip install openai-agents")
        raise

    specialist = Agent(name="Specialist", instructions="Answer technical AI agent questions concisely.")
    triage = Agent(
        name="Triage",
        instructions="Route technical questions to Specialist.",
        handoffs=[specialist],
    )
    result = await Runner.run(triage, "What is ReAct for AI agents?")
    print(f"✓ Agent handoff complete: {result.final_output[:80]}…")


def main() -> None:
    asyncio.run(run_demo())


if __name__ == "__main__":
    main()
