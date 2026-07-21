#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
ROOT_DIR="$(cd -- "$SCRIPT_DIR/.." >/dev/null 2>&1 && pwd)"

if [[ "${1:-}" == "--privacy-scan" ]]; then
  target="${2:-.}"
  exec python3 "$ROOT_DIR/tools/validate_skill.py" --privacy-only "$target"
fi

if [[ "${1:-}" == "--project" ]]; then
  project="${2:-}"
  if [[ -z "$project" ]]; then
    echo "Usage: bash scripts/doctor.sh --project <project_dir>"
    exit 2
  fi
  exec python3 "$ROOT_DIR/tools/video_doctor.py" --project "$project"
fi

echo "Naive Video Skill environment check"
echo

missing_required=0
check_required() {
  local command="$1"
  if command -v "$command" >/dev/null 2>&1; then
    printf '[ok]   %-10s %s\n' "$command" "$(command -v "$command")"
  else
    printf '[miss] %-10s required\n' "$command"
    missing_required=1
  fi
}

check_optional() {
  local command="$1"
  if command -v "$command" >/dev/null 2>&1; then
    printf '[ok]   %-10s %s\n' "$command" "$(command -v "$command")"
  else
    printf '[note] %-10s optional for preview/rendering\n' "$command"
  fi
}

check_required python3
check_required ffmpeg
check_required ffprobe
check_optional node
check_optional npm
check_optional npx
check_optional whisper

echo
if [[ "$missing_required" -eq 1 ]]; then
  echo "Install missing tools, then run this check again."
  case "$(uname -s)" in
    Darwin) echo "macOS hint: brew install ffmpeg python node" ;;
    Linux) echo "Linux hint: use your package manager to install ffmpeg, python3, and nodejs/npm" ;;
  esac
  exit 1
fi

echo "Required environment is ready."
echo "Next: initialize a project with the main skill or run tools/bootstrap.py."
