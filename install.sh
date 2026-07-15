#!/usr/bin/env bash
set -euo pipefail

SUB_SKILLS=(
  naive-video-init
  naive-video-captions
  naive-video-design
  naive-video-preview
  naive-video-export
  naive-video-revise
  naive-video-status
  naive-video-doctor
  naive-video-learn
  naive-video-retro
  naive-video-migrate
)
ROOT_SKILL="talking-head-video-pipeline"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
MODE="symlink"
TARGET="codex"
FORCE=0

usage() {
  echo "Usage: bash install.sh [--codex|--claude|--all] [--copy] [--force]"
}

for arg in "$@"; do
  case "$arg" in
    --codex) TARGET="codex" ;;
    --claude) TARGET="claude" ;;
    --all) TARGET="all" ;;
    --copy) MODE="copy" ;;
    --force) FORCE=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $arg"; usage; exit 2 ;;
  esac
done

python3 "$SCRIPT_DIR/tools/validate_skill.py" "$SCRIPT_DIR"

skill_source() {
  local name="$1"
  if [[ "$name" == "$ROOT_SKILL" ]]; then
    echo "$SCRIPT_DIR"
  else
    echo "$SCRIPT_DIR/skills/$name"
  fi
}

install_one() {
  local target_dir="$1"
  local name="$2"
  local source
  local destination="$target_dir/$name"
  source="$(skill_source "$name")"

  if [[ -e "$destination" || -L "$destination" ]]; then
    if [[ "$FORCE" -ne 1 ]]; then
      printf 'Replace existing %s? [y/N] ' "$destination"
      read -r answer
      [[ "$answer" =~ ^[Yy]$ ]] || return 0
    fi
    rm -rf "$destination"
  fi

  if [[ "$MODE" == "copy" ]]; then
    cp -R "$source" "$destination"
    rm -rf "$destination/.git"
  else
    ln -s "$source" "$destination"
  fi
  echo "Installed: $destination"
}

install_target() {
  local label="$1"
  local target_dir="$2"
  mkdir -p "$target_dir"
  echo "Installing for $label in $MODE mode"
  install_one "$target_dir" "$ROOT_SKILL"
  for name in "${SUB_SKILLS[@]}"; do
    install_one "$target_dir" "$name"
  done
}

if [[ "$TARGET" == "codex" || "$TARGET" == "all" ]]; then
  install_target "Codex" "$HOME/.codex/skills"
fi
if [[ "$TARGET" == "claude" || "$TARGET" == "all" ]]; then
  install_target "Claude Code" "$HOME/.claude/skills"
fi

echo
echo "Install complete. Restart the agent if the skills do not appear."
echo "First prompt: 用 \$talking-head-video-pipeline 初始化视频项目，这是主视频：<path>"
