---
name: naive-video-migrate
description: Safely migrate an older or partially initialized Naive Video Skill project to the current state schema. Use after updating the skill, when schema versions differ, when an old project has outputs but no state file, or when the user asks to upgrade project state without moving or overwriting media.
---

# Naive Video Migrate

Upgrade metadata, never media.

Resolve `<skill_root>` by locating the installed `talking-head-video-pipeline/SKILL.md`; do not assume the user's current directory is the skill directory.

## Workflow

1. Read `migrations/registry.md` and determine the ordered migration chain.
2. Run project doctor and capture current findings.
3. Back up only `.naive-video-state.json` when it exists.
4. Apply one migration step at a time.
5. Preserve unknown fields and all user-authored project files.
6. Validate JSON after each step.
7. Run project doctor again.
8. Set stage to the last quality gate that actually passes.

For projects with no state, follow `migrations/0-to-1.0.md` and use:

```bash
python3 <skill_root>/tools/bootstrap.py \
  --project <project_dir> \
  --video <main_video> \
  --adopt-existing
```

## Safety

- Do not move, rename, transcode, or delete media.
- Do not invent preview approval.
- Stop at the first failed migration and report the last successful schema.
