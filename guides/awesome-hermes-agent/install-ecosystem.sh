#!/usr/bin/env bash
# Install Hermes ecosystem layers: skills, plugins, tools, integrations, multi-agent.
# Usage: ./install-ecosystem.sh [skills|plugins|tools|integrations|multiagent|all]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="${HERMES_SKILLS_DIR:-$HOME/.hermes/skills}"
PLUGINS_DIR="${HERMES_PLUGINS_DIR:-$HOME/.hermes/plugins}"
TOOLS_DIR="${HERMES_TOOLS_DIR:-$HOME/.hermes/ecosystem-tools}"

clone_repo() {
  local name="$1"
  local url="$2"
  local dest="$3"
  mkdir -p "$(dirname "$dest")"
  if [[ -d "$dest/.git" ]]; then
    echo "SKIP: $name — pull $dest"
    git -C "$dest" pull --ff-only || true
  else
    echo "CLONE: $name -> $dest"
    git clone --depth 1 "$url" "$dest"
  fi
}

install_skills() {
  echo "=== Skills (procedural memory) -> $SKILLS_DIR"
  mkdir -p "$SKILLS_DIR"
  clone_repo "wondelai-skills" "https://github.com/wondelai/skills.git" "$SKILLS_DIR/wondelai-skills"
  clone_repo "litprog-skill" "https://github.com/tlehman/litprog-skill.git" "$SKILLS_DIR/litprog-skill"
  clone_repo "youtube-skills" "https://github.com/therohitdas/youtube-skills.git" "$SKILLS_DIR/youtube-skills"
  clone_repo "drawio-skill" "https://github.com/Agents365-ai/drawio-skill.git" "$SKILLS_DIR/drawio-skill"
  clone_repo "oh-my-hermes" "https://github.com/witt3rd/oh-my-hermes.git" "$SKILLS_DIR/oh-my-hermes"
  clone_repo "hermes-agent-acp-skill" "https://github.com/Rainhoole/hermes-agent-acp-skill.git" "$SKILLS_DIR/hermes-agent-acp-skill"
  echo "Optional large skill pack (753+ security skills):"
  echo "  git clone --depth 1 https://github.com/mukul975/Anthropic-Cybersecurity-Skills.git $SKILLS_DIR/cybersecurity-skills"
}

install_plugins() {
  echo "=== Plugins -> $PLUGINS_DIR"
  mkdir -p "$PLUGINS_DIR"
  clone_repo "hermes-web-search-plus" "https://github.com/robbyczgw-cla/hermes-web-search-plus.git" "$PLUGINS_DIR/hermes-web-search-plus"
  clone_repo "rtk-hermes" "https://github.com/ogallotti/rtk-hermes.git" "$PLUGINS_DIR/rtk-hermes"
  clone_repo "mnemo-hermes" "https://github.com/hernanqwz/mnemo-hermes.git" "$PLUGINS_DIR/mnemo-hermes"
  clone_repo "hermes-curator-evolver" "https://github.com/pingchesu/hermes-curator-evolver.git" "$PLUGINS_DIR/hermes-curator-evolver"
  clone_repo "evey-bridge-plugin" "https://github.com/42-evey/evey-bridge-plugin.git" "$PLUGINS_DIR/evey-bridge-plugin"
  echo "Enable plugins in Hermes config — see TUTORIAL Part 4.4"
}

install_tools() {
  echo "=== Tools & utilities -> $TOOLS_DIR"
  mkdir -p "$TOOLS_DIR"
  clone_repo "hermes-workspace" "https://github.com/outsourc-e/hermes-workspace.git" "$TOOLS_DIR/hermes-workspace"
  clone_repo "mission-control" "https://github.com/builderz-labs/mission-control.git" "$TOOLS_DIR/mission-control"
  clone_repo "SkillClaw" "https://github.com/AMAP-ML/SkillClaw.git" "$TOOLS_DIR/SkillClaw"
  clone_repo "lintlang" "https://github.com/roli-lpci/lintlang.git" "$TOOLS_DIR/lintlang"
  clone_repo "agenttrace" "https://github.com/luoyuctl/agenttrace.git" "$TOOLS_DIR/agenttrace"
  clone_repo "camofox-browser" "https://github.com/jo-inc/camofox-browser.git" "$TOOLS_DIR/camofox-browser"
  echo "Each tool has its own README — follow upstream install inside $TOOLS_DIR/<name>"
}

install_integrations() {
  echo "=== Integrations & bridges -> $SKILLS_DIR + $PLUGINS_DIR + $TOOLS_DIR"
  mkdir -p "$SKILLS_DIR" "$PLUGINS_DIR" "$TOOLS_DIR"
  clone_repo "microsoft-workspace-skill" "https://github.com/Andrew-Girgis/microsoft-workspace-skill.git" "$SKILLS_DIR/microsoft-workspace-skill"
  clone_repo "hindsight-plugin" "https://github.com/vectorize-io/hindsight.git" "$PLUGINS_DIR/hindsight"
  clone_repo "honcho-self-hosted" "https://github.com/elkimek/honcho-self-hosted.git" "$TOOLS_DIR/honcho-self-hosted"
  clone_repo "MeiGen-AI-Design-MCP" "https://github.com/jau123/MeiGen-AI-Design-MCP.git" "$TOOLS_DIR/MeiGen-AI-Design-MCP"
  clone_repo "mistral-mcp" "https://github.com/Swih/mistral-mcp.git" "$TOOLS_DIR/mistral-mcp"
  echo "Wire MCP servers in Hermes config — see TUTORIAL Part 6"
}

install_multiagent() {
  echo "=== Multi-agent & swarms -> $SKILLS_DIR + $TOOLS_DIR"
  mkdir -p "$SKILLS_DIR" "$TOOLS_DIR"
  clone_repo "oh-my-hermes" "https://github.com/witt3rd/oh-my-hermes.git" "$SKILLS_DIR/oh-my-hermes"
  clone_repo "hermes-agent-acp-skill" "https://github.com/Rainhoole/hermes-agent-acp-skill.git" "$SKILLS_DIR/hermes-agent-acp-skill"
  clone_repo "opencode-hermes-multiagent" "https://github.com/1ilkhamov/opencode-hermes-multiagent.git" "$TOOLS_DIR/opencode-hermes-multiagent"
  clone_repo "bigiron" "https://github.com/supermodeltools/bigiron.git" "$TOOLS_DIR/bigiron"
  clone_repo "zouroboros-swarm-executors" "https://github.com/marlandoj/zouroboros-swarm-executors.git" "$TOOLS_DIR/zouroboros-swarm-executors"
  echo "Pair with mission-control for fleet visibility — ./install-ecosystem.sh tools"
}

usage() {
  cat <<EOF
Usage: $0 [skills|plugins|tools|integrations|multiagent|all]

Layers map to TUTORIAL Parts 4–7:
  skills        Community + agentskills.io skills
  plugins       Search, memory, curator, bridges
  tools         GUIs, SkillClaw, lintlang, camofox
  integrations  MCP, M365, hindsight, honcho
  multiagent    oh-my-hermes, ACP skill, swarm executors
  all           Run every layer (large download)
EOF
}

main() {
  local target="${1:-all}"
  case "$target" in
    skills) install_skills ;;
    plugins) install_plugins ;;
    tools) install_tools ;;
    integrations) install_integrations ;;
    multiagent) install_multiagent ;;
    all)
      install_skills
      install_plugins
      install_tools
      install_integrations
      install_multiagent
      ;;
    -h|--help) usage; exit 0 ;;
    *) usage; exit 1 ;;
  esac
  echo ""
  echo "Done. Run: hermes doctor && hermes --tui"
}

main "$@"
