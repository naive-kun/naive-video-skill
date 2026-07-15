---
name: naive-video-retro
description: Run a structured post-delivery retrospective for a Naive Video Skill project. Use after a final export, after repeated revisions, when the user asks what should improve next time, or when confirmed feedback should become project or private-profile rules without leaking media, paths, brands, or customer information.
---

# Naive Video Retro

Close the production loop with facts, explicit feedback, and testable improvements.

Resolve `<skill_root>` by locating the installed `talking-head-video-pipeline/SKILL.md`; do not assume the user's current directory is the skill directory.

## Preconditions

- Prefer a project at `final_ready`; a revision-heavy preview may be reviewed early when the user asks.
- Read `.naive-video-state.json`, `EDIT_PLAN.md`, `DESIGN.md`, `VIDEO_LESSONS.md`, `VIDEO_RETRO.md`, and `qa/QA_REPORT.md`.
- Treat user feedback as the source of preference truth. Do not infer approval from silence.

## Workflow

1. Compare requested inserts, protected regions, approval state, and final QA facts.
2. Separate outcomes into:
   - confirmed wins
   - visible failures or revisions
   - environment or tooling failures
   - user taste preferences
3. For every failure, record the smallest responsible layer and one preventive check.
4. Write the factual result to `VIDEO_RETRO.md`; do not paste transcripts, screenshots, customer data, or long logs.
5. Present candidate lessons to the user before promoting them.
6. Route confirmed project rules to `naive-video-learn` with `project` scope.
7. Route explicitly cross-project rules to `naive-video-learn` with `profile` scope.
8. Keep general product candidates sanitized and local until a maintainer reviews them.
9. Record the retro path without changing the completed production stage:

   ```bash
   python3 <skill_root>/tools/state.py \
     --project <project_dir> output retro <project_dir>/VIDEO_RETRO.md
   ```

## Promotion Gate

A lesson becomes a private profile rule only when it is explicit, observable, testable, and free of private context. A public product rule additionally needs either two independent project observations or one hard correctness failure with a regression test.

## Completion

Return:

- confirmed wins
- root causes and preventive checks
- lessons promoted to project or profile
- product candidates that still require maintainer review
- the `VIDEO_RETRO.md` path
