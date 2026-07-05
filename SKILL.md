---
name: talking-head-video-pipeline
description: End-to-end talking-head video production workflow. Use when the user wants to transcribe a raw or rough-cut talking-head video, generate editable SRT/CSV caption timing, optionally revise caption text, choose or customize a visual style, build a HyperFrames/GSAP preview, and export a final video while preserving the source audio/video timing.
---

# Talking Head Video Pipeline

This skill turns a raw or rough-cut talking-head video into a publishable video:

1. Transcribe the source video.
2. Generate editable caption timing files.
3. Ask for or infer the visual style.
4. Build an HTML/GSAP motion-graphics preview.
5. Export the final video without breaking audio sync.

Keep the user's original media untouched unless they explicitly ask for cuts.

## Operating Modes

Choose the narrowest mode that satisfies the user:

- `captions-only`: transcribe and create `script-aligned.srt`, `caption-table.csv`, and raw transcript JSON.
- `style-preview`: use existing caption files to build a motion-graphics preview.
- `full-pipeline`: captions, optional text revision, style onboarding, preview, and final export.
- `revise`: update caption text or motion style from user feedback without redoing unrelated work.

Default to `full-pipeline` only when the user asks for end-to-end production.

## Required First Step

Before editing, collect or infer:

- `main_video`: source talking-head video.
- `output_dir`: where generated files should go. Default to `<main_video_dir>/edit/` for captions and `<main_video_dir>/final/` for rendered videos.
- `transcript_or_script`: optional correction script supplied by the user.
- `style`: existing brand guide, reference screenshot, or user preferences.
- `extra_media`: optional screenshots, screen recordings, logos, or demo videos with timestamps.
- `preview_required`: default `true`; skip preview only when the user explicitly says to export directly.
- `transcription_method`: local ASR, cloud API, existing transcript JSON, or user-provided captions.

Use `ffprobe` to inspect source duration, size, frame rate, codec, pixel format, and audio stream.

If the environment is unknown, run `scripts/doctor.sh` from this skill folder or do equivalent checks manually.

## Caption Axis Workflow

Create these files under `<main_video_dir>/edit/`:

```text
script-aligned.srt
caption-table.csv
transcripts/<video_name>.json
```

Workflow:

1. Run word-level transcription and cache the raw JSON.
2. If the user supplies a script, use it as a correction guide, but prefer the spoken video when the script differs.
3. Group captions by semantic sentence, not by mechanical line length.
4. Write both SRT and CSV.
5. Lightly fix obvious terminology errors.

Caption rules:

- Do not modify the source video.
- Avoid zero-second captions.
- Avoid tiny flash captions below roughly 0.5s unless unavoidable.
- Avoid a long first line with a tiny second line.
- Keep terminology consistent: product names, tools, people, brands, project names.
- When the user asks for text replacement, update SRT and CSV together without changing timing.
- If no transcription tool/API is available, explain the missing dependency and offer to continue from a user-provided transcript, SRT, CSV, or JSON.

Default delivery message:

```text
Caption files are ready; source video was not modified.

- script-aligned.srt
- caption-table.csv
- transcript json

Checked: N captions, shortest Xs, longest Ys, obvious ASR terms fixed.
```

## Style Onboarding

If no style guide or reference screenshot is provided, ask concise questions before building the preview:

1. Brand/accent color?
2. Caption style: brush subtitle, clean lower-third, or platform-style subtitles?
3. Card style: frosted white tool cards, dark tech panels, sticker cards, or minimal captions only?
4. Mood: professional, energetic, tutorial, documentary, humorous, or cinematic?
5. Output format: 16:9, 9:16, 1:1, or preserve source aspect ratio?

If the user does not answer and wants speed, choose a conservative default:

- White frosted cards.
- One accent color.
- Bold readable captions.
- Minimal motion.
- Do not cover faces or evidence screenshots.

Store the chosen style in a project-local `DESIGN.md` so future turns can reuse it.

See `references/style-onboarding.md` for a reusable question set and style schema.
See `references/caption-workflow.md` for caption grouping rules.

## Motion Graphics Preview

Use HTML video composition with GSAP when available. HyperFrames is recommended but not mandatory if the user's environment has another renderer.

Preview project structure:

```text
<work_dir>/
  hyperframes-preview/
    index.html
    DESIGN.md
    hyperframes.json
    assets/
```

Preview rules:

- Main video/audio is the master clock.
- Do not retime or reorder the main video unless the user asks for an edit.
- If screenshots or demos are already in the main video, treat it as a locked base and only add captions/cards/transparent overlays.
- Use GSAP for motion: `scale`, `y`, `filter: blur(...)`, `autoAlpha`, `back.out`, `elastic.out`, `stagger`, subtle shake, pulse.
- Avoid static PPT-style slides.
- Evidence screenshots stay readable. Do not cover body text with big cards or captions.
- If using picture-in-picture, avoid faces, subtitles, and important UI.
- If the source codec stutters in browser preview, generate a temporary H.264 preview proxy and keep the original video for final export.

Default preview response:

```text
Preview is ready:
http://localhost:<port>/#project/<project-name>

Please confirm the motion/style before final export.
```

## Final Export

Export only after preview approval, unless the user explicitly says to skip preview.

Final rules:

- Preserve source audio as the master audio.
- Preserve source timing.
- Use the original source video as the base when possible.
- Do not use a low-resolution preview proxy as the final base.
- If the source is high-resolution HEVC/Main10 or otherwise fragile, render a transparent overlay and composite it over the original source with ffmpeg.

Minimum verification:

- Confirm file exists.
- Confirm duration.
- Confirm resolution.
- Confirm audio stream exists.

If the user says not to inspect frames, do not extract visual QA frames; only do file parameter checks.

See `references/export-recipes.md` for ffmpeg patterns and stable-overlay guidance.

## Privacy and Open Source Rules

Never bake personal paths, account names, private screenshots, API keys, or user-specific brand rules into this skill.

Use placeholders:

- `<main_video>`
- `<output_dir>`
- `<work_dir>`
- `<project_name>`
- `<accent_color>`

Do not mention a specific creator account, local username, private folder, or previous customer/video unless the user provides it in the current task.

## Troubleshooting

- If preview fails, check whether the server process is still listening on the port.
- If browser preview stutters on HEVC, create an H.264 preview proxy; keep the original for final export.
- Do not pipe long-running render commands into `head`; redirect logs to a file, then inspect the log separately.
- If rendering is slow but progressing, wait. Do not switch pipelines without a real error or user approval.
- Before publishing changes to the skill, run a privacy scan for local usernames, absolute personal paths, API keys, private project names, and real customer media names.
