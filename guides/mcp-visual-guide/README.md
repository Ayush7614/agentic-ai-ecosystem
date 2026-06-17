# Model Context Protocol (MCP) — Visual Guide

Original guide to **connecting AI hosts to tools and data** — host/client/server architecture, capability exchange, API vs MCP, building servers, and the next wave of **UI-native MCP apps**.

**References (not copies):** [Daily Dose of Data — Visual Guide to MCP](https://www.dailydoseofds.com/p/visual-guide-to-model-context-protocol-mcp/) · [Visuals MCP — Giving Your AI Agent a Face](https://harrybin.de/posts/visuals-mcp-server/)

## What you'll learn

- **USB-C mental model** — one protocol, many data sources  
- **Host · Client · Server** — who talks to whom  
- **Tools, Resources, Prompts** — what servers expose  
- **Capability exchange** — why MCP beats rigid REST contracts for agents  
- **Transport** — stdio, SSE, streamable HTTP  
- **App MCP** — interactive UI beyond markdown tables  
- Runnable **Python weather server** + host config snippets  

![MCP hub — one host, many servers](./assets/diagram-usbc-hub.gif)

**Blog mega-GIF:** [mega-mcp-everything.gif](./assets/mega-mcp-everything.gif)

## Quick start

```bash
pip install "mcp[cli]>=1.2"
cd guides/mcp-visual-guide
python examples/minimal_weather_server.py   # stdio MCP server
# Add examples/cursor_mcp.json snippet to Cursor → MCP settings
```

## Guide map

- **[Full tutorial](./TUTORIAL.md)** — Parts 1–14 with GIFs  
- **[Examples](./examples/)** — weather server, Cursor + Claude Desktop config  
- **[Assets](./assets/)** — diagram + terminal GIFs, blog poster  

## Related guides

- [Hermes masterclass](../hermes-agent-masterclass/) — agents that consume MCP tools  
- [Loop engineering](../loop-engineering/) — tool-call loops inside the host  
- [Harness engineering](../harness-engineering/) — environment around the agent  
- [OpenClaw](../openclaw/) — gateway + skills + MCP-style tool wiring  

**Blog header:** `assets/blog-poster-1200x600.png` · Regenerate: `cd assets && python3 render_blog_poster.py`

## License

Guide: MIT · MCP spec & SDKs: respective licenses
