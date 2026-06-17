"""Smoke tests for agent examples (stdlib only for minimal_react)."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"


def test_minimal_react_runs():
    r = subprocess.run([sys.executable, str(EXAMPLES / "minimal_react_agent.py")], capture_output=True, text=True)
    assert r.returncode == 0
    assert "ReAct loop completed" in r.stdout


def test_langgraph_import_or_skip():
    r = subprocess.run([sys.executable, "-c", "import langgraph"], capture_output=True)
    if r.returncode != 0:
        return
    r2 = subprocess.run([sys.executable, str(EXAMPLES / "langgraph_research_agent.py")], capture_output=True, text=True)
    assert r2.returncode == 0


def test_crewai_demo_stub():
    r = subprocess.run([sys.executable, str(EXAMPLES / "crewai_content_crew.py")], capture_output=True, text=True, env={**__import__("os").environ})
    assert r.returncode == 0
    assert "blog_draft.md" in r.stdout


def test_openai_sdk_demo():
    r = subprocess.run([sys.executable, str(EXAMPLES / "openai_agents_sdk.py")], capture_output=True, text=True)
    assert r.returncode == 0


def test_pydantic_ai_demo():
    r = subprocess.run([sys.executable, str(EXAMPLES / "pydantic_ai_typed_agent.py")], capture_output=True, text=True)
    assert r.returncode == 0
