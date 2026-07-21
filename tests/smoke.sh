#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." >/dev/null 2>&1 && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

python3 -m py_compile "$ROOT_DIR"/tools/*.py
python3 "$ROOT_DIR/tools/validate_skill.py" "$ROOT_DIR"

mkdir -p "$TMP_DIR/project"
printf 'not a real video\n' > "$TMP_DIR/source.mp4"
python3 "$ROOT_DIR/tools/bootstrap.py" \
  --project "$TMP_DIR/project" \
  --video "$TMP_DIR/source.mp4" \
  --mode quick

test -f "$TMP_DIR/project/.naive-video-state.json"
test -f "$TMP_DIR/project/EDIT_PLAN.md"
test -f "$TMP_DIR/project/DESIGN.md"
test -f "$TMP_DIR/project/VIDEO_LESSONS.md"
test -f "$TMP_DIR/project/VIDEO_RETRO.md"

cat > "$TMP_DIR/project/edit/script-aligned.srt" <<'EOF'
1
00:00:00,000 --> 00:00:01,200
Hello world

2
00:00:01,200 --> 00:00:02,800
Second caption
EOF

cat > "$TMP_DIR/project/edit/caption-table.csv" <<'EOF'
index,start,end,duration,text
1,0.000,1.200,1.200,Hello world
2,1.200,2.800,1.600,Second caption
EOF

python3 "$ROOT_DIR/tools/caption_check.py" \
  "$TMP_DIR/project/edit/script-aligned.srt" \
  "$TMP_DIR/project/edit/caption-table.csv"

python3 "$ROOT_DIR/tools/state.py" --project "$TMP_DIR/project" stage captions_ready
python3 "$ROOT_DIR/tools/state.py" --project "$TMP_DIR/project" show >/dev/null
python3 "$ROOT_DIR/tools/video_doctor.py" --project "$TMP_DIR/project" > "$TMP_DIR/doctor.log" 2>&1 || true
grep -q "stage: captions_ready" "$TMP_DIR/doctor.log"
grep -q "Summary:" "$TMP_DIR/doctor.log"

HOME="$TMP_DIR/profile-home" python3 "$ROOT_DIR/tools/profile.py" init
HOME="$TMP_DIR/profile-home" python3 "$ROOT_DIR/tools/profile.py" add-rule \
  --stage preview \
  --rule "Keep screenshot text readable"
HOME="$TMP_DIR/profile-home" python3 "$ROOT_DIR/tools/profile.py" apply \
  --project "$TMP_DIR/project"
grep -q "Keep screenshot text readable" "$TMP_DIR/project/VIDEO_LESSONS.md"

HOME="$TMP_DIR/profile-home" python3 "$ROOT_DIR/tools/bootstrap.py" \
  --project "$TMP_DIR/profile-project" \
  --video "$TMP_DIR/source.mp4" \
  --mode quick
grep -q "Keep screenshot text readable" "$TMP_DIR/profile-project/VIDEO_LESSONS.md"

HOME="$TMP_DIR/home" bash "$ROOT_DIR/install.sh" --codex --copy --force
test -f "$TMP_DIR/home/.codex/skills/talking-head-video-pipeline/SKILL.md"
test -f "$TMP_DIR/home/.codex/skills/naive-video-init/SKILL.md"
test -f "$TMP_DIR/home/.codex/skills/naive-video-design/SKILL.md"
test -f "$TMP_DIR/home/.codex/skills/naive-video-retro/SKILL.md"

echo "Smoke test passed."
