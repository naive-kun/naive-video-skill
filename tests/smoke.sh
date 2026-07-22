#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." >/dev/null 2>&1 && pwd)"
TMP_DIR="$(mktemp -d)"

python3 -m py_compile "$ROOT_DIR"/tools/*.py
python3 "$ROOT_DIR/tools/validate_skill.py" "$ROOT_DIR"
test "$(find "$ROOT_DIR" -name SKILL.md -not -path '*/.git/*' | wc -l | tr -d ' ')" = "1"

mkdir -p "$TMP_DIR/project"
printf 'not a real video\n' > "$TMP_DIR/source.mp4"
HOME="$TMP_DIR/initial-home" python3 "$ROOT_DIR/tools/bootstrap.py" \
  --project "$TMP_DIR/project" \
  --video "$TMP_DIR/source.mp4" \
  --mode quick

test -f "$TMP_DIR/project/.naive-video-state.json"
test -f "$TMP_DIR/project/EDIT_PLAN.md"
test -f "$TMP_DIR/project/DESIGN.md"
test -f "$TMP_DIR/project/VIDEO_LESSONS.md"
test -f "$TMP_DIR/project/VIDEO_RETRO.md"

python3 "$ROOT_DIR/tools/design_check.py" "$TMP_DIR/project/DESIGN.md"
cp "$TMP_DIR/project/DESIGN.md" "$TMP_DIR/invalid-design.md"
python3 - "$TMP_DIR/invalid-design.md" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
path.write_text(
    text.replace("Display weight: 700 bold", "Display weight: 400 regular"),
    encoding="utf-8",
)
PY
if python3 "$ROOT_DIR/tools/design_check.py" "$TMP_DIR/invalid-design.md"; then
  echo "Expected thin display weight failure" >&2
  exit 1
fi

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
printf 'approved rough cut\n' > "$TMP_DIR/project/edit/rough-cut.mp4"
python3 "$ROOT_DIR/tools/state.py" --project "$TMP_DIR/project" \
  working-video "$TMP_DIR/project/edit/rough-cut.mp4"
python3 "$ROOT_DIR/tools/state.py" --project "$TMP_DIR/project" show > "$TMP_DIR/state.json"
grep -q '"master_audio": "working_video"' "$TMP_DIR/state.json"
grep -q '"rough_cut"' "$TMP_DIR/state.json"
python3 "$ROOT_DIR/tools/video_doctor.py" --project "$TMP_DIR/project" > "$TMP_DIR/doctor.log" 2>&1 || true
grep -q "stage: captions_ready" "$TMP_DIR/doctor.log"
grep -q "working video:" "$TMP_DIR/doctor.log"
grep -q "Summary:" "$TMP_DIR/doctor.log"

mkdir -p "$TMP_DIR/gsap/minified"
cat > "$TMP_DIR/gsap/minified/gsap.min.js" <<'EOF'
/*! GSAP 3.15.0 @license test-only fixture */
EOF
cat > "$TMP_DIR/gsap/minified/SplitText.min.js" <<'EOF'
/*! SplitText 3.15.0 @license test-only fixture */
EOF
python3 "$ROOT_DIR/tools/gsap_check.py" "$TMP_DIR/gsap"
mkdir -p "$TMP_DIR/gsap-mixed/minified"
cp "$TMP_DIR/gsap/minified/gsap.min.js" "$TMP_DIR/gsap-mixed/minified/gsap.min.js"
cp "$TMP_DIR/gsap/minified/SplitText.min.js" "$TMP_DIR/gsap-mixed/minified/SplitText.min.js"
cat > "$TMP_DIR/gsap-mixed/minified/Flip.min.js" <<'EOF'
/*! Flip 3.14.0 @license test-only fixture */
EOF
if python3 "$ROOT_DIR/tools/gsap_check.py" "$TMP_DIR/gsap-mixed"; then
  echo "Expected mixed GSAP version failure" >&2
  exit 1
fi

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

cat > "$TMP_DIR/valid-motion-plan.json" <<'EOF'
{
  "schema_version": "1.0",
  "timeline_duration": 15,
  "motion_density": "energetic",
  "protected_regions": ["face", "captions", "screenshots", "product-ui"],
  "nodes": [
    {"node_id":"m1","recipe_id":"focus-frame","start":0.2,"end":0.9,"semantic_tag":"question","semantic_evidence":{"start":0.0,"end":1.0,"text":"为什么会这样？","intent":"question"},"target":"question","region":"top-safe","visual_role":"focus-frame","covers_protected_regions":false,"plugin":null,"fallback":"core DOM corners"},
    {"node_id":"m2","recipe_id":"counter-roll","start":2.0,"end":3.0,"semantic_tag":"number","semantic_evidence":{"start":1.9,"end":3.1,"text":"总共 12 个步骤","intent":"number"},"target":"12","region":"left-safe","visual_role":"metric-counter","covers_protected_regions":false,"plugin":null,"fallback":"numeric object tween"},
    {"node_id":"m3","recipe_id":"split-reveal","start":4.0,"end":5.5,"semantic_tag":"list","semantic_evidence":{"start":3.9,"end":5.6,"text":"第一步检查，第二步确认","intent":"list"},"target":"steps","region":"right-safe","visual_role":"split-steps","covers_protected_regions":false,"plugin":"SplitText","fallback":"word spans with core stagger"},
    {"node_id":"m4","recipe_id":"compare-split","start":6.5,"end":8.0,"semantic_tag":"compare","semantic_evidence":{"start":6.4,"end":8.1,"text":"之前很慢，之后更快","intent":"compare"},"target":"comparison","region":"center-safe","visual_role":"split-comparison","covers_protected_regions":false,"plugin":null,"fallback":"overflow wrappers"},
    {"node_id":"m5","recipe_id":"glass-notification","start":9.5,"end":10.2,"semantic_tag":"warning","semantic_evidence":{"start":9.4,"end":10.3,"text":"注意这个风险","intent":"warning"},"target":"risk","region":"top-safe","visual_role":"glass-warning","covers_protected_regions":false,"plugin":null,"fallback":"translucent DOM surface"},
    {"node_id":"m6","recipe_id":"approval-stamp","start":12.2,"end":13.2,"semantic_tag":"confirmation","semantic_evidence":{"start":12.1,"end":13.3,"text":"人工确认通过","intent":"confirmation"},"target":"approval","region":"right-safe","visual_role":"approval-mark","covers_protected_regions":false,"plugin":null,"fallback":"core scale and rotation"}
  ]
}
EOF
python3 "$ROOT_DIR/tools/motion_plan_check.py" "$TMP_DIR/valid-motion-plan.json"

python3 - "$TMP_DIR/valid-motion-plan.json" "$TMP_DIR/invalid-motion-plan.json" <<'PY'
import json
import sys

source, target = sys.argv[1:]
plan = json.load(open(source, encoding="utf-8"))
plan["nodes"] = plan["nodes"][:2]
for node in plan["nodes"]:
    node["visual_role"] = "corner-card"
json.dump(plan, open(target, "w", encoding="utf-8"))
PY
if python3 "$ROOT_DIR/tools/motion_plan_check.py" "$TMP_DIR/invalid-motion-plan.json"; then
  echo "Expected energetic coverage failure" >&2
  exit 1
fi

python3 - "$TMP_DIR/valid-motion-plan.json" "$TMP_DIR/unsafe-motion-plan.json" <<'PY'
import json
import sys

source, target = sys.argv[1:]
plan = json.load(open(source, encoding="utf-8"))
plan["nodes"][0]["region"] = "face"
plan["nodes"][0]["covers_protected_regions"] = True
json.dump(plan, open(target, "w", encoding="utf-8"))
PY
if python3 "$ROOT_DIR/tools/motion_plan_check.py" "$TMP_DIR/unsafe-motion-plan.json"; then
  echo "Expected protected-region failure" >&2
  exit 1
fi

HOME="$TMP_DIR/home" bash "$ROOT_DIR/install.sh" --codex --copy --force
test -f "$TMP_DIR/home/.codex/skills/talking-head-video-pipeline/SKILL.md"
test "$(find "$TMP_DIR/home/.codex/skills/talking-head-video-pipeline" -name SKILL.md | wc -l | tr -d ' ')" = "1"

printf 'preserve me\n' > "$TMP_DIR/home/.codex/skills/talking-head-video-pipeline/LOCAL_NOTE.txt"
printf 'n\n' | HOME="$TMP_DIR/home" bash "$ROOT_DIR/install.sh" --codex --copy
grep -q 'preserve me' "$TMP_DIR/home/.codex/skills/talking-head-video-pipeline/LOCAL_NOTE.txt"
mkdir -p "$TMP_DIR/home/.codex/skills/naive-video-init"
printf 'legacy entry\n' > "$TMP_DIR/home/.codex/skills/naive-video-init/SKILL.md"
HOME="$TMP_DIR/home" bash "$ROOT_DIR/install.sh" --codex --copy --force
find "$TMP_DIR/home/.naive-video-skill/backups" \
  -name LOCAL_NOTE.txt -type f | grep -q .
find "$TMP_DIR/home/.naive-video-skill/backups" \
  -path '*/legacy/naive-video-init/SKILL.md' -type f | grep -q .
test -f "$TMP_DIR/home/.codex/skills/talking-head-video-pipeline/SKILL.md"
test ! -e "$TMP_DIR/home/.codex/skills/naive-video-init"
test "$(find "$TMP_DIR/home/.codex/skills" -name SKILL.md | wc -l | tr -d ' ')" = "1"

HOME="$TMP_DIR/home" bash "$ROOT_DIR/uninstall.sh" --codex
test ! -e "$TMP_DIR/home/.codex/skills/talking-head-video-pipeline"
find "$TMP_DIR/home/.naive-video-skill/uninstalled" \
  -path '*/talking-head-video-pipeline/SKILL.md' -type f | grep -q .
test -f "$TMP_DIR/project/.naive-video-state.json"

echo "Smoke test passed."
echo "Test artifacts retained for inspection: $TMP_DIR"
