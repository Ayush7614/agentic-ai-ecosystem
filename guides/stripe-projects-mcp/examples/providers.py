#!/usr/bin/env python3
"""Provider registry — what the MCP server is allowed to provision.

A *provider* is a recipe the server knows how to stand up through Stripe
Projects. Keeping providers in a registry (instead of hard-coding them into the
MCP tools) is the whole trick: adding a new provisionable service is one entry,
and every MCP host gets it for free at the next capability exchange.

`supermemory` is the headline provider — once provisioned, the same agent can
use the minted key for cross-session memory. The supermemory adapter calls the
real API when `SUPERMEMORY_API_KEY` is set and the SDK is importable, and falls
back to a local JSON memory store otherwise so the demo always runs offline.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Provider:
    """A provisionable service: env var to set + sensible default spend cap."""

    key: str
    label: str
    env_var: str
    default_cap_usd: float
    docs: str


REGISTRY: dict[str, Provider] = {
    "supermemory": Provider(
        key="supermemory",
        label="Supermemory (agent long-term memory)",
        env_var="SUPERMEMORY_API_KEY",
        default_cap_usd=25.0,
        docs="https://supermemory.ai",
    ),
    "vector-db": Provider(
        key="vector-db",
        label="Managed vector database",
        env_var="VECTOR_DB_API_KEY",
        default_cap_usd=50.0,
        docs="https://example.com/vector-db",
    ),
    "email": Provider(
        key="email",
        label="Transactional email sender",
        env_var="EMAIL_API_KEY",
        default_cap_usd=10.0,
        docs="https://example.com/email",
    ),
}


def get(provider_key: str) -> Provider:
    try:
        return REGISTRY[provider_key]
    except KeyError:
        known = ", ".join(sorted(REGISTRY))
        raise KeyError(f"unknown provider '{provider_key}'. known: {known}")


# ---------------------------------------------------------------------------
# Supermemory client — real API when possible, local fallback otherwise.
# ---------------------------------------------------------------------------

_LOCAL_MEM_PATH = Path(__file__).with_name(".supermemory_local.json")


class SupermemoryClient:
    """Thin wrapper so the agent demo doesn't care if it's live or simulated."""

    def __init__(self, api_key: str | None) -> None:
        self.api_key = api_key
        self._real = None
        # Try the real SDK only if a key was provisioned.
        if api_key and not api_key.startswith("sk_proj_sim_"):
            try:  # pragma: no cover - exercised only with a live key
                from supermemory import Supermemory  # type: ignore

                self._real = Supermemory(api_key=api_key)
            except Exception:
                self._real = None

    @property
    def mode(self) -> str:
        return "live" if self._real else "local-fallback"

    def add(self, content: str, metadata: dict | None = None) -> dict:
        if self._real:  # pragma: no cover
            return self._real.memories.add(content=content, metadata=metadata or {})
        store = self._load_local()
        entry = {"id": f"mem_{len(store) + 1}", "content": content,
                 "metadata": metadata or {}, "ts": time.time()}
        store.append(entry)
        self._save_local(store)
        return entry

    def search(self, query: str, limit: int = 3) -> list[dict]:
        if self._real:  # pragma: no cover
            res = self._real.search.execute(q=query, limit=limit)
            return getattr(res, "results", res)
        store = self._load_local()
        q = query.lower()
        scored = [(sum(w in e["content"].lower() for w in q.split()), e) for e in store]
        hits = [e for score, e in sorted(scored, key=lambda x: -x[0]) if score]
        return hits[:limit]

    @staticmethod
    def _load_local() -> list[dict]:
        if _LOCAL_MEM_PATH.exists():
            return json.loads(_LOCAL_MEM_PATH.read_text())
        return []

    @staticmethod
    def _save_local(store: list[dict]) -> None:
        _LOCAL_MEM_PATH.write_text(json.dumps(store, indent=2))


def supermemory_from_env() -> SupermemoryClient:
    return SupermemoryClient(os.environ.get("SUPERMEMORY_API_KEY"))
