# GSAP Semantic Motion Recipes

Load this reference when planning or implementing semantic motion. Recipes use GSAP core primitives already present in the project. Never install an effects package just to satisfy a recipe.

Read [visual-quality-rules.md](visual-quality-rules.md) for typography, component geometry, public/private style boundaries, and deterministic adaptation of web-component behavior. These recipes define motion roles; they do not prescribe a creator's colors, fonts, or card system.

## Density Policy

- `restrained`: essential emphasis only; protect evidence-heavy intervals.
- `balanced`: varied semantic nodes with quiet breathing room.
- `energetic`: broad semantic coverage. A 15-second showcase should contain at least 6 independent nodes. For longer timelines, the checker adds nodes slowly rather than repeating an effect every few seconds.

Evidence, face, product UI, and caption protected regions always override density.

## Semantic Mapping

| Intent tag | Typical caption cues | Preferred recipes |
|---|---|---|
| `number` | digits, percentages, counts, prices, durations | `counter-roll`, `impact-pop` |
| `list` | first/second, steps, multiple items | `stagger-list`, `split-reveal` |
| `compare` | versus, before/after, but, higher/lower | `compare-split`, `before-after-reveal`, `focus-frame` |
| `warning` | risk, danger, do not, failure | `warning-shake`, `spotlight-mask`, `split-reveal`, `glass-notification` |
| `process` | workflow, steps, then, sequence | `connector-flow`, `timeline-lock`, `seekable-type`, `split-reveal` |
| `causality` | because, therefore, leads to | `connector-flow`, `spotlight-mask` |
| `task-transfer` | assign, hand off, route to | `connector-flow` |
| `confirmation` | approve, confirm, passed, accepted | `approval-stamp`, `scan-verify`, `glass-notification` |
| `result` | result, completed, finally, outcome | `before-after-reveal`, `impact-pop`, `seekable-type`, `split-reveal`, `glass-notification` |
| `question` | why, how, whether, question mark | `spotlight-mask`, `impact-pop`, `focus-frame` |
| `verify` | check, scan, validate, inspect | `scan-verify`, `focus-frame` |
| `timeline` | sync, locked timing, aligned audio | `timeline-lock` |

## Recipe Catalog

### impact-pop
- `recipe_id`: `impact-pop`
- Semantic tags: `number`, `result`, `question`
- Recommended duration: 0.45-1.20s
- GSAP primitives: `fromTo`, `scale`, `y`, `autoAlpha`, `back.out`
- Enter: scale 0.72 to 1 with short upward travel.
- Emphasis: one restrained scale pulse.
- Exit: autoAlpha down with 8-16px upward travel.
- Safe area: centered safe area or verified empty side; never over eyes or caption line.
- No-plugin fallback: GSAP core scale and opacity.
- Not for: long paragraphs, screenshot body text, repeated every sentence.

### stagger-list
- `recipe_id`: `stagger-list`
- Semantic tags: `list`, `process`
- Recommended duration: 0.90-2.80s
- GSAP primitives: `timeline`, `from`, `y`, `autoAlpha`, `stagger`, `back.out`
- Enter: items rise and fade in sequentially.
- Emphasis: active item receives a small accent pulse.
- Exit: reverse stagger or grouped fade.
- Safe area: dedicated column with fixed row height.
- No-plugin fallback: core timeline with numeric stagger.
- Not for: screenshots already containing dense lists or fewer than two items.

### counter-roll
- `recipe_id`: `counter-roll`
- Semantic tags: `number`
- Recommended duration: 0.70-1.80s
- GSAP primitives: `to`, numeric object tween, `snap`, `textContent` update
- Enter: label fades in before value begins.
- Emphasis: value rolls to target and settles with a short pulse.
- Exit: grouped fade or scale to 0.96.
- Safe area: fixed-width numeric container; preserve units and sign.
- No-plugin fallback: tween a JavaScript number and update text content; no TextPlugin.
- Not for: phone numbers, IDs, dates, or values that must not appear approximate.

### scan-verify
- `recipe_id`: `scan-verify`
- Semantic tags: `verify`, `confirmation`
- Recommended duration: 1.00-2.20s
- GSAP primitives: `timeline`, `xPercent` or `yPercent`, `autoAlpha`, `scale`
- Enter: verification frame fades in without covering evidence.
- Emphasis: thin scan line crosses the target, then check indicator resolves.
- Exit: line retracts and frame fades.
- Safe area: scan only a declared target rectangle; no full-screen dark veil.
- No-plugin fallback: transform a plain DOM line with GSAP core.
- Not for: text that becomes unreadable under a tint or decorative continuous scanning.

### connector-flow
- `recipe_id`: `connector-flow`
- Semantic tags: `process`, `causality`, `task-transfer`
- Recommended duration: 1.20-3.20s
- GSAP primitives: `timeline`, `scaleX`, `x`, `autoAlpha`, `stagger`
- Enter: nodes appear in logical order.
- Emphasis: connector grows from origin to destination and active node pulses.
- Exit: destination resolves first, then group fades.
- Safe area: route around protected regions; connectors stay thin and local.
- No-plugin fallback: div/SVG line transformed with core `scaleX`; no DrawSVG requirement.
- Not for: ambiguous direction, decorative networks, or paths crossing a face.

### timeline-lock
- `recipe_id`: `timeline-lock`
- Semantic tags: `timeline`, `process`
- Recommended duration: 1.00-2.40s
- GSAP primitives: `timeline`, `x`, `scaleX`, `autoAlpha`, `back.out`
- Enter: audio and video ticks arrive on parallel tracks.
- Emphasis: playheads meet and lock indicator snaps in.
- Exit: tracks compress and fade together.
- Safe area: horizontal band outside captions and source controls.
- No-plugin fallback: core transforms and a text/symbol lock indicator.
- Not for: actual retiming or any implication that source audio was altered.

### compare-split
- `recipe_id`: `compare-split`
- Semantic tags: `compare`
- Recommended duration: 1.20-3.00s
- GSAP primitives: `timeline`, `xPercent`, `clipPath` when supported, `autoAlpha`
- Enter: left and right treatments arrive from opposite sides.
- Emphasis: one shared divider or alternating highlight.
- Exit: panels separate outward.
- Safe area: two stable columns; neither may cover evidence or face.
- No-plugin fallback: overflow-hidden wrappers with core x transforms.
- Not for: one-sided evidence, narrow layouts without readable columns.

### spotlight-mask
- `recipe_id`: `spotlight-mask`
- Semantic tags: `warning`, `causality`, `question`
- Recommended duration: 0.90-2.00s
- GSAP primitives: `autoAlpha`, `scale`, CSS `clip-path` or radial overlay
- Enter: surrounding emphasis layer fades in while target remains clear.
- Emphasis: target breathes once.
- Exit: mask expands or fades away.
- Safe area: target rectangle must be declared; overlay opacity must preserve readability.
- No-plugin fallback: four translucent DOM panels around the target.
- Not for: unknown target coordinates, faces, or already dark evidence.

### approval-stamp
- `recipe_id`: `approval-stamp`
- Semantic tags: `confirmation`, `result`
- Recommended duration: 0.60-1.40s
- GSAP primitives: `fromTo`, `scale`, `rotation`, `autoAlpha`, `back.out`
- Enter: stamp lands with slight rotation and scale overshoot.
- Emphasis: one tiny settle or shadow pulse.
- Exit: lift and fade.
- Safe area: adjacent to the confirmed item, never on its body text.
- No-plugin fallback: plain DOM badge with core transforms.
- Not for: unverified claims, automated approval presented as human approval.

### warning-shake
- `recipe_id`: `warning-shake`
- Semantic tags: `warning`
- Recommended duration: 0.45-1.00s
- GSAP primitives: `timeline`, `x`, `rotation`, `autoAlpha`
- Enter: quick fade or short scale-in.
- Emphasis: 2-4 diminishing x offsets, then return exactly to zero.
- Exit: clean fade after the spoken warning.
- Safe area: compact warning area outside face and evidence.
- No-plugin fallback: core timeline offsets; no RoughEase requirement.
- Not for: long continuous shake, accessibility-sensitive repeated flashing.

### before-after-reveal
- `recipe_id`: `before-after-reveal`
- Semantic tags: `compare`, `result`
- Recommended duration: 1.40-3.50s
- GSAP primitives: `timeline`, `clipPath` or overflow mask, `xPercent`, `autoAlpha`
- Enter: before state establishes first.
- Emphasis: reveal boundary moves once to expose after state.
- Exit: after state holds briefly, then fades.
- Safe area: both states share a fixed frame and readable scale.
- No-plugin fallback: overflow-hidden wrapper with translated inner layer.
- Not for: unrelated images, misleading edits, or evidence requiring simultaneous comparison.

### focus-frame
- `recipe_id`: `focus-frame`
- Semantic tags: `question`, `verify`, `compare`
- Recommended duration: 0.80-2.40s
- GSAP primitives: `timeline`, `x`, `y`, `width`, `height`, `filter`, `autoAlpha`
- Enter: establish a stable word or label group, then resolve the first measured target.
- Emphasis: move one outline or four corner marks between targets while inactive words receive only mild blur.
- Exit: clear blur first, then fade the frame.
- Safe area: use inside a structured component; measure after fonts load.
- No-plugin fallback: absolutely positioned DOM corners moved by GSAP core.
- Not for: full-screen loose typography, unreadable blur, timer-driven cycling, or targets measured before fonts load.

### seekable-type
- `recipe_id`: `seekable-type`
- Semantic tags: `process`, `result`
- Recommended duration: 0.70-2.20s
- GSAP primitives: `timeline`, `steps`, deterministic textContent update, cursor autoAlpha
- Enter: reveal a short auxiliary line from timeline time with a fixed character count.
- Emphasis: cursor blinks a finite number of times, then settles.
- Exit: fade the complete line as one unit; do not run a deletion loop.
- Safe area: compact status or prompt area with fixed width.
- No-plugin fallback: derive `text.slice(0, count)` from normalized progress.
- Not for: captions, paragraphs, random speed, infinite loops, setTimeout, or viewport visibility triggers.

### split-reveal
- `recipe_id`: `split-reveal`
- Semantic tags: `list`, `process`, `result`, `warning`
- Recommended duration: 0.60-1.80s
- GSAP primitives: `fromTo`, `y`, `autoAlpha`, `stagger`, optional installed SplitText
- Enter: reveal words by default; use characters only for very short emphasis.
- Emphasis: settle the complete phrase before other motion begins.
- Exit: animate the wrapper or grouped targets, then revert stale split instances when rebuilding.
- Safe area: inside a structured component with explicit overflow behavior.
- No-plugin fallback: wrap words in spans and stagger with GSAP core.
- Not for: long body copy, pre-font measurement, dense per-character animation, or ScrollTrigger in a video-time composition.

### glass-notification
- `recipe_id`: `glass-notification`
- Semantic tags: `warning`, `confirmation`, `result`
- Recommended duration: 0.80-2.20s
- GSAP primitives: `fromTo`, `y`, `scale`, `autoAlpha`, `back.out`, short progress sweep
- Enter: the complete aligned notification settles as one component.
- Emphasis: resolve one icon, status dot, or progress line without shifting text baselines.
- Exit: grouped fade and short vertical travel.
- Safe area: verified empty region with sufficient contrast against the source.
- No-plugin fallback: translucent DOM surface, border, and core transforms.
- Not for: recreating a branded operating-system screen, weak contrast, excessive blur, or stacking many simultaneous notices.
