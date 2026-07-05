# Caption Workflow Reference

## Output Files

Create:

```text
edit/script-aligned.srt
edit/caption-table.csv
edit/transcripts/<video_name>.json
```

## Caption Grouping Rules

- Prefer semantic sentence groups over mechanical line breaks.
- Keep each caption readable at normal playback speed.
- Avoid one very long line plus one tiny line.
- Avoid captions shorter than roughly 0.5s unless the speech is genuinely short.
- Avoid zero-duration or near-zero-duration captions.
- Keep timestamps on the output timeline when cutting is involved.

## Text Correction Rules

- Use a user script as a correction guide, not as absolute truth.
- Prefer the spoken words when the script and video differ.
- Preserve tool names and brand names exactly.
- When replacing a word globally, update SRT and CSV together.
- Do not change timings during text-only revisions.

## Suggested CSV Fields

```csv
index,start,end,duration,text
```

## Common Self Checks

- Count captions.
- Report shortest and longest duration.
- Search for requested replaced words.
- Search for known ASR mistakes in proper nouns and tool names.
