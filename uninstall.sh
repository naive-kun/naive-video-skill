#!/usr/bin/env bash
set -euo pipefail

SKILLS=(
  talking-head-video-pipeline
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
TARGET="codex"

for arg in "$@"; do
  case "$arg" in
    --codex) TARGET="codex" ;;
    --claude) TARGET="claude" ;;
    --all) TARGET="all" ;;
    -h|--help) echo "Usage: bash uninstall.sh [--codex|--claude|--all]"; exit 0 ;;
    *) echo "Unknown option: $arg"; exit 2 ;;
  esac
done

remove_from() {
  local target_dir="$1"
  for name in "${SKILLS[@]}"; do
    if [[ -e "$target_dir/$name" || -L "$target_dir/$name" ]]; then
      rm -rf "$target_dir/$name"
      echo "Removed: $target_dir/$name"
    fi
  done
}

if [[ "$TARGET" == "codex" || "$TARGET" == "all" ]]; then
  remove_from "$HOME/.codex/skills"
fi
if [[ "$TARGET" == "claude" || "$TARGET" == "all" ]]; then
  remove_from "$HOME/.claude/skills"
fi

echo "Uninstall complete. User video projects were not touched."
