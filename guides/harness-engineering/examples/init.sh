#!/usr/bin/env bash
# Harness init — run at every agent session start
set -euo pipefail

echo "==> install"
npm ci --prefer-offline 2>/dev/null || npm install

echo "==> health check"
npm run typecheck
npm test -- --passWithNoTests 2>/dev/null || npm test

echo "==> harness state"
test -f feature_list.json || { echo "missing feature_list.json"; exit 1; }
test -f AGENTS.md || { echo "missing AGENTS.md"; exit 1; }

echo "OK — environment ready. Read claude-progress.md then pick ONE feature."
