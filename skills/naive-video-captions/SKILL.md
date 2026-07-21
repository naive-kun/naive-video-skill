---
name: naive-video-captions
description: Generate, validate, or text-revise caption timing for a Naive Video Skill project. Use when the user asks to transcribe, extract caption timing, create SRT/CSV/transcript JSON, use an existing script as a correction guide, replace caption text without changing timing, or diagnose caption-axis problems while leaving source video untouched.
---

# Naive Video Captions

Produce editable caption files without changing the source video.

Resolve `<skill_root>` by locating the installed `talking-head-video-pipeline/SKILL.md`; do not assume the user's current directory is the skill directory.

## Inputs

- main video from state or user message
- optional existing SRT, CSV, or transcript JSON
- optional correction script
- optional terminology list

## Workflow

1. Confirm the exact source and output directory.
2. Reuse existing word-level transcript data before retranscribing.
3. Select an adapter using `references/asr-adapters.md`.
4. When a HyperFrames CLI command or version was explicitly supplied and verifies successfully, treat `hyperframes transcribe` as the active adapter. A failed `import whisper` alone is not a blocker.
5. Confirm the media contains an audio stream and intelligible speech. Silence or a synthetic tone is a `no usable speech` input blocker, not an ASR installation blocker.
6. Use spoken audio as timing truth. Use a supplied script only as a correction guide.
7. Group semantic sentences and create:

   ```text
   edit/script-aligned.srt
   edit/caption-table.csv
   edit/transcripts/<video_name>.json
   ```

8. For text-only corrections, update SRT and CSV together without changing timestamps.
9. Run:

   ```bash
   python3 <skill_root>/tools/caption_check.py \
     <project_dir>/edit/script-aligned.srt \
     <project_dir>/edit/caption-table.csv
   ```

10. Set state stage to `captions_ready` only after G1 passes.

## Rules

- Never modify source media.
- Avoid zero-duration or near-zero flash captions.
- Keep proper nouns consistent.
- Do not pretend transcription succeeded when no adapter or usable caption source exists.

## Completion

Return paths first, then cue count, shortest duration, longest duration, and any unresolved terminology. End with: `字幕确认后，我可以继续做风格和官方预览。`
