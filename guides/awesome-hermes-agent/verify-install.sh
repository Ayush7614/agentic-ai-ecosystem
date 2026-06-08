#!/usr/bin/env bash
# Verify Hermes Agent CLI is installed and healthy.
set -euo pipefail

echo "==> Hermes install check"
command -v hermes >/dev/null || {
  echo "FAIL: hermes not found. Run:"
  echo "  curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash"
  exit 1
}

hermes --version 2>/dev/null || hermes version 2>/dev/null || true
echo "OK: hermes on PATH ($(command -v hermes))"

echo ""
echo "==> hermes doctor"
if hermes doctor; then
  echo "OK: doctor passed"
else
  echo "WARN: doctor reported issues — run hermes setup or hermes model"
  exit 1
fi

echo ""
echo "==> Config directory"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
if [[ -d "$HERMES_HOME" ]]; then
  echo "OK: $HERMES_HOME exists"
  ls -la "$HERMES_HOME" 2>/dev/null | head -12 || true
else
  echo "WARN: $HERMES_HOME not found yet — run hermes once to initialize"
fi

echo ""
echo "All checks done."
