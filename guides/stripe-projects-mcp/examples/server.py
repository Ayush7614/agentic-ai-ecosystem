#!/usr/bin/env python3
"""Stripe Projects MCP server — give your agent a safe credit card.

Exposes four tools over MCP so any host (Cursor, Claude Code, Hermes) can
provision real infra through one protocol:

    provision(name, provider, spend_cap_usd=…)  → mint a capped, scoped key
    list_projects()                             → see status + spend per project
    rotate_key(name)                            → kill the old key, mint a new one
    teardown(name)                              → revoke the key, stop billing

The credential is written to a local .env file (never printed in full) so the
same agent can immediately *use* what it provisioned — e.g. provision
"supermemory" and start storing memories in the next turn.

Run:  python examples/server.py        # stdio transport (for MCP hosts)
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

from mcp.server.fastmcp import FastMCP

try:  # allow `python examples/server.py` and `from examples.server import …`
    from . import providers
    from .stripe_projects import Backend, ProvisionError
except ImportError:  # pragma: no cover - direct script run
    import providers  # type: ignore
    from stripe_projects import Backend, ProvisionError  # type: ignore

ENV_PATH = Path(os.environ.get("AGENT_ENV_FILE", Path(__file__).with_name(".env")))

mcp = FastMCP("stripe-projects")
backend = Backend()


def _upsert_env(var: str, value: str) -> None:
    """Write KEY=value into the agent's .env, replacing any prior line."""
    line = f"{var}={value}"
    existing = ENV_PATH.read_text().splitlines() if ENV_PATH.exists() else []
    out, replaced = [], False
    for row in existing:
        if re.match(rf"^{re.escape(var)}=", row):
            out.append(line)
            replaced = True
        else:
            out.append(row)
    if not replaced:
        out.append(line)
    ENV_PATH.write_text("\n".join(out) + "\n")


@mcp.tool()
def provision(name: str, provider: str, spend_cap_usd: float = 0.0) -> str:
    """Provision a service through Stripe Projects and store its scoped key.

    Args:
        name: a label for this project, e.g. "agent-memory".
        provider: which service to stand up. One of the registry keys
            (supermemory, vector-db, email).
        spend_cap_usd: hard billing cap. 0 = use the provider default.

    Returns a JSON summary. The real key lands in the agent's .env; only a
    masked form is returned so it can't leak through the model transcript.
    """
    try:
        prov = providers.get(provider)
    except KeyError as exc:
        return json.dumps({"error": str(exc)})

    cap = spend_cap_usd or prov.default_cap_usd
    try:
        project = backend.provision(name=name, provider=provider, spend_cap_usd=cap)
    except ProvisionError as exc:
        return json.dumps({"error": str(exc)})

    _upsert_env(prov.env_var, project.api_key)
    summary = project.public_view()
    summary["env_var"] = prov.env_var
    summary["env_written_to"] = str(ENV_PATH.name)
    summary["next"] = f"key available as ${prov.env_var}; you can now use {prov.label}"
    return json.dumps(summary, indent=2)


@mcp.tool()
def list_projects() -> str:
    """List every provisioned project with status, spend cap, and usage."""
    projects = [p.public_view() for p in backend.list_projects()]
    return json.dumps({"count": len(projects), "projects": projects}, indent=2)


@mcp.tool()
def rotate_key(name: str) -> str:
    """Rotate a project's key — the previous key stops working immediately."""
    try:
        project = backend.rotate_key(name)
    except ProvisionError as exc:
        return json.dumps({"error": str(exc)})
    prov = providers.get(project.provider)
    _upsert_env(prov.env_var, project.api_key)
    summary = project.public_view()
    summary["rotated_to_version"] = project.key_version
    return json.dumps(summary, indent=2)


@mcp.tool()
def teardown(name: str) -> str:
    """Tear down a project — revokes the key and stops all billing."""
    try:
        project = backend.teardown(name)
    except ProvisionError as exc:
        return json.dumps({"error": str(exc)})
    return json.dumps({"name": name, "status": project.status,
                       "message": "key revoked, billing stopped"}, indent=2)


@mcp.resource("stripe-projects://providers")
def list_providers() -> str:
    """Capability hint for hosts: which providers this server can provision."""
    return json.dumps(
        {k: {"label": p.label, "env_var": p.env_var, "default_cap_usd": p.default_cap_usd}
         for k, p in providers.REGISTRY.items()},
        indent=2,
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
