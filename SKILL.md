---
name: talking-head-video-pipeline
description: End-to-end, stateful talking-head video production for complete beginners and experienced editors. Use when a user wants optional rough-cut guidance, transcription or caption revision, screenshot and demo placement, visual design, a HyperFrames/GSAP preview, a synchronized final export, interrupted-work recovery, diagnosis, or reusable style learning from explicit feedback. Routes through internal workflow modules, optionally integrates video-use for raw footage, and preserves originals, evidence readability, privacy, and preview approval.
---

# Talking Head Video Pipeline

Turn raw or rough-cut talking-head footage into an approved working cut, editable captions, a motion-packaged preview, and a verified final export. Treat this file as the router and shared contract. Read only the routed internal workflow and references needed for the current stage.

## Beginner Promise

Assume the user has never edited with Codex.

- Ask one short question at a time only when an answer cannot be inferred safely.
- Prefer a working default over presenting many technical choices.
- Explain the next visible result, not the renderer internals.
- Introduce rough cutting, transcription providers, or API setup only when raw footage actually needs that branch.
- Explain paid and local choices plainly, recommend one when useful, and never force it.
- End every stage with exact output paths and the next phrase the user can say.
- Resume existing work instead of restarting it.

## Non-Negotiable Rules

1. **Source is immutable.** Never overwrite or destructively edit the supplied source media.
2. **Main audio is the clock.** Do not retime, reorder, resample, or replace it unless the user explicitly approves a rough-cut strategy. After approval, the derived `working_video` becomes the downstream clock while the original remains immutable.
3. **Evidence stays readable.** Never cover screenshot body text, product UI, faces, or user-marked safe zones. Do not blur evidence assets.
4. **Preview before final.** Build an official preview and wait for approval unless the user explicitly requests direct export.
5. **Original-quality final.** Do not present an upscaled low-resolution preview as a true high-resolution final. Use the original source as the final base whenever possible.
6. **Do not interrupt progress.** If a render is advancing, wait and report progress. Change pipelines only after a real error or explicit approval.
7. **No private data in the skill.** Project-local paths, media names, brand rules, screenshots, customer details, and API keys stay in the user's project.
8. **Learn only from explicit feedback.** Do not infer permanent style rules from silence or one unconfirmed draft.
9. **Typography is part of correctness.** Declare and verify font family, real weight, caption line policy, baseline alignment, and longest-label fit before approval.
10. **Public defaults stay brand-neutral.** Store creator palettes, recurring card systems, and private visual rules only in the local profile.
11. **Public install exposes one Skill.** Keep stage modules under `references/workflows/`; do not add nested `SKILL.md` files that package managers may register separately.
12. **Install operations are recoverable.** Back up an existing installation before replacement and archive uninstall targets instead of performing recursive force deletion.

Read [references/quality-gates.md](references/quality-gates.md) before preview or export work.

## Route Table

| User intent or phrase | Route | Typical output |
|---|---|---|
| `初始化视频项目`, `第一次用`, `start a video project` | `references/workflows/init.md` | State, edit plan, design profile |
| `原片还没剪`, `删口误和停顿`, `帮我粗剪`, `raw takes`, `rough cut` | `references/workflows/rough-cut.md` | Approved non-destructive rough cut and timing handoff |
| `抽字幕轴`, `只做字幕`, `transcribe`, `改字幕` | `references/workflows/captions.md` | SRT, CSV, transcript JSON |
| `帮我设计`, `换颜色风格`, `规划弹窗`, `design` | `references/workflows/design.md` | DESIGN and complete edit plan |
| `参考这张截图设计`, `按这张图的视觉语言`, `style reference` | `references/workflows/design.md` reference branch | Project-local STYLE_REFERENCE |
| `按语义匹配动效`, `GSAP 动效丰富一点`, `semantic motion` | `references/workflows/design.md`, then preview | Validated MOTION_PLAN and preview |
| `做预览`, `加动效`, `build preview` | `references/workflows/preview.md` | Official preview URL |
| `出成片`, `导出 4K`, `export final` | `references/workflows/export.md` | Verified final video |
| `改这个`, `恢复上一版`, `revise` | `references/workflows/revise.md` | Scoped revision and new preview/final |
| `进度`, `到哪了`, `status` | `references/workflows/status.md` | Current stage and next action |
| `体检`, `为什么失败`, `doctor` | `references/workflows/doctor.md` | Read-only diagnosis |
| `以后都这样`, `记住这个风格`, `learn this` | `references/workflows/learn.md` | Confirmed project-local lessons |
| `复盘成片`, `下次怎么改进`, `retro` | `references/workflows/retro.md` | Structured delivery retrospective |
| `升级状态`, `迁移`, `migrate` | `references/workflows/migrate.md` | State schema upgrade |

## Mode Detection

Before routing:

1. Identify the user's video project directory, not this skill repository.
2. Look for `.naive-video-state.json`.
3. If absent and the task is more than a one-off caption text edit, load the init workflow.
4. If present, read it plus `EDIT_PLAN.md`, `DESIGN.md`, and `VIDEO_LESSONS.md` only when relevant. Use `working_video` when present; otherwise use `main_video`.
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
3. Ask whether the footage is already rough-cut only when that status is unclear. If it is raw, load the optional rough-cut workflow and require strategy approval.
4. Produce or validate caption files from `working_video` when present, otherwise `main_video`.
5. Ask whether screenshots, recordings, product images, charts, or demos must appear. Let the user choose semantic placement, exact seconds/spoken-sentence anchors, or a hybrid; explain that exact anchors are more precise.
6. Collect or infer a style profile and safe zones. Offer optional screenshot-reference matching to beginners.
7. Write an edit plan and semantic motion plan with every requested insert and time range.
8. Build a HyperFrames + GSAP preview using a browser-friendly proxy if needed.
9. Run preview quality gates and provide the official preview URL.
10. Wait for approval unless explicitly told to skip.
11. Render overlays or final composition using the approved working video and its audio clock.
12. Verify file existence, duration, resolution, frame rate, and audio.
13. Record only confirmed feedback as project-local lessons.
14. After delivery, run a factual retrospective and promote only explicit, privacy-safe rules.

## Project Files

The init workflow creates this minimal project memory without touching source media:

```text
<project_dir>/
├── .naive-video-state.json
├── EDIT_PLAN.md
├── DESIGN.md
├── STYLE_REFERENCE.md       # created only when a reference image is used
├── MOTION_PLAN.json         # created when semantic motion is planned
├── VIDEO_LESSONS.md
├── VIDEO_RETRO.md
├── edit/
│   ├── rough-cut.mp4            # optional; original media is never overwritten
│   ├── rough-cut-edl.json       # optional decision record
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
- Keep readable text level and baseline-aligned; animate the containing component instead of skewing labels.
- Choose an explicit caption maximum line count and wrap policy.

Ask for an accent color only if brand consistency matters. Otherwise use the neutral preset and make it easy to change later. Beginners may optionally provide a screenshot and choose `low`, `medium`, or `high` reference strength; explain that the skill copies visual language, never the source brand or content. Motion density is `restrained`, `balanced`, or `energetic`. See [references/style-onboarding.md](references/style-onboarding.md).

Detailed GSAP recipes and semantic mappings live in [references/motion-recipes.md](references/motion-recipes.md). Runtime and plugin selection live in [references/gsap-runtime.md](references/gsap-runtime.md). Screenshot extraction and anti-copy rules live in [references/style-reference-workflow.md](references/style-reference-workflow.md). Asset timing choices live in [references/asset-onboarding.md](references/asset-onboarding.md). Load them only for the matching design branch.

Typography, component geometry, glass notifications, and seek-safe focus/type/split adaptation live in [references/visual-quality-rules.md](references/visual-quality-rules.md). Load it for every design or preview task.

## Self-Iteration Contract

Self-iteration means improving the current user's workflow without leaking it into public defaults.

Classify feedback into one scope:

- `project`: applies only to this video.
- `profile`: applies to this user's future videos; write it only after explicit confirmation.
- `product`: a privacy-safe, general reliability improvement; propose it to the skill maintainer separately.

Record profile feedback in `VIDEO_LESSONS.md` with the user's words, the confirmed rule, and the affected stage. Never copy media paths or private evidence into this repository. See [references/self-iteration.md](references/self-iteration.md).

Use the retro workflow after delivery to separate failures, environment issues, and taste feedback before promoting any rule. New projects import active private-profile rules into `VIDEO_LESSONS.md` so the editor can actually apply them.

## Recovery Rules

- If preview stops responding, check the process and port before rebuilding.
- If a browser cannot decode HEVC/Main10 smoothly, make an H.264 proxy for preview only.
- If a render session is running, poll it; do not terminate it merely because it is slow.
- If partial frames exist, compare expected and actual frame counts before resuming or restarting.
- Move damaged partial outputs to a project-local quarantine only after confirming they are not the sole valid result.
- Keep logs outside command pipes that can terminate long jobs.

## Privacy Before Publishing

Run:

```bash
bash scripts/doctor.sh --privacy-scan .
python3 tools/validate_skill.py .
```

Block publication if either command reports personal absolute paths, secrets, private media names, invalid frontmatter, multiple skill manifests, missing internal workflows, unsafe install commands, or broken templates.
