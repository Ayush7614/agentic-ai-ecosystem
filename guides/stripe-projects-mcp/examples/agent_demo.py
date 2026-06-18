#!/usr/bin/env python3
"""End-to-end demo: provision over MCP, then USE what you provisioned.

This is the story the guide tells, in one runnable script:

    1. The agent provisions "supermemory" through the Stripe Projects MCP server
       → a capped, scoped key is minted and written to .env.
    2. The SAME agent loads that key and stores a few memories.
    3. A later "session" searches its memory — continuity it just paid for.
    4. Mock usage accrues against the spend cap; we rotate the key, then tear
       the project down to stop billing.

It calls the MCP *tool functions* directly (no transport needed) so you can see
exactly what a host like Cursor or Claude Code would get back over the wire.
Runs fully offline: simulated keys route supermemory to a local memory store.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import providers
import server


def show(title: str, payload: str) -> None:
    print(f"\n\033[1m▸ {title}\033[0m")
    print(payload)


def load_env_into_process(env_path: Path) -> None:
    """Mimic a host reloading .env so the freshly minted key is visible."""
    if not env_path.exists():
        return
    for row in env_path.read_text().splitlines():
        if "=" in row and not row.startswith("#"):
            k, v = row.split("=", 1)
            os.environ[k] = v


def main() -> None:
    name = "agent-memory"

    show("provision(supermemory)", server.provision(name, "supermemory", spend_cap_usd=15))
    show("list_projects()", server.list_projects())

    # The host reloads .env → the agent now holds the scoped key.
    load_env_into_process(server.ENV_PATH)
    mem = providers.supermemory_from_env()
    print(f"\n  supermemory client mode: {mem.mode}")

    # Use the thing we just provisioned.
    mem.add("User prefers dark-mode dashboards and concise weekly digests.",
            metadata={"kind": "preference"})
    mem.add("Production DB is Postgres 16 on the eu-west region.",
            metadata={"kind": "infra"})
    server.backend.record_usage(name, 4.0)  # pretend those writes cost $4

    # A later session recalls context.
    hits = mem.search("what does the user prefer for dashboards?")
    show("memory.search('dashboard preference')", json.dumps(hits, indent=2))

    # Spend management: rotate the key, then tear it all down.
    show("rotate_key(agent-memory)", server.rotate_key(name))
    show("teardown(agent-memory)", server.teardown(name))
    show("list_projects() after teardown", server.list_projects())


if __name__ == "__main__":
    main()
