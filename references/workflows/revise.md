# Naive Video Revise

Change the smallest responsible layer and preserve approved work.

Resolve `<skill_root>` by locating the installed `talking-head-video-pipeline/SKILL.md`; do not assume the user's current directory is the skill directory.

## Workflow

1. Restate the visible problem in one sentence.
2. Identify the responsible layer: caption, style, motion, asset timing, PiP/mask, preview playback, render, or final composition.
3. Read active `VIDEO_LESSONS.md` rules relevant to that layer.
4. Preserve every element the user liked or did not ask to change.
5. If the user says "return to the original", recover the original project source or committed baseline instead of approximating it from a later broken version.
6. Apply the minimum edit.
7. If motion intent, timing, region, or density changes, update `MOTION_PLAN.json` and rerun `motion_plan_check.py` before rebuilding preview.
8. If the reference image or reference strength changes, regenerate `STYLE_REFERENCE.md` and only the derived style fields; preserve unrelated timing and media placement.
9. Visible revisions invalidate preview approval. Return state to `preview_ready` or the last passed stage.
10. Re-run only affected quality gates plus downstream gates.

## Feedback Handling

Do not write a permanent lesson automatically. If the user explicitly says the rule should apply in future, load the internal learn workflow after the revision is confirmed.

## Completion

Report what changed, what was intentionally preserved, and the new preview or final path.
