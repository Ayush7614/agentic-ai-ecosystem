#!/usr/bin/env bash
# Use Node 22+ for OpenClaw in this shell (required: >= 22.12.0).
set -euo pipefail

export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
if [[ -s "$NVM_DIR/nvm.sh" ]]; then
  # shellcheck source=/dev/null
  . "$NVM_DIR/nvm.sh"
  nvm use "$(cat "$(dirname "$0")/.nvmrc")"
else
  echo "nvm not found. Install Node 22+ from https://nodejs.org/" >&2
  exit 1
fi

echo "Node: $(node -v)"
echo "OpenClaw: $(openclaw --version 2>/dev/null || echo 'not in PATH — npm i -g openclaw@latest')"
