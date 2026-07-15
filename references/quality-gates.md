# Quality Gates

Use these gates as stage boundaries. A stage is complete only when its gate passes.

## G0 Source Gate

Record with `ffprobe`:

- source path
- duration
- width and height
- frame rate
- video codec and pixel format
- audio codec and sample rate

Pass when the source exists, has a video stream, and the intended master audio stream is known.

## G1 Caption Gate

Pass when:

- SRT parses successfully.
- Every cue has positive duration.
- Cues are ordered and do not overlap unexpectedly.
- Requested text-only replacements appear in SRT and CSV.
- Source media was not modified.

Run:

```bash
python3 tools/caption_check.py <srt> [<csv>]
```

## G2 Design Gate

Pass when `DESIGN.md` states:

- aspect ratio and resolution
- accent color and contrast intent
- caption and card style
- motion density
- face, screenshot, UI, and subtitle safe zones
- whether preview approval is required

Every requested insert must also exist in `EDIT_PLAN.md` with start, end or duration, layout, audio behavior, and exit behavior.

## G3 Preview Gate

Pass when:

- the official preview service is reachable
- main video and audio stay synchronized
- GSAP is present and the timeline is seekable
- evidence text remains readable
- no card, caption, or PiP covers a protected region
- requested demos actually play rather than freeze on one frame
- preview uses a proxy only as a preview asset

When the renderer supports lint or inspect commands, run them at all insert boundaries and transitions.

## G4 Approval Gate

Pass when the user explicitly approves the preview, or explicitly says to skip preview and export directly. Record the decision and timestamp in `.naive-video-state.json`.

Revisions invalidate previous approval when they change visible motion, layout, captions, or inserted media.

## G5 Final Gate

Pass when:

- final file exists and is non-empty
- duration matches the master timeline within normal container tolerance
- resolution matches the requested target
- frame rate is expected
- audio stream exists and comes from the intended master source
- the final was composed from original-quality source media, not a low-resolution preview proxy

If the user declines visual frame checks, perform only parameter checks and say so.

## G6 Learning Gate (Optional After Delivery)

Pass when:

- `VIDEO_RETRO.md` separates facts from guesses.
- each failure names the smallest responsible layer and a preventive check.
- project and profile lessons are based on explicit user confirmation.
- profile rules contain no paths, media names, customer data, transcript text, or secrets.
- public product candidates meet the promotion rules in `references/self-iteration.md`.

G6 does not change `final_ready`; it improves the next project without rewriting delivery history.

## Failure Policy

- Do not advance the state stage after a failed gate.
- Save the exact failing command and concise cause in `qa/QA_REPORT.md`.
- Fix the smallest failing layer.
- Do not rebuild approved layers without a reason.
