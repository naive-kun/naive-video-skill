# Transcription Adapters

The skill does not require one proprietary transcription service. Select the first available input.

## Priority

1. Existing SRT and CSV supplied by the user.
2. Existing word-level transcript JSON.
3. An explicitly supplied or already available HyperFrames CLI transcription command.
4. Another transcription capability already installed in the user's environment.
5. A local Whisper-compatible CLI or Python package.
6. A user-configured cloud API.
7. User-provided text as a correction guide while timing still comes from audio.

## Detection

Check without installing anything silently:

```bash
command -v npx
npx --no-install hyperframes --version 2>/dev/null
command -v whisper
command -v faster-whisper
python3 -c "import whisper" 2>/dev/null
python3 -c "import faster_whisper" 2>/dev/null
```

If the user explicitly supplied a HyperFrames version or command, verify that exact command. It is then a valid ASR adapter even when `import whisper` and the standalone `whisper` CLI are unavailable:

```bash
npx --yes hyperframes@<supplied-version> --version
npx --yes hyperframes@<supplied-version> transcribe <video-or-audio>
```

Do not silently download HyperFrames when the user has not supplied it or approved the download. Do not report "no ASR adapter" merely because standalone Whisper is missing when the verified HyperFrames command is available.

## HyperFrames Adapter

Run transcription against the real source media, then normalize its outputs into the project contract. Preserve the raw HyperFrames transcription output under `edit/transcripts/`.

Before transcription, confirm that the source has an audio stream. If the test asset is silence, a synthetic tone, or otherwise contains no intelligible speech, report `no usable speech` rather than treating it as an adapter failure or inventing captions.

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

If no adapter exists, or the source has no usable speech:

1. Distinguish `adapter missing` from `audio has no usable speech`.
2. Offer the shortest compatible installation path for the current OS.
3. Offer to continue immediately from an existing SRT, CSV, JSON, or transcript.
4. Do not claim caption files were generated.
