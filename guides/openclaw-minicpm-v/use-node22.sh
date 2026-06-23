#!/usr/bin/env bash
set -euo pipefail
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
if [[ -s "$NVM_DIR/nvm.sh" ]]; then
  . "$NVM_DIR/nvm.sh"
  nvm use "$(cat "$(dirname "$0")/.nvmrc")"
else
  echo "nvm not found — install Node 22+" >&2
  exit 1
fi
echo "Node: $(node -v)"
