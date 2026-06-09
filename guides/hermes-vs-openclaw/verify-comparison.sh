#!/usr/bin/env bash
# Quick check: are OpenClaw and/or Hermes installed and healthy?
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ok()   { echo -e "${GREEN}✓${NC} $*"; }
warn() { echo -e "${YELLOW}!${NC} $*"; }
fail() { echo -e "${RED}✗${NC} $*"; }

echo "==> Hermes vs OpenClaw — install check"
echo

# Node (OpenClaw)
if command -v node >/dev/null 2>&1; then
  NODE_VER=$(node -v | sed 's/^v//')
  ok "Node $NODE_VER"
  MAJOR=$(echo "$NODE_VER" | cut -d. -f1)
  MINOR=$(echo "$NODE_VER" | cut -d. -f2)
  if [[ "$MAJOR" -lt 22 ]] || { [[ "$MAJOR" -eq 22 ]] && [[ "$MINOR" -lt 19 ]]; }; then
    warn "OpenClaw needs Node 22.19+ or 24 — see guides/openclaw-gemma-rag/use-node22.sh"
  fi
else
  warn "Node not found — required for OpenClaw"
fi

# OpenClaw
if command -v openclaw >/dev/null 2>&1; then
  ok "OpenClaw $(openclaw --version 2>/dev/null || echo 'installed')"
  if openclaw doctor >/dev/null 2>&1; then
    ok "openclaw doctor passed"
  else
    warn "openclaw doctor reported issues — run: openclaw doctor"
  fi
else
  warn "OpenClaw not installed — npm install -g openclaw@latest && openclaw onboard --install-daemon"
fi

# Hermes
if command -v hermes >/dev/null 2>&1; then
  ok "Hermes $(hermes --version 2>/dev/null || echo 'installed')"
  if hermes doctor >/dev/null 2>&1; then
    ok "hermes doctor passed"
  else
    warn "hermes doctor reported issues — run: hermes doctor"
  fi
else
  warn "Hermes not installed — curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash"
fi

echo
if command -v openclaw >/dev/null 2>&1 && command -v hermes >/dev/null 2>&1; then
  ok "Both CLIs present — ready for side-by-side comparison (Part 13 of TUTORIAL.md)"
else
  warn "Install missing stack(s) to complete hands-on comparison"
fi

echo
echo "Docs: guides/hermes-vs-openclaw/TUTORIAL.md"
