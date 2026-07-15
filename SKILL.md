---
name: talking-head-video-pipeline
description: End-to-end, stateful talking-head video production for beginners and experienced editors. Use when a user wants to initialize a video project, transcribe or revise captions, choose a visual style, add screenshots or demo videos, build a HyperFrames/GSAP preview, export a synchronized final video, resume interrupted work, diagnose a project, or learn reusable style rules from explicit feedback. Routes to focused sub-skills and preserves source timing, audio, evidence readability, privacy, and preview approval.
---

# Talking Head Video Pipeline

Turn a raw or rough-cut talking-head video into editable captions, a motion-packaged preview, and a verified final export. Treat this file as the router and shared contract. Read only the routed sub-skill and references needed for the current stage.

## Beginner Promise

Assume the user has never edited with Codex.

- Ask one short question at a time only when an answer cannot be inferred safely.
- Prefer a working default over presenting many technical choices.
- Explain the next visible result, not the renderer internals.
- End every stage with exact output paths and the next phrase the user can say.
- Resume existing work instead of restarting it.

## Non-Negotiable Rules

1. **Source is immutable.** Never overwrite or destructively edit the supplied source media.
2. **Main audio is the clock.** Do not retime, reorder, resample, or replace it unless explicitly requested.
3. **Evidence stays readable.** Never cover screenshot body text, product UI, faces, or user-marked safe zones. Do not blur evidence assets.
4. **Preview before final.** Build an official preview and wait for approval unless the user explicitly requests direct export.
5. **Original-quality final.** Do not present an upscaled low-resolution preview as a true high-resolution final. Use the original source as the final base whenever possible.
6. **Do not interrupt progress.** If a render is advancing, wait and report progress. Change pipelines only after a real error or explicit approval.
7. **No private data in the skill.** Project-local paths, media names, brand rules, screenshots, customer details, and API keys stay in the user's project.
8. **Learn only from explicit feedback.** Do not infer permanent style rules from silence or one unconfirmed draft.

Read [references/quality-gates.md](references/quality-gates.md) before preview or export work.

## Route Table

| User intent or phrase | Route | Typical output |
|---|---|---|
| `初始化视频项目`, `第一次用`, `start a video project` | `skills/naive-video-init/SKILL.md` | State, edit plan, design profile |
| `抽字幕轴`, `只做字幕`, `transcribe`, `改字幕` | `skills/naive-video-captions/SKILL.md` | SRT, CSV, transcript JSON |
| `帮我设计`, `换颜色风格`, `规划弹窗`, `design` | `skills/naive-video-design/SKILL.md` | DESIGN and complete edit plan |
| `做预览`, `加动效`, `build preview` | `skills/naive-video-preview/SKILL.md` | Official preview URL |
| `出成片`, `导出 4K`, `export final` | `skills/naive-video-export/SKILL.md` | Verified final video |
| `改这个`, `恢复上一版`, `revise` | `skills/naive-video-revise/SKILL.md` | Scoped revision and new preview/final |
| `进度`, `到哪了`, `status` | `skills/naive-video-status/SKILL.md` | Current stage and next action |
| `体检`, `为什么失败`, `doctor` | `skills/naive-video-doctor/SKILL.md` | Read-only diagnosis |
| `以后都这样`, `记住这个风格`, `learn this` | `skills/naive-video-learn/SKILL.md` | Confirmed project-local lessons |
| `复盘成片`, `下次怎么改进`, `retro` | `skills/naive-video-retro/SKILL.md` | Structured delivery retrospective |
| `升级状态`, `迁移`, `migrate` | `skills/naive-video-migrate/SKILL.md` | State schema upgrade |

## Mode Detection

Before routing:

1. Identify the user's video project directory, not this skill repository.
2. Look for `.naive-video-state.json`.
3. If absent and the task is more than a one-off caption text edit, route to `naive-video-init`.
4. If present, read it plus `EDIT_PLAN.md`, `DESIGN.md`, and `VIDEO_LESSONS.md` only when relevant.
5. Run `python3 tools/video_doctor.py --project <project_dir>` when state and files disagree.

Use these stages:

```text
initialized -> captions_ready -> design_ready -> preview_ready
-> approved -> rendering -> final_ready
```

Never mark a later stage until its quality gate passes.

## Default Pipeline

When the user asks for the complete workflow:

1. Inspect source media with `ffprobe`.
2. Initialize project state and safe output directories.
3. Produce or validate caption files.
4. Collect or infer a style profile and safe zones.
5. Write an edit plan with every requested insert and time range.
6. Build a HyperFrames + GSAP preview using a browser-friendly proxy if needed.
7. Run preview quality gates and provide the official preview URL.
8. Wait for approval unless explicitly told to skip.
9. Render overlays or final composition using the original source and original audio.
10. Verify file existence, duration, resolution, frame rate, and audio.
11. Record only confirmed feedback as project-local lessons.
12. After delivery, run a factual retrospective and promote only explicit, privacy-safe rules.

## Project Files

`naive-video-init` creates this minimal project memory without touching source media:

```text
<project_dir>/
├── .naive-video-state.json
├── EDIT_PLAN.md
├── DESIGN.md
├── VIDEO_LESSONS.md
├── VIDEO_RETRO.md
├── edit/
│   ├── script-aligned.srt
│   ├── caption-table.csv
│   └── transcripts/
├── preview/
├── final/
└── qa/
```

State is operational metadata, not a media database. Keep it small and never store transcript bodies, private screenshots, or secrets in it. See [references/state-management.md](references/state-management.md).

## Style Defaults

If the user wants speed and gives no reference:

- Preserve the source aspect ratio.
- Use a clean, readable card system with one configurable accent color.
- Use bold captions with restrained keyword emphasis.
- Use GSAP transforms and opacity for motion.
- Place cards in verified empty space.
- Reduce motion density while screenshots or demos are visible.

Ask for an accent color only if brand consistency matters. Otherwise use the neutral preset and make it easy to change later. See [references/style-onboarding.md](references/style-onboarding.md).

## Self-Iteration Contract

Self-iteration means improving the current user's workflow without leaking it into public defaults.

Classify feedback into one scope:

- `project`: applies only to this video.
- `profile`: applies to this user's future videos; write it only after explicit confirmation.
- `product`: a privacy-safe, general reliability improvement; propose it to the skill maintainer separately.

Record profile feedback in `VIDEO_LESSONS.md` with the user's words, the confirmed rule, and the affected stage. Never copy media paths or private evidence into this repository. See [references/self-iteration.md](references/self-iteration.md).

Use `naive-video-retro` after delivery to separate failures, environment issues, and taste feedback before promoting any rule. New projects import active private-profile rules into `VIDEO_LESSONS.md` so the editor can actually apply them.

## Recovery Rules

- If preview stops responding, check the process and port before rebuilding.
- If a browser cannot decode HEVC/Main10 smoothly, make an H.264 proxy for preview only.
- If a render session is running, poll it; do not terminate it merely because it is slow.
- If partial frames exist, compare expected and actual frame counts before resuming or restarting.
- Delete damaged partial outputs only after confirming they are not the sole valid result.
- Keep logs outside command pipes that can terminate long jobs.

## Privacy Before Publishing

Run:

```bash
bash scripts/doctor.sh --privacy-scan .
python3 tools/validate_skill.py .
```

Block publication if either command reports personal absolute paths, secrets, private media names, invalid frontmatter, missing routed sub-skills, or broken templates.
