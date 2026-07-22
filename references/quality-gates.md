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

When rough cutting is requested, also pass the rough-cut handoff only when:

- the keep/remove strategy was explicitly approved;
- the original `main_video` still exists and was not overwritten;
- the derived rough cut exists and is recorded as `working_video`;
- `master_audio` points to `working_video`;
- ambiguous cuts are listed instead of silently guessed.

## G1 Caption Gate

Pass when:

- SRT parses successfully.
- Every cue has positive duration.
- Cues are ordered and do not overlap unexpectedly.
- Requested text-only replacements appear in SRT and CSV.
- Original source media was not modified. Captions use `working_video` when an approved rough cut exists.

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

The typography and component contract must also state:

- explicit font family plus real display and body weights
- readable-text transform policy
- caption maximum lines and wrap policy
- primary and notification component families
- maximum simultaneous components
- paused or seekable GSAP timeline driver
- font measurement after fonts load

Run:

```bash
python3 tools/design_check.py <project_dir>/DESIGN.md
```

Every requested insert must also exist in `EDIT_PLAN.md` with placement mode, original second or spoken-sentence anchor, resolved start, end or duration, layout, audio behavior, entrance/exit behavior, caption evidence, and protected regions.

When semantic motion is used, `MOTION_PLAN.json` must pass:

```bash
python3 tools/motion_plan_check.py <project_dir>/MOTION_PLAN.json
```

When a screenshot reference is used, project-local `STYLE_REFERENCE.md` must record reference strength, extracted visual-language fields, prohibited copied elements, and any static-to-motion inference as `inferred`.

## G3 Preview Gate

Pass when:

- the official preview service is reachable
- main video and audio stay synchronized
- GSAP is present and the timeline is seekable
- evidence text remains readable
- no card, caption, or PiP covers a protected region
- requested demos actually play rather than freeze on one frame
- preview uses a proxy only as a preview asset
- every planned semantic node is implemented with its declared recipe or documented fallback
- `energetic` does not consist only of subtitles and a recurring corner card, and meets the duration-aware coverage check
- computed font family and weight match `DESIGN.md`
- captions obey the declared line policy at representative states
- readable text remains level and baseline-aligned
- focus, typing, and split effects reproduce the same state after seeking
- glass surfaces preserve contrast and do not weaken evidence readability

When the renderer supports lint or inspect commands, run them at all insert boundaries and transitions.

Timer-driven, random, viewport-triggered, or scroll-triggered state fails G3 for a video-time composition.

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
