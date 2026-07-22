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
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
MODE="symlink"
TARGET="codex"
FORCE=0
BACKUP_STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
SAFETY_HOME="${NAIVE_VIDEO_SAFETY_HOME:-$HOME/.naive-video-skill}"

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
  echo "$SCRIPT_DIR"
}

target_id() {
  local target_dir="$1"
  if [[ "$target_dir" == "$HOME/.codex/skills" ]]; then
    echo "codex"
  elif [[ "$target_dir" == "$HOME/.claude/skills" ]]; then
    echo "claude"
  else
    echo "custom"
  fi
}

same_symlink() {
  local destination="$1"
  local source="$2"
  [[ "$MODE" == "symlink" && -L "$destination" ]] || return 1
  python3 - "$destination" "$source" <<'PY'
import sys
from pathlib import Path

destination, source = map(Path, sys.argv[1:])
raise SystemExit(0 if destination.resolve() == source.resolve() else 1)
PY
}

confirm_replacement() {
  local target_dir="$1"
  local source destination
  local needs_backup=0
  destination="$target_dir/$ROOT_SKILL"
  source="$(skill_source)"
  if [[ -e "$destination" || -L "$destination" ]]; then
    if ! same_symlink "$destination" "$source"; then
      needs_backup=1
    fi
  fi
  if [[ "$needs_backup" -eq 0 ]]; then
    local legacy
    for legacy in "${LEGACY_SKILLS[@]}"; do
      if [[ -e "$target_dir/$legacy" || -L "$target_dir/$legacy" ]]; then
        needs_backup=1
        break
      fi
    done
  fi
  [[ "$needs_backup" -eq 1 ]] || return 0
  [[ "$FORCE" -eq 1 ]] && return 0

  printf 'Existing Naive Video Skill files will be moved to a timestamped backup before installation. Continue? [y/N] '
  read -r answer
  [[ "$answer" =~ ^[Yy]$ ]]
}

archive_legacy_skills() {
  local target_dir="$1"
  local id backup_root
  id="$(target_id "$target_dir")"
  backup_root="$SAFETY_HOME/backups/$id/$BACKUP_STAMP/legacy"
  local legacy source
  for legacy in "${LEGACY_SKILLS[@]}"; do
    source="$target_dir/$legacy"
    if [[ -e "$source" || -L "$source" ]]; then
      mkdir -p "$backup_root"
      mv "$source" "$backup_root/$legacy"
      echo "Archived legacy skill entry: $source -> $backup_root/$legacy"
    fi
  done
}

install_one() {
  local target_dir="$1"
  local name="$2"
  local source backup backup_root failed_root
  local destination="$target_dir/$name"
  source="$(skill_source)"
  local id
  id="$(target_id "$target_dir")"
  backup_root="$SAFETY_HOME/backups/$id/$BACKUP_STAMP"
  failed_root="$SAFETY_HOME/failed/$id/$BACKUP_STAMP"
  backup=""

  if [[ -e "$destination" || -L "$destination" ]]; then
    if same_symlink "$destination" "$source"; then
      echo "Already installed: $destination"
      return 0
    fi
    mkdir -p "$backup_root"
    backup="$backup_root/$name"
    mv "$destination" "$backup"
    echo "Backed up: $destination -> $backup"
  fi

  if [[ "$MODE" == "copy" ]]; then
    if ! python3 "$SCRIPT_DIR/tools/install_copy.py" "$source" "$destination"; then
      echo "ERROR: copy installation failed for $name" >&2
      if [[ -e "$destination" || -L "$destination" ]]; then
        mkdir -p "$failed_root"
        mv "$destination" "$failed_root/$name"
      fi
      if [[ -n "$backup" && ( -e "$backup" || -L "$backup" ) ]]; then
        mv "$backup" "$destination"
        echo "Restored previous installation: $destination"
      fi
      return 1
    fi
  else
    if ! ln -s "$source" "$destination"; then
      echo "ERROR: symlink installation failed for $name" >&2
      if [[ -n "$backup" && ( -e "$backup" || -L "$backup" ) ]]; then
        mv "$backup" "$destination"
        echo "Restored previous installation: $destination"
      fi
      return 1
    fi
  fi
  echo "Installed: $destination"
}

install_target() {
  local label="$1"
  local target_dir="$2"
  mkdir -p "$target_dir"
  echo "Installing for $label in $MODE mode"
  echo "Safety: existing installations are backed up, never bulk-deleted."
  if ! confirm_replacement "$target_dir"; then
    echo "Installation cancelled for $label; existing files were not changed."
    return 0
  fi
  archive_legacy_skills "$target_dir"
  install_one "$target_dir" "$ROOT_SKILL"
}

if [[ "$TARGET" == "codex" || "$TARGET" == "all" ]]; then
  install_target "Codex" "$HOME/.codex/skills"
fi
if [[ "$TARGET" == "claude" || "$TARGET" == "all" ]]; then
  install_target "Claude Code" "$HOME/.claude/skills"
fi

echo
echo "Install complete. Restart the agent if the skills do not appear."
echo "Existing installations, if any, were preserved outside skill discovery under $SAFETY_HOME/backups/."
echo "First prompt: 用 \$talking-head-video-pipeline 初始化视频项目，这是主视频：<path>"
