#!/usr/bin/env bash
# Copy the sample .claude/ project layout into the current directory.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
DEST="${1:-.}"

if [[ -f "$DEST/CLAUDE.md" ]] || [[ -d "$DEST/.claude" ]]; then
  echo "Refusing to overwrite existing CLAUDE.md or .claude/ in: $DEST"
  echo "Remove or rename them first, or pass a different target directory."
  exit 1
fi

mkdir -p "$DEST"
cp "$ROOT/template/CLAUDE.md" "$DEST/"
cp -R "$ROOT/template/.claude" "$DEST/"

if [[ ! -f "$DEST/CLAUDE.local.md" ]]; then
  cp "$ROOT/template/CLAUDE.local.md.example" "$DEST/CLAUDE.local.md"
  echo "Created CLAUDE.local.md from example (gitignore this file)."
fi

if [[ ! -f "$DEST/.claude/settings.local.json" ]]; then
  cp "$ROOT/template/.claude/settings.local.json.example" "$DEST/.claude/settings.local.json"
  echo "Created .claude/settings.local.json from example (gitignore this file)."
fi

SNIP="$ROOT/template/gitignore.snippet"
if [[ -f "$DEST/.gitignore" ]]; then
  if ! grep -q 'CLAUDE.local.md' "$DEST/.gitignore" 2>/dev/null; then
    echo "" >> "$DEST/.gitignore"
    cat "$SNIP" >> "$DEST/.gitignore"
    echo "Appended Claude gitignore lines to .gitignore"
  fi
else
  cp "$SNIP" "$DEST/.gitignore"
  echo "Created .gitignore with Claude local-file entries"
fi

echo "Done. Project Claude layout installed in: $(cd "$DEST" && pwd)"
echo "Next: cd there and run: claude"
