---
name: naive-video-doctor
description: Perform a read-only environment and project consistency diagnosis for Naive Video Skill. Use when setup fails, dependencies are missing, preview is blank or frozen, state is inconsistent, output paths are missing, captions fail validation, a render appears stuck, or the user asks for a health check before repair.
---

# Naive Video Doctor

Diagnose before changing anything.

Resolve `<skill_root>` by locating the installed `talking-head-video-pipeline/SKILL.md`; do not assume the user's current directory is the skill directory.

## Commands

Environment:

```bash
bash <skill_root>/scripts/doctor.sh
```

Project:

```bash
python3 <skill_root>/tools/video_doctor.py --project <project_dir>
```

Captions:

```bash
python3 <skill_root>/tools/caption_check.py <srt> [<csv>]
```

## Diagnosis Order

1. Missing required tools.
2. Missing or invalid state.
3. Missing source or outputs referenced by state.
4. Failed quality gate.
5. Renderer process or port state.
6. Codec/browser compatibility.
7. Timeline or asset-duration mismatch.

## Output

List findings by severity:

- `BLOCKER`: work cannot continue.
- `WARNING`: work can continue with risk.
- `INFO`: current verified state.

Give the smallest repair order. Do not edit files, kill processes, delete outputs, or migrate state in doctor mode.
