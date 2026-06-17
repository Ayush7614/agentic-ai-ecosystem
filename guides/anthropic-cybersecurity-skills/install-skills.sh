#!/usr/bin/env bash
# Clone Anthropic Cybersecurity Skills for local agent use.
set -euo pipefail

REPO_URL="${CYBERSEC_SKILLS_REPO:-https://github.com/mukul975/Anthropic-Cybersecurity-Skills.git}"
INSTALL_DIR="${CYBERSEC_SKILLS_DIR:-${HOME}/.cybersec-skills/Anthropic-Cybersecurity-Skills}"

echo "==> Anthropic Cybersecurity Skills installer"
echo "    Repo:  ${REPO_URL}"
echo "    Dir:   ${INSTALL_DIR}"

if command -v npx >/dev/null 2>&1; then
  echo ""
  echo "Tip: npx skills add mukul975/Anthropic-Cybersecurity-Skills"
  echo "     installs into your agent's skills path automatically."
  echo ""
fi

mkdir -p "$(dirname "${INSTALL_DIR}")"

if [[ -d "${INSTALL_DIR}/.git" ]]; then
  echo "==> Existing clone — pulling latest"
  git -C "${INSTALL_DIR}" pull --ff-only
else
  echo "==> Cloning"
  git clone "${REPO_URL}" "${INSTALL_DIR}"
fi

SKILL_COUNT="$(find "${INSTALL_DIR}/skills" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')"
echo ""
echo "==> Done. ${SKILL_COUNT} skill directories under skills/"
echo ""
echo "Point your agent at: ${INSTALL_DIR}/skills"
echo ""
echo "Examples:"
echo "  Claude Code:  ln -sf ${INSTALL_DIR}/skills/* ~/.claude/skills/  # or copy subsets"
echo "  Cursor:       Settings → Rules → add skill paths, or symlink to ~/.cursor/skills/"
echo "  Hermes:       cp -r ${INSTALL_DIR}/skills/* ~/.hermes/skills/"
echo ""
echo "Run ./verify-install.sh to validate."
