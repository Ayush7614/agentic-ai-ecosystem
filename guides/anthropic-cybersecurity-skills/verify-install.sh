#!/usr/bin/env bash
# Verify Anthropic Cybersecurity Skills clone and sample skill structure.
set -euo pipefail

INSTALL_DIR="${CYBERSEC_SKILLS_DIR:-${HOME}/.cybersec-skills/Anthropic-Cybersecurity-Skills}"
PASS=0
FAIL=0

ok()   { echo "  OK   $*"; PASS=$((PASS + 1)); }
bad()  { echo "  FAIL $*"; FAIL=$((FAIL + 1)); }

echo "==> verify-install.sh"
echo "    Dir: ${INSTALL_DIR}"
echo ""

if [[ ! -d "${INSTALL_DIR}" ]]; then
  echo "Clone not found. Run ./install-skills.sh first."
  exit 1
fi

[[ -d "${INSTALL_DIR}/skills" ]] && ok "skills/ directory exists" || bad "missing skills/"

SKILL_COUNT="$(find "${INSTALL_DIR}/skills" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')"
if [[ "${SKILL_COUNT}" -ge 700 ]]; then
  ok "skill count ${SKILL_COUNT} (expected ~754)"
else
  bad "skill count ${SKILL_COUNT} (expected ~754 — pull latest?)"
fi

SAMPLE="${INSTALL_DIR}/skills/performing-memory-forensics-with-volatility3/SKILL.md"
if [[ -f "${SAMPLE}" ]]; then
  ok "sample skill: performing-memory-forensics-with-volatility3"
  grep -q "^name:" "${SAMPLE}" && ok "  frontmatter: name" || bad "  missing name in frontmatter"
  grep -q "^description:" "${SAMPLE}" && ok "  frontmatter: description" || bad "  missing description"
  grep -q "## Workflow" "${SAMPLE}" && ok "  body: Workflow section" || bad "  missing Workflow section"
else
  bad "sample skill not found (repo layout may have changed)"
fi

README="${INSTALL_DIR}/README.md"
[[ -f "${README}" ]] && ok "README.md present" || bad "README.md missing"

echo ""
if [[ "${FAIL}" -eq 0 ]]; then
  echo "All checks passed (${PASS})."
  exit 0
else
  echo "${FAIL} check(s) failed, ${PASS} passed."
  exit 1
fi
