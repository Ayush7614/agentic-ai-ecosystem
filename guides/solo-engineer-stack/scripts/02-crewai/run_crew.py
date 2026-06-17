#!/usr/bin/env python3
"""CrewAI stage — writes brief.md, spec.md, test-plan.md. Use --mock for offline demo."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "artifacts" / "02-crewai"

MOCK_BRIEF = """# PulseFeedback — Market Brief

## Problem
Solo founders collect feedback in scattered channels (email, DMs, Notion). Nothing loops back to the product.

## Competitors
- Canny, UserVoice, Frill — hosted, paid, overkill for MVP
- GitHub Issues — wrong UX for non-technical users

## Positioning
Self-hosted, stack-native feedback SaaS built entirely with open-source agent tooling.

## Target user
Indie hacker / solo founder shipping weekly.
"""

MOCK_SPEC = """# PulseFeedback — Technical Spec

## Stack
- Backend: FastAPI + SQLite (Postgres in production)
- Frontend: Static HTML/JS served by FastAPI
- Deploy: Coolify + Docker

## API
| Method | Path | Description |
|--------|------|-------------|
| POST | /api/feedback | Create feedback |
| GET | /api/feedback | List feedback (?status=) |
| PATCH | /api/feedback/{id} | Update status |
| POST | /api/events | Analytics capture |
| POST | /api/webhooks/csat | CSAT loop trigger |
| GET | /api/stack | 10-tool status board |

## Schema
- feedback: id, title, body, email, status (new|triaged|done), created_at
"""

MOCK_QA = """# PulseFeedback — Test Plan

## API
- [ ] POST feedback returns 201 + id
- [ ] GET lists in reverse chronological order
- [ ] PATCH status triaged → done

## UI
- [ ] Submit form clears on success
- [ ] Dashboard status buttons update row
- [ ] Analytics tab shows feedback_submitted

## Stack integration
- [ ] CSAT score 1 creates artifacts/11-csat-loop/new-task.json
- [ ] /api/stack shows 10 tools with live flags
- [ ] n8n webhook hits /api/webhooks/csat (manual curl)
"""


def write_mock():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "brief.md").write_text(MOCK_BRIEF)
    (OUT / "spec.md").write_text(MOCK_SPEC)
    (OUT / "test-plan.md").write_text(MOCK_QA)
    print(f"Wrote mock artifacts to {OUT}/")


def run_crew():
    from crewai import Agent, Crew, LLM, Task

    llm = LLM(model=os.environ.get("CREWAI_MODEL", "gpt-4o"))
    prd = (ROOT / "examples" / "prd-pulsefeedback.md").read_text()

    researcher = Agent(
        role="Market Researcher",
        goal="Summarize feedback-SaaS landscape",
        backstory="B2B SaaS analyst",
        llm=llm,
    )
    architect = Agent(
        role="Technical Architect",
        goal="Write implementable API spec",
        backstory="Staff engineer",
        llm=llm,
    )
    qa = Agent(
        role="QA Lead",
        goal="Acceptance tests for all 10 stack tools",
        backstory="Breaks MVPs before launch",
        llm=llm,
    )

    tasks = [
        Task(description=f"Market brief from PRD:\n{prd[:2000]}", expected_output="brief.md", agent=researcher),
        Task(description="Tech spec with routes and schema", expected_output="spec.md", agent=architect),
        Task(description="Test plan covering API, UI, CSAT loop", expected_output="test-plan.md", agent=qa),
    ]
    result = Crew(agents=[researcher, architect, qa], tasks=tasks, verbose=True).kickoff()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "output.log").write_text(str(result))
    print(result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true", help="Offline demo without LLM")
    args = parser.parse_args()
    if args.mock:
        write_mock()
    else:
        run_crew()


if __name__ == "__main__":
    main()
