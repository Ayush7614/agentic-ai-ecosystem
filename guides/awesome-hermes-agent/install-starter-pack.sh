#!/usr/bin/env bash
# Install recommended starter skills into ~/.hermes/skills/
set -euo pipefail

SKILLS_DIR="${HERMES_SKILLS_DIR:-$HOME/.hermes/skills}"
mkdir -p "$SKILLS_DIR"

install_skill_repo() {
  local name="$1"
  local url="$2"
  local dest="$SKILLS_DIR/$name"
  if [[ -d "$dest/.git" ]]; then
    echo "SKIP: $name already installed — git pull in $dest"
    git -C "$dest" pull --ff-only || true
  else
    echo "CLONE: $name"
    git clone --depth 1 "$url" "$dest"
  fi
}

echo "Installing starter skills to: $SKILLS_DIR"
echo "(Hermes also creates skills from experience — these are community starters.)"
echo ""

# Cross-platform agentskills.io library (production on awesome list)
install_skill_repo "wondelai-skills" "https://github.com/wondelai/skills.git"

# Literate programming across agents (beta)
install_skill_repo "litprog-skill" "https://github.com/tlehman/litprog-skill.git"

echo ""
echo "Done. Restart Hermes or run: hermes skills  (if available)"
echo "List installed: ls -la $SKILLS_DIR"
