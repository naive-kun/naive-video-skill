# Naive Video Captions

Produce editable caption files without changing the source video.

Resolve `<skill_root>` by locating the installed `talking-head-video-pipeline/SKILL.md`; do not assume the user's current directory is the skill directory.

## Inputs

- `working_video` from state when an approved rough cut exists, otherwise `main_video` or the video from the user message
- optional existing SRT, CSV, or transcript JSON
- optional correction script
- optional terminology list

## Workflow

1. Confirm the exact source and output directory.
2. Reuse existing word-level transcript data before retranscribing.
3. Select an adapter using `references/asr-adapters.md`.
4. Use spoken audio as timing truth. Use a supplied script only as a correction guide.
5. Group semantic sentences and create:

   ```text
   edit/script-aligned.srt
   edit/caption-table.csv
   edit/transcripts/<video_name>.json
   ```

6. For text-only corrections, update SRT and CSV together without changing timestamps.
7. Run:

   ```bash
   python3 <skill_root>/tools/caption_check.py \
     <project_dir>/edit/script-aligned.srt \
     <project_dir>/edit/caption-table.csv
   ```

8. Set state stage to `captions_ready` only after G1 passes.

## Rules

- Never modify source media.
- Avoid zero-duration or near-zero flash captions.
- Keep proper nouns consistent.
- Do not pretend transcription succeeded when no adapter or usable caption source exists.
- Do not ask users with valid existing captions to choose a cloud or local provider.

## Completion

Return paths first, then cue count, shortest duration, longest duration, and any unresolved terminology. End with: `字幕确认后，我可以继续做风格和官方预览。`
