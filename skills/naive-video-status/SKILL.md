---
name: naive-video-status
description: Report the current stage, render progress, verified outputs, blockers, and exact next action for a Naive Video Skill project. Use when the user asks where the task is, how many frames are rendered, whether it is stuck, what remains, or how to continue after an interruption.
---

# Naive Video Status

Provide a factual, short status update without changing project files.

Resolve `<skill_root>` by locating the installed `talking-head-video-pipeline/SKILL.md`; do not assume the user's current directory is the skill directory.

## Workflow

1. Read `.naive-video-state.json`.
2. Check declared output and log paths.
3. If a process or render session exists, poll it without interrupting it.
4. If frame output is used, report actual frame count and expected count from duration times frame rate.
5. Run project doctor only when state and files disagree.
6. Report:
   - current stage
   - completed gates
   - active process and progress
   - last verified output
   - blocker, if any
   - exact next action

Do not call a progressing render "stuck" merely because it is slow.
