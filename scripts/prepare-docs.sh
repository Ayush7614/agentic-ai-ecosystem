#!/usr/bin/env bash
# Copy guide assets into docs/ so MkDocs can serve images referenced from included READMEs.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

for guide_dir in "$ROOT"/guides/*/; do
  [[ -d "$guide_dir" ]] || continue
  slug="$(basename "$guide_dir")"
  [[ "$slug" == "*" ]] && continue

  if [[ -d "$guide_dir/assets" ]]; then
    dest="$ROOT/docs/guides/$slug/assets"
    rm -rf "$dest"
    mkdir -p "$(dirname "$dest")"
    cp -r "$guide_dir/assets" "$dest"
    echo "Copied assets for guide: $slug"
  fi
done
