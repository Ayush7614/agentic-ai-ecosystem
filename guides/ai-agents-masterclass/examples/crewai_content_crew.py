#!/usr/bin/env python3
"""CrewAI content crew demo (requires: pip install crewai)."""
from __future__ import annotations

import os

try:
    from crewai import Agent, Crew, Process, Task
except ImportError:
    print("Install: pip install crewai")
    raise


def main() -> None:
    topic = os.environ.get("CREW_TOPIC", "Why AI agents need governance")

    researcher = Agent(
        role="Research Analyst",
        goal="Find accurate facts about the topic",
        backstory="You distill complex AI topics into bullet facts.",
        verbose=False,
        allow_delegation=False,
    )
    writer = Agent(
        role="Technical Writer",
        goal="Draft a clear blog section",
        backstory="You write for senior engineers.",
        verbose=False,
        allow_delegation=False,
    )

    research_task = Task(
        description=f"List 5 key points about: {topic}",
        expected_output="Bullet list of 5 facts",
        agent=researcher,
    )
    write_task = Task(
        description="Turn the research into a 200-word blog draft",
        expected_output="Markdown blog section",
        agent=writer,
    )

    crew = Crew(agents=[researcher, writer], tasks=[research_task, write_task], process=Process.sequential)
    # Demo mode: write placeholder when no LLM key
    if not os.environ.get("OPENAI_API_KEY"):
        draft = f"# {topic}\n\n(Demo mode — set OPENAI_API_KEY for live crew run)\n"
        with open("blog_draft.md", "w") as f:
            f.write(draft)
        print("✓ Crew output: blog_draft.md (demo stub)")
        return

    result = crew.kickoff()
    with open("blog_draft.md", "w") as f:
        f.write(str(result))
    print("✓ Crew output: blog_draft.md")


if __name__ == "__main__":
    main()
