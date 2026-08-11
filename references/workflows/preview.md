# Naive Video Preview

Build the reviewable visual layer while keeping the main video and audio as the master clock.

Resolve `<skill_root>` by locating the installed `talking-head-video-pipeline/SKILL.md`; do not assume the user's current directory is the skill directory.

## Preconditions

Read:

- `.naive-video-state.json`
- `EDIT_PLAN.md`
- `DESIGN.md`
- `MOTION_PLAN.json` when semantic motion is requested
- `CONTENT_LOGIC.json` when captions drive explanatory motion
- `STYLE_REFERENCE.md` when a screenshot reference is used
- relevant active rules in `VIDEO_LESSONS.md`
- `references/layout-safety.md`
- `references/quality-gates.md`
- `references/visual-quality-rules.md`
- `references/gsap-runtime.md`
- `references/motion-recipes.md` when `MOTION_PLAN.json` exists
- `references/shotcraft-integration.md` when any motion node has `reference.provider=video-shotcraft`
- `references/shotcraft-default-pack.md` when automatic references are present

Require G0, G1 when captions are used, and G2. If G2 is incomplete, return to the internal design workflow instead of inventing layout during rendering.

## Workflow

1. Verify every requested asset exists and every insert has a start and end or duration.
2. Mark face, screenshot, UI, and caption protected regions.
3. If browser playback of the source is unreliable, create an H.264 preview proxy. Record that it is preview-only.
4. Validate `DESIGN.md` with `python3 <skill_root>/tools/design_check.py <project_dir>/DESIGN.md`, then validate `MOTION_PLAN.json` with `python3 <skill_root>/tools/motion_plan_check.py <project_dir>/MOTION_PLAN.json` before authoring animation. If using an offline GSAP folder, also run `python3 <skill_root>/tools/gsap_check.py <gsap_directory>`.
5. When captions drive explanatory motion, require a ready `CONTENT_LOGIC.json` and validate it. A pending bootstrap placeholder does not block caption-only, asset-only, or direct-layout work. Then build an HTML composition with one paused, seekable GSAP timeline. Implement each node by its `recipe_id`; do not substitute one generic card animation for the complete plan.
6. For ShotCraft-referenced nodes, keep the native recipe as fallback. Build the curated default pack from `references/shotcraft-default-pack.md` inside the same seekable timeline; it must not require the provider repository or Remotion at runtime.
7. Use transforms and opacity for motion: scale, y, autoAlpha, back.out, elastic.out, stagger, restrained pulse or shake.
8. Use only GSAP capabilities already present. Prefer core plus only the required production plugins. If a plugin is unavailable, apply the recipe's no-plugin fallback and keep the preview working.
9. Reduce motion density during evidence screenshots and demos.
10. Use the user's requested PiP or mask geometry. Preserve main audio.
11. For a first project, new style, reasoning-heavy layout, or user-requested staged review, render static keyframes before a full preview. Cover the opening, every major logic-group peak, the densest state, all evidence/PiP layouts, major transitions, and the ending. Record paths and status in `qa/KEYFRAME_REVIEW.md`.
12. Resolve static composition, font, hierarchy, and occlusion failures before spending time on a complete preview. Static approval does not approve timing.
13. Run HyperFrames lint and inspect commands when available.
14. Build the dynamic preview only after the keyframe gate passes or the user explicitly skips it. Inspect every insert boundary, logic-group accumulation/exit, demo start/end, PiP transition, and final callout. Also inspect the computed font family and weight, caption line count, text baseline, longest label, and container alignment at representative states.
15. Start the official preview service and verify the URL responds.
16. Write the URL to state and set stage to `preview_ready`; approval remains pending.

## Hard Checks

- Demo video must move through time; a frozen first frame fails G3.
- Screenshot text must remain readable.
- No caption or card may cover protected evidence.
- Preview proxy must never become the final base.
- Do not render the final while approval is pending unless the user explicitly skips the gate.
- `energetic` previews fail when the motion plan contains only captions and one recurring corner card, or misses the duration-aware minimum from the checker.
- A screenshot reference controls visual language only. Do not reproduce its logo, watermark, person, original text, or full branded UI.
- Do not use ScrollTrigger, IntersectionObserver, timers, random timing, or framework state as the video clock. Adapt focus, typing, and split effects to the seekable timeline.
- Wait for fonts to load before measuring focus rectangles, wrapping captions, or splitting text.
- Keep readable text nodes level; apply intentional rotation or perspective only to a containing component.
- Reject unrequested hand-drawn-looking arrows, crude boxes, thin oversized loose type, crooked baselines, and arbitrary one-line/two-line caption switching.
- Reject motion that clears every sentence or lets one logic group leak into the next without a declared accumulation/exit decision.
- Reject ShotCraft references that overlap `evidence_intervals`, lack a native fallback recipe, or require the external provider at runtime.
- A `remotion-subclip` needs explicit approval and a muted pre-rendered asset before preview; it never supplies master audio.

## Completion

Return the official preview URL and a short list of requested insert times. Ask the user to confirm visible motion and layout.
