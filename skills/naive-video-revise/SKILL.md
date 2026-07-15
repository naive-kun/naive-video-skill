---
name: naive-video-revise
description: Apply scoped revisions to an existing Naive Video Skill project. Use when the user reports a visual problem, asks to restore an earlier version, changes a caption or insert, wants a different color or card style, or asks to preserve liked parts while fixing only the named issue.
---

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
7. Visible revisions invalidate preview approval. Return state to `preview_ready` or the last passed stage.
8. Re-run only affected quality gates plus downstream gates.

## Feedback Handling

Do not write a permanent lesson automatically. If the user explicitly says the rule should apply in future, route to `naive-video-learn` after the revision is confirmed.

## Completion

Report what changed, what was intentionally preserved, and the new preview or final path.
