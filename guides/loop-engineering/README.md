# Loop Engineering — Visual Guide

Design AI agents that **loop until the goal passes** — not one prompt at a time with you as the checkpoint.

**References:** [Cloud Girl — Loop Engineering](https://priyankavergadia.substack.com/) · [MindStudio — Loop Engineering](https://www.mindstudio.ai/blog/loop-engineering)

## What you'll learn

- **Manual chat vs automated loops** — why the old workflow hit a ceiling  
- **Single-agent & fleet loops** — orchestrator + specialists  
- **Open vs closed loops** — exploration vs production budgets  
- **Five loop parts** + four common **patterns**  
- Framework mapping (LangGraph, Swarm, Hermes, OpenClaw)  
- Runnable **closed-loop** example + eval gate YAML  

![Manual vs loop](./assets/diagram-manual-vs-loop.gif)

**Blog mega-GIF:** [mega-loop-everything.gif](./assets/mega-loop-everything.gif)

## Quick start

```bash
cd guides/loop-engineering
python examples/minimal_closed_loop.py
```

## Guide map

- **[Full tutorial](./TUTORIAL.md)** — Parts 1–15 with GIFs  
- **[Examples](./examples/)** — minimal loop + eval gate config  
- **[Assets](./assets/)** — 10 diagram GIFs, 5 terminal GIFs, blog poster  

## Related guides

- [Hermes Agent Masterclass](../hermes-agent-masterclass/) — ReAct runtime, tools, cron loops  
- [OpenClaw](../openclaw/) — gateway, multi-agent, proactive heartbeat  
- [LLM Fine-Tuning](../llm-fine-tuning/) — adapt models loops run on  

**Blog header:** `assets/blog-poster-1200x600.png`

## License

Guide: MIT
