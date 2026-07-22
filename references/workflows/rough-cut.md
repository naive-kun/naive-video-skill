# Naive Video Rough Cut

Create a reviewable rough cut without overwriting any original media.

Resolve `<skill_root>` by locating the installed `talking-head-video-pipeline/SKILL.md`; do not assume the user's current directory is the skill directory.

## Trigger Boundary

Use this skill only for raw footage or an explicit rough-cut request. If the user says the video is already rough-cut, return to captions or design without discussing ASR providers.

## Workflow

1. Read `references/video-use-integration.md`.
2. Inventory the supplied clips and inspect duration, codecs, frame rate, resolution, and audio. Do not modify them.
3. Ask what should be removed or preserved only when it cannot be inferred safely. Propose a concise keep/remove strategy and wait for approval.
4. Reuse existing timing files first. When transcription is needed, explain the hosted and local word-level choices in plain language and let the user choose without pressure.
5. If `video-use` is installed and the user approves, route the actual rough cut to `$video-use` and follow its current instructions. Do not duplicate or partially imitate its editing engine.
6. If `video-use` is absent, explain that it is optional and offer the public installation route. Never install it or request an API key silently.
7. Verify all cuts at word or silence boundaries. Add short audio fades at new segment boundaries and retain an edit decision record.
8. Present the rough cut for review. After approval, record it as the project `working_video` using `tools/state.py working-video`.
9. Return to the main pipeline for captions, asset placement, design, and preview.

## Hard Rules

- Originals are immutable.
- A paid cloud service is never mandatory.
- A local ASR is not described as equally accurate unless it is actually verified on the user's footage.
- Do not cut inside a word.
- Do not execute a destructive edit before strategy approval.
- Do not expose API keys in chat, logs, state, or project documentation.
- Keep transcription caches in the user's project, never in this public skill directory.

## Completion

Return the rough-cut path, strategy approval, timing source, ambiguous cuts, and next phrase: `粗剪确认，继续做字幕和画面设计。`
