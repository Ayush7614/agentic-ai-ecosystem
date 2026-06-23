#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SKILL_SRC="${ROOT}/skills/vision-photo"
GLOBAL=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    --global) GLOBAL=true; shift ;;
    *) echo "Usage: ./install-skill.sh [--global]" >&2; exit 1 ;;
  esac
done
if [[ "$GLOBAL" == true ]]; then
  DEST="${HOME}/.openclaw/skills/vision-photo"
else
  DEST="${OPENCLAW_WORKSPACE:-${HOME}/.openclaw/workspace}/skills/vision-photo"
fi
mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
cp -R "$SKILL_SRC" "$DEST"
chmod +x "${DEST}/scripts/"*.sh 2>/dev/null || true
echo "Installed vision-photo skill → ${DEST}"
