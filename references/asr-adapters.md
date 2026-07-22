# Transcription Adapters

The skill does not require one proprietary transcription service. Reuse existing timing first and discuss provider choices only when transcription is actually needed.

## Priority

1. Existing SRT and CSV supplied by the user.
2. Existing word-level transcript JSON.
3. A transcription capability already installed in the user's environment.
4. For precision rough cutting, installed `video-use` with its hosted word-level adapter when the user accepts possible service cost.
5. A compatible local word-level ASR chosen by the user.
6. Another user-configured cloud API.
7. User-provided text as a correction guide while timing still comes from audio.

For raw takes, hosted word-level transcription is the recommended best-fit route because retakes, filler words, and cut boundaries need fine timestamps. Say clearly that it may cost money and requires the user's own credentials. A local route remains optional and may be slower or less consistent depending on hardware and model. Never force either route.

## Detection

Check without installing anything silently. Treat these as examples, not mandatory dependencies:

```bash
command -v whisper
command -v faster-whisper
python3 -c "import whisper" 2>/dev/null
python3 -c "import faster_whisper" 2>/dev/null
```

Do not print or read API key values. Check only whether required environment variable names are present.

If `video-use` is installed and the task is rough cutting, follow [video-use-integration.md](video-use-integration.md) instead of recreating its editing pipeline.

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
