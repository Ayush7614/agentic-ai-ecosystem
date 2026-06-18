#!/usr/bin/env python3
"""Simulated Stripe Projects backend.

This stands in for the real `stripe projects` CLI / API. It does the one thing
that matters for the guide: turn a *provision* request into a billable, capped,
revocable credential — without ever touching your real root key.

The simulation is deliberately real-shaped:

- Each provisioned service becomes a **project** with a spend cap and a status.
- Provisioning mints a scoped API key (the agent never sees your root key).
- A mock **invoice** accrues usage so `list` can report real-looking spend.
- Keys can be **rotated** (old key dies) and projects can be **torn down**.

State persists to a local JSON file so the MCP server, the CLI, and the agent
demo all see the same world between runs. To wire the *real* Stripe Projects,
replace the bodies of the `Backend` methods with CLI/API calls — the shapes of
the return values are what the rest of the guide depends on.
"""
from __future__ import annotations

import json
import os
import secrets
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

STATE_PATH = Path(os.environ.get("STRIPE_PROJECTS_STATE", Path(__file__).with_name(".stripe_projects_state.json")))

# A scoped key always carries the project id so a leaked key is traceable and
# revocable in isolation — the whole point of the "safe credit card".
KEY_PREFIX = "sk_proj_sim_"


class ProvisionError(RuntimeError):
    """Raised for invalid provisioning requests (unknown provider, dup name…)."""


@dataclass
class Project:
    name: str
    provider: str
    project_id: str
    api_key: str
    spend_cap_usd: float
    status: str = "active"  # active | suspended | torn_down
    created_at: float = field(default_factory=time.time)
    usage_usd: float = 0.0
    key_version: int = 1

    def public_view(self) -> dict:
        """What an agent is allowed to see — never the full key in plaintext."""
        if self.api_key.startswith(KEY_PREFIX):
            masked = self.api_key[:len(KEY_PREFIX) + 4] + "…" + self.api_key[-4:]
        else:
            masked = self.api_key  # e.g. "revoked"
        return {
            "name": self.name,
            "provider": self.provider,
            "project_id": self.project_id,
            "api_key_masked": masked,
            "status": self.status,
            "spend_cap_usd": self.spend_cap_usd,
            "usage_usd": round(self.usage_usd, 4),
            "remaining_usd": round(max(self.spend_cap_usd - self.usage_usd, 0.0), 4),
            "key_version": self.key_version,
        }


class Backend:
    """Tiny persistent store that mimics Stripe Projects semantics."""

    def __init__(self, state_path: Path = STATE_PATH) -> None:
        self.state_path = state_path
        self._projects: dict[str, Project] = {}
        self._load()

    # ----- persistence -------------------------------------------------
    def _load(self) -> None:
        if self.state_path.exists():
            raw = json.loads(self.state_path.read_text())
            self._projects = {k: Project(**v) for k, v in raw.items()}

    def _save(self) -> None:
        payload = {k: asdict(v) for k, v in self._projects.items()}
        self.state_path.write_text(json.dumps(payload, indent=2))

    # ----- helpers -----------------------------------------------------
    @staticmethod
    def _mint_key() -> str:
        return KEY_PREFIX + secrets.token_hex(16)

    def _require_active(self, name: str) -> Project:
        proj = self._projects.get(name)
        if proj is None:
            raise ProvisionError(f"no project named '{name}'")
        if proj.status == "torn_down":
            raise ProvisionError(f"project '{name}' was torn down")
        return proj

    # ----- the four primitives ----------------------------------------
    def provision(self, name: str, provider: str, spend_cap_usd: float = 25.0) -> Project:
        existing = self._projects.get(name)
        if existing and existing.status != "torn_down":
            raise ProvisionError(f"project '{name}' already exists (status={existing.status})")
        proj = Project(
            name=name,
            provider=provider,
            project_id="proj_" + secrets.token_hex(6),
            api_key=self._mint_key(),
            spend_cap_usd=float(spend_cap_usd),
        )
        self._projects[name] = proj
        self._save()
        return proj

    def list_projects(self) -> list[Project]:
        return list(self._projects.values())

    def rotate_key(self, name: str) -> Project:
        proj = self._require_active(name)
        proj.api_key = self._mint_key()
        proj.key_version += 1
        self._save()
        return proj

    def teardown(self, name: str) -> Project:
        proj = self._require_active(name)
        proj.status = "torn_down"
        proj.api_key = "revoked"
        self._save()
        return proj

    # ----- usage simulation -------------------------------------------
    def record_usage(self, name: str, amount_usd: float) -> Project:
        """Accrue mock spend and auto-suspend when the cap is hit."""
        proj = self._require_active(name)
        proj.usage_usd += float(amount_usd)
        if proj.usage_usd >= proj.spend_cap_usd:
            proj.status = "suspended"
        self._save()
        return proj


if __name__ == "__main__":  # tiny manual smoke test
    b = Backend(Path("/tmp/_sp_demo_state.json"))
    p = b.provision("demo-mem", "supermemory", spend_cap_usd=10)
    print("provisioned:", json.dumps(p.public_view(), indent=2))
    b.record_usage("demo-mem", 3.5)
    print("after usage:", json.dumps(b._require_active("demo-mem").public_view(), indent=2))
