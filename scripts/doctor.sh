#!/usr/bin/env bash
set -u

if [[ "${1:-}" == "--privacy-scan" ]]; then
  target="${2:-.}"
  echo "Privacy scan target: $target"
  if ! command -v grep >/dev/null 2>&1; then
    echo "grep not found"
    exit 1
  fi
  patterns='(/Users/|/home/[^ <"]+|API[_-]?KEY|SECRET|TOKEN|PASSWORD|BEGIN [A-Z ]*PRIVATE KEY|\.env|Desktop/|Downloads/)'
  if grep -RInE "$patterns" "$target" \
    --exclude-dir=.git \
    --exclude-dir=node_modules \
    --exclude='.gitignore' \
    --exclude='CONTRIBUTING.md' \
    --exclude='doctor.sh' \
    --exclude='README.md' \
    --exclude='*.log' 2>/dev/null; then
    echo "Potential private strings found. Review before publishing."
    exit 2
  fi
  echo "No obvious private strings found."
  exit 0
fi

echo "Talking Head Video Pipeline environment check"
echo

check_cmd() {
  name="$1"
  cmd="$2"
  if command -v "$cmd" >/dev/null 2>&1; then
    printf "[ok]   %s: %s\n" "$name" "$(command -v "$cmd")"
  else
    printf "[miss] %s: command not found (%s)\n" "$name" "$cmd"
  fi
}

check_cmd "ffmpeg" "ffmpeg"
check_cmd "ffprobe" "ffprobe"
check_cmd "node" "node"
check_cmd "npm" "npm"
check_cmd "npx" "npx"

echo
echo "Optional renderer check:"
if command -v npx >/dev/null 2>&1; then
  echo "  HyperFrames can usually be run with: npx --yes hyperframes --help"
else
  echo "  npx missing; install Node.js/npm or use another renderer."
fi

echo
echo "Transcription check:"
echo "  This skill does not bundle ASR. Configure your preferred transcription tool/API,"
echo "  or provide an existing transcript, SRT, CSV, or transcript JSON."
