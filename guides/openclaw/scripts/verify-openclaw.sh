#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
echo "OpenClaw guide — verify"
for f in README.md TUTORIAL.md examples/SOUL.md; do
  [[ -f "$ROOT/$f" ]] && echo "  ✓ $f" || { echo "  ✗ missing $f"; exit 1; }
done
command -v openclaw >/dev/null 2>&1 && echo "  ✓ openclaw on PATH" || echo "  ⚠ openclaw not installed (optional)"
echo "OK"
