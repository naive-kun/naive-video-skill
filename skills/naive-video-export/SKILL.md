---
name: naive-video-export
description: Export and verify the final video for a Naive Video Skill project. Use when the user approves a preview, explicitly asks to skip preview, requests a final or 4K deliverable, wants original audio preserved, or needs a stable original-source plus transparent-overlay composition for high-resolution HEVC or Main10 media.
---

# Naive Video Export

Render the approved composition with original-quality media and master audio.

Resolve `<skill_root>` by locating the installed `talking-head-video-pipeline/SKILL.md`; do not assume the user's current directory is the skill directory.

## Preconditions

1. Read state and G4 approval.
2. If approval is pending, stop and request preview confirmation unless state records `skipped_by_user`.
3. Re-run G0 and confirm the original source still exists.
4. Determine final target resolution from the request or source; do not infer true 4K from a 1080p proxy.

## Stable Strategy

Prefer:

1. Render transparent motion overlays at final resolution.
2. Use the original source as the ffmpeg base.
3. Composite inserted demos and overlays at their timeline positions.
4. Map the original main audio.

Use this strategy for 4K HEVC/Main10 or whenever preserving the locked base is important. Read `references/export-recipes.md`.

## Rendering

- Write long render output to a log file.
- Poll progress without killing the process.
- If frames advance, wait.
- Resume only when the renderer supports a safe resume contract.
- Replace damaged partial output only after the full rerender starts successfully.
- Set state to `rendering` with output path and log path.

## Final Gate

Verify with `ffprobe`:

- file exists and is non-empty
- duration
- resolution
- frame rate
- video codec
- audio codec and stream presence

Perform visual frame checks unless the user explicitly declines them. Set `final_ready` only after G5 passes.

## Completion

Return the final file path, containing folder path, duration, resolution, and audio confirmation. State clearly if visual QA was skipped at the user's request.
