---
name: naive-video-init
description: Initialize or adopt a talking-head video project for Naive Video Skill. Use on first use, when the user says initialize/start a video project, when a source video has no project state, or when an older project must be adopted without moving media. Creates safe project memory, inspects source media, chooses quick or guided style onboarding, and points to the next action.
---

# Naive Video Init

Create a resumable project without modifying source media.

Resolve `<skill_root>` by locating the installed `talking-head-video-pipeline/SKILL.md`; do not assume the user's current directory is the skill directory.

## Workflow

1. Resolve `project_dir` and `main_video` from the user's message and attachments.
2. If `.naive-video-state.json` exists, do not reinitialize. Run project doctor and route to status or the requested stage.
3. Run environment checks:

   ```bash
   bash <skill_root>/scripts/doctor.sh
   ```

4. Inspect the source with `ffprobe`. Record duration, resolution, frame rate, codecs, pixel format, and audio stream.
5. Ask whether the user wants `quick` or `guided` setup only when they did not already request speed or provide a style reference.
6. Run:

   ```bash
   python3 <skill_root>/tools/bootstrap.py \
     --project <project_dir> \
     --video <main_video> \
     --mode <quick-or-guided>
   ```

7. If a private default profile exists, tell the user it was loaded. Use `--profile none` when the user wants a clean project without prior preferences.
8. In guided mode, ask one question at a time using `references/style-onboarding.md`, then update `DESIGN.md` and the state style profile.
9. Add all user-specified assets and time ranges to `EDIT_PLAN.md`. Do not load the media into the public skill.
10. Run:

   ```bash
   python3 <skill_root>/tools/video_doctor.py --project <project_dir>
   ```

## Adoption

For an older project with existing files, use `--adopt-existing`. Detect files but do not move or rename them. Set the stage only to the last quality gate that passes.

## Completion

Report:

- project directory
- source duration and resolution
- files created
- missing optional tools
- next phrase: `抽字幕轴` or `用现有字幕做预览`
