# Transcription Adapters

The skill does not require one proprietary transcription service. Select the first available input.

## Priority

1. Existing SRT and CSV supplied by the user.
2. Existing word-level transcript JSON.
3. A transcription capability already installed in the user's environment.
4. A local Whisper-compatible CLI or Python package.
5. A user-configured cloud API.
6. User-provided text as a correction guide while timing still comes from audio.

## Detection

Check without installing anything silently:

```bash
command -v whisper
command -v faster-whisper
python3 -c "import whisper" 2>/dev/null
python3 -c "import faster_whisper" 2>/dev/null
```

Do not print or read API key values. Check only whether required environment variable names are present.

## Output Contract

Any adapter must produce word-level timing or enough timing detail to create:

```text
edit/script-aligned.srt
edit/caption-table.csv
edit/transcripts/<video_name>.json
```

Keep the raw adapter output cached so later text corrections do not require retranscription.

## Missing Adapter

If no adapter exists:

1. Say exactly what is missing.
2. Offer the shortest compatible installation path for the current OS.
3. Offer to continue immediately from an existing SRT, CSV, JSON, or transcript.
4. Do not claim caption files were generated.
