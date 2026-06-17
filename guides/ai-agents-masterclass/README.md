# AI Agents Masterclass — Visual Guide

**Original comprehensive masterclass** on AI agents: definitions, ReAct/ReWOO, anatomy, 15+ frameworks, six use-case families, MCP/A2A, governance, Cloud Run, and **five runnable code examples** with white-theme GIFs.

**References (not copies):** [ServiceNow AI Agent Masterclass](https://www.servicenow.com/community/now-assist-articles/ai-agent-masterclass-overview-recordings-and-resources/ta-p/3469262) · [coleam00/ai-agents-masterclass](https://github.com/coleam00/ai-agents-masterclass) · [OpenAI — Building AI agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)

## What you'll learn

- **Agent vs assistant vs bot** — autonomy, complexity, learning  
- **Six capabilities** — reason, act, observe, plan, collaborate, self-refine  
- **Anatomy** — persona, memory, tools, model  
- **ReAct + ReWOO** — two dominant reasoning paradigms  
- **Multi-agent** — single vs fleet, surface vs background  
- **Frameworks** — LangGraph, CrewAI, AutoGen, OpenAI SDK, Pydantic AI, Google ADK, Hermes, OpenClaw, and more  
- **Protocols** — MCP tools layer, A2A agent mesh  
- **Production** — HITL, logs, Cloud Run, evals  

![What is an AI agent](./assets/diagram-agent-definition.gif)

**Blog mega-GIF:** [mega-agents-everything.gif](./assets/mega-agents-everything.gif)

## Quick start

```bash
cd guides/ai-agents-masterclass
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # optional — per-framework
python examples/minimal_react_agent.py   # no API key required
```

## Guide map

- **[Full tutorial](./TUTORIAL.md)** — Parts 1–35 with diagram + terminal GIFs  
- **[Examples](./examples/)** — ReAct, LangGraph, CrewAI, OpenAI SDK, Pydantic AI  
- **[Assets](./assets/)** — 18 diagram GIFs, 7 terminal GIFs, blog poster  

## Related guides

- [MCP Visual Guide](../mcp-visual-guide/) — tool protocol for agents  
- [Loop Engineering](../loop-engineering/) — ReAct loops and eval gates  
- [Harness Engineering](../harness-engineering/) — agent environment design  
- [Hermes Agent Masterclass](../hermes-agent-masterclass/) — self-improving agent runtime  

**Blog header:** `assets/blog-poster-1200x600.png` · Regenerate: `cd assets && python3 render_diagrams.py all`

## License

Guide: MIT · Framework SDKs: respective licenses
