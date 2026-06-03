#!/usr/bin/env bash
# Install the agentic-rag skill into the OpenClaw workspace (or --global managed dir).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
SKILL_SRC="${ROOT}/skills/agentic-rag"
GLOBAL=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --global) GLOBAL=true; shift ;;
    -h|--help)
      echo "Usage: ./install-skill.sh [--global]"
      echo "  default: ~/.openclaw/workspace/skills/agentic-rag"
      echo "  --global: ~/.openclaw/skills/agentic-rag"
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

if [[ ! -f "${SKILL_SRC}/SKILL.md" ]]; then
  echo "Missing ${SKILL_SRC}/SKILL.md" >&2
  exit 1
fi

if [[ "$GLOBAL" == true ]]; then
  DEST="${HOME}/.openclaw/skills/agentic-rag"
else
  DEST="${OPENCLAW_WORKSPACE:-${HOME}/.openclaw/workspace}/skills/agentic-rag"
fi

mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
cp -R "$SKILL_SRC" "$DEST"
chmod +x "${DEST}/scripts/"*.sh 2>/dev/null || true

echo "Installed agentic-rag skill to: ${DEST}"
echo "Enable in ~/.openclaw/openclaw.json (see config/openclaw.snippet.json5)"
echo "Restart gateway: openclaw gateway restart"
