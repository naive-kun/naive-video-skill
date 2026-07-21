# Changelog

## 2.0.1

- Added HyperFrames CLI transcription as a first-class ASR adapter.
- Clarified that a missing standalone Whisper package is not an ASR blocker when an explicitly supplied HyperFrames CLI is available.
- Added a no-speech gate so synthetic tones and silent media still stop honestly instead of producing invented captions.

## 2.0.0

- Added a root router and eleven focused child skills.
- Added beginner project initialization and resumable project state.
- Added explicit quality gates for source, captions, design, preview, approval, and final export.
- Added project doctor, caption consistency check, privacy scan, and no-dependency skill validation.
- Added Codex and Claude Code installers plus uninstall support.
- Added explicit-feedback learning and privacy-safe self-iteration rules.
- Added post-delivery retrospectives and deterministic private-profile rule inheritance.
- Added schema migration registry and adoption path for older projects.
- Added smoke tests and GitHub Actions validation.
- Corrected export guidance so a low-resolution proxy is never presented as a true high-resolution final.
