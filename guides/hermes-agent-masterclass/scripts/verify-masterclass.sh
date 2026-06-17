#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
echo "Hermes Agent Masterclass — verify"
for f in README.md TUTORIAL.md examples/SOUL-designer.md; do
  [[ -f "$ROOT/$f" ]] && echo "  ✓ $f" || { echo "  ✗ $f"; exit 1; }
done
echo "OK"
