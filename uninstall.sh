#!/usr/bin/env bash
set -euo pipefail

ROOT_SKILL="talking-head-video-pipeline"
LEGACY_SKILLS=(
  naive-video-init
  naive-video-roughcut
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
ARCHIVE_STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
SAFETY_HOME="${NAIVE_VIDEO_SAFETY_HOME:-$HOME/.naive-video-skill}"

for arg in "$@"; do
  case "$arg" in
    --codex) TARGET="codex" ;;
    --claude) TARGET="claude" ;;
    --all) TARGET="all" ;;
    -h|--help) echo "Usage: bash uninstall.sh [--codex|--claude|--all]"; exit 0 ;;
    *) echo "Unknown option: $arg"; exit 2 ;;
  esac
done

archive_from() {
  local target_dir="$1"
  local source="$target_dir/$ROOT_SKILL"
  local id
  if [[ "$target_dir" == "$HOME/.codex/skills" ]]; then
    id="codex"
  elif [[ "$target_dir" == "$HOME/.claude/skills" ]]; then
    id="claude"
  else
    id="custom"
  fi
  local archive_root="$SAFETY_HOME/uninstalled/$id/$ARCHIVE_STAMP"
  local archive="$archive_root/$ROOT_SKILL"
  if [[ -e "$source" || -L "$source" ]]; then
    mkdir -p "$archive_root"
    mv "$source" "$archive"
    echo "Archived: $source -> $archive"
  else
    echo "Not installed: $source"
  fi

  local legacy legacy_source legacy_archive_root
  legacy_archive_root="$archive_root/legacy"
  for legacy in "${LEGACY_SKILLS[@]}"; do
    legacy_source="$target_dir/$legacy"
    if [[ -e "$legacy_source" || -L "$legacy_source" ]]; then
      mkdir -p "$legacy_archive_root"
      mv "$legacy_source" "$legacy_archive_root/$legacy"
      echo "Archived legacy entry: $legacy_source -> $legacy_archive_root/$legacy"
    fi
  done
}

if [[ "$TARGET" == "codex" || "$TARGET" == "all" ]]; then
  archive_from "$HOME/.codex/skills"
fi
if [[ "$TARGET" == "claude" || "$TARGET" == "all" ]]; then
  archive_from "$HOME/.claude/skills"
fi

echo "Uninstall complete. The installed skill was archived for recovery; user video projects were not touched."
