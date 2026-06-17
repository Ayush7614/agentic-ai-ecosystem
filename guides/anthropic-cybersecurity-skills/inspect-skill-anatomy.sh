#!/usr/bin/env bash
# Part 11 — inspect a real skill from the upstream library (read-only).
set -euo pipefail

REPO="${CYBERSEC_SKILLS_DIR:-${HOME}/.cybersec-skills/Anthropic-Cybersecurity-Skills}"
SKILL_NAME="${1:-performing-memory-forensics-with-volatility3}"
SKILL="${REPO}/skills/${SKILL_NAME}"

echo "==> Skill anatomy demo (real files from upstream repo)"
echo "    Repo:  ${REPO}"
echo "    Skill: ${SKILL_NAME}"
echo ""

if [[ ! -d "${REPO}/.git" ]]; then
  echo "Clone not found. Run ./install-skills.sh first."
  exit 1
fi

if [[ ! -f "${SKILL}/SKILL.md" ]]; then
  echo "Skill not found: ${SKILL}"
  exit 1
fi

echo "── Directory layout ──"
ls -la "${SKILL}"
echo ""
find "${SKILL}" -maxdepth 2 -type f | sed "s|${SKILL}/||" | sort
echo ""

echo "── YAML frontmatter (first 22 lines) ──"
sed -n '1,22p' "${SKILL}/SKILL.md"
echo ""

echo "── Markdown sections ──"
grep '^## ' "${SKILL}/SKILL.md"
echo ""

echo "── Workflow preview (first 12 lines) ──"
sed -n '/^## Workflow/,/^## /p' "${SKILL}/SKILL.md" | head -12
echo ""
echo "Done. This is read-only inspection — no memory dump or Volatility execution."
