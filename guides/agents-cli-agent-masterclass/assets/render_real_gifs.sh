#!/usr/bin/env bash
# Record REAL terminal GIFs via VHS (charmbracelet/vhs).
# Every GIF runs actual uvx google-agents-cli commands — no HTML mockups.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
TAPES="$ROOT/tapes"
ASSETS="$ROOT"

if ! command -v vhs >/dev/null 2>&1; then
  echo "Install VHS: brew install vhs" >&2
  exit 1
fi

if ! command -v uvx >/dev/null 2>&1; then
  echo "Install uv: https://docs.astral.sh/uv/" >&2
  exit 1
fi

# Pre-warm uvx cache so tapes record faster
uvx google-agents-cli --version >/dev/null

for tape in step-01-install step-02-scaffold step-03-install-info \
            step-04-eval-metrics step-05-run-agent step-06-login mega-workflow; do
  echo "Recording $tape.tape …"
  (cd "$TAPES" && vhs "$tape.tape")
done

echo "Done. GIFs in $ASSETS"
ls -la "$ASSETS"/*.gif
