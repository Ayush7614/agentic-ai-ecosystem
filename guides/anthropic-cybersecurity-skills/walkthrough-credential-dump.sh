#!/usr/bin/env bash
# Part 13 — credential theft memory dump walkthrough (lab-safe).
# Real: skill discovery + prerequisites + workflow commands from upstream SKILL.md
# Optional: set MEMORY_IMAGE=/path/to/server01.raw and install volatility3 to execute vol.*
set -euo pipefail

REPO="${CYBERSEC_SKILLS_DIR:-${HOME}/.cybersec-skills/Anthropic-Cybersecurity-Skills}"
SKILLS="${REPO}/skills"
IMAGE="${MEMORY_IMAGE:-server01.raw}"

SKILL_A="performing-memory-forensics-with-volatility3"
SKILL_B="extracting-credentials-from-memory-dump"
SKILL_C="detecting-credential-dumping-techniques"

echo "==> Part 13: Credential theft in a memory dump"
echo "    Scenario: suspected Mimikatz · image: ${IMAGE}"
echo "    Repo: ${REPO}"
echo ""

if [[ ! -d "${SKILLS}" ]]; then
  echo "Clone not found. Run ./install-skills.sh first."
  exit 1
fi

echo "── Step 1: Discover skills (real frontmatter scan) ──"
echo "Tags: memory-forensics, credential-dumping, lsass, dfir"
MATCHES="$(rg -l "memory-forensics|credential-dump|lsass" "${SKILLS}"/*/SKILL.md 2>/dev/null | wc -l | tr -d ' ')"
echo "  Matched ${MATCHES} skills in library"
echo "  Top picks for this incident:"
for s in "${SKILL_A}" "${SKILL_B}" "${SKILL_C}"; do
  if [[ -f "${SKILLS}/${s}/SKILL.md" ]]; then
    desc="$(rg "^description:" "${SKILLS}/${s}/SKILL.md" | head -1 | sed 's/description: //' | cut -c1-72)"
    echo "    • ${s}"
    echo "      ${desc}…"
  fi
done
echo ""

echo "── Step 2: Prerequisites (from SKILL.md) ──"
for s in "${SKILL_A}" "${SKILL_B}"; do
  echo "  [${s}]"
  sed -n '/^## Prerequisites/,/^## /p' "${SKILLS}/${s}/SKILL.md" | grep -E "^- " | head -4 | sed 's/^/    /'
done
echo ""

echo "── Step 3: Workflow execution ──"
VOL=""
if command -v vol >/dev/null 2>&1; then
  VOL="vol"
elif command -v vol3 >/dev/null 2>&1; then
  VOL="vol3"
fi

if [[ -n "${VOL}" && -f "${IMAGE}" ]]; then
  echo "  Volatility found · running against ${IMAGE}"
  "${VOL}" -f "${IMAGE}" windows.info 2>&1 | head -8
  echo "  …"
  "${VOL}" -f "${IMAGE}" windows.pslist 2>&1 | rg -i "lsass|mimikatz|powershell" | head -5 || true
else
  if [[ -z "${VOL}" ]]; then
    echo "  Volatility3 not installed (lab optional: pip install volatility3)"
  fi
  if [[ ! -f "${IMAGE}" ]]; then
    echo "  Memory image not found: ${IMAGE}"
    echo "  Lab: export MEMORY_IMAGE=/path/to/your/server01.raw"
  fi
  echo ""
  echo "  Commands from ${SKILL_B} (real SKILL.md workflow):"
  echo "    vol -f ${IMAGE} windows.info"
  echo "    vol -f ${IMAGE} windows.pslist | grep -i lsass"
  echo "    vol -f ${IMAGE} windows.malfind | head -20"
  echo "    vol -f ${IMAGE} windows.hashdump"
fi
echo ""

echo "── Step 4: Verification checklist ──"
echo "  □ Process accessed lsass.exe with suspicious GrantedAccess (Sysmon 10)"
echo "  □ malfind / injection artifacts near credential dump tools"
echo "  □ Timeline aligns with alert window"
echo "  □ ATT&CK mapped: T1003.001 — OS Credential Dumping: LSASS Memory"
echo ""

echo "── Step 5: Detection correlation (${SKILL_C}) ──"
rg -n "Event ID 10|4656|4663|T1003" "${SKILLS}/${SKILL_C}/SKILL.md" 2>/dev/null | head -4 | sed 's/^/    /' || true
echo ""
echo "Done. Authorized DFIR only · chain of custody required."
