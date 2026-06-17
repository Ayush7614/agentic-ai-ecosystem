#!/usr/bin/env python3
"""Pydantic AI typed agent (requires: pip install pydantic-ai)."""
from __future__ import annotations

import os
from pydantic import BaseModel


class WeatherReport(BaseModel):
    location: str
    best_week: str
    confidence: float
    notes: str


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        report = WeatherReport(
            location="Greece",
            best_week="July 12–19",
            confidence=0.82,
            notes="Demo stub — set OPENAI_API_KEY for live run",
        )
        print(f"✓ Validated Pydantic model: {report.model_dump()}")
        return

    try:
        from pydantic_ai import Agent
    except ImportError:
        print("Install: pip install pydantic-ai")
        raise

    agent = Agent("openai:gpt-4o-mini", result_type=WeatherReport, system_prompt="You are a weather planning assistant.")
    result = agent.run_sync("Best surfing week in Greece next year?")
    print(f"✓ Validated Pydantic model returned: {result.data}")


if __name__ == "__main__":
    main()
