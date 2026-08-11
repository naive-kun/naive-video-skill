# Naive Video Revise

Change the smallest responsible layer and preserve approved work.

Resolve `<skill_root>` by locating the installed `talking-head-video-pipeline/SKILL.md`; do not assume the user's current directory is the skill directory.

## Workflow

1. Normalize each requested change as `time or range + object + current problem + target state`. Ask only for fields that cannot be inferred safely.
2. Restate the visible problem in one sentence.
3. Identify the responsible layer: caption, content logic, style, motion, asset timing, PiP/mask, preview playback, render, or final composition.
4. Read active `VIDEO_LESSONS.md` rules relevant to that layer.
5. Preserve every element the user liked or did not ask to change.
6. If the user says "return to the original", recover the original project source or committed baseline instead of approximating it from a later broken version.
7. Apply the minimum edit.
8. If grouping, takeaway, or accumulation changes, update and validate `CONTENT_LOGIC.json` before changing downstream motion.
9. If motion intent, timing, region, or density changes, update `MOTION_PLAN.json` and rerun `motion_plan_check.py` before rebuilding preview.
10. If the reference image or reference strength changes, regenerate `STYLE_REFERENCE.md` and only the derived style fields; preserve unrelated timing and media placement.
11. First render affected keyframes or a short fragment spanning the change plus 2-3 seconds on each side. Do not rebuild the complete preview until the scoped change passes.
12. Visible revisions invalidate preview approval. Return state to `preview_ready` or the last passed stage.
13. Re-run only affected quality gates plus downstream gates.

## Feedback Handling

Do not write a permanent lesson automatically. If the user explicitly says the rule should apply in future, load the internal learn workflow after the revision is confirmed.

## Completion

Report what changed, what was intentionally preserved, and the new preview or final path.
