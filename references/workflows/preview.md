# Naive Video Preview

Build the reviewable visual layer while keeping the main video and audio as the master clock.

Resolve `<skill_root>` by locating the installed `talking-head-video-pipeline/SKILL.md`; do not assume the user's current directory is the skill directory.

## Preconditions

Read:

- `.naive-video-state.json`
- `EDIT_PLAN.md`
- `DESIGN.md`
- `MOTION_PLAN.json` when semantic motion is requested
- `STYLE_REFERENCE.md` when a screenshot reference is used
- relevant active rules in `VIDEO_LESSONS.md`
- `references/layout-safety.md`
- `references/quality-gates.md`
- `references/visual-quality-rules.md`
- `references/gsap-runtime.md`
- `references/motion-recipes.md` when `MOTION_PLAN.json` exists

Require G0, G1 when captions are used, and G2. If G2 is incomplete, return to the internal design workflow instead of inventing layout during rendering.

## Workflow

1. Verify every requested asset exists and every insert has a start and end or duration.
2. Mark face, screenshot, UI, and caption protected regions.
3. If browser playback of the source is unreliable, create an H.264 preview proxy. Record that it is preview-only.
4. Validate `DESIGN.md` with `python3 <skill_root>/tools/design_check.py <project_dir>/DESIGN.md`, then validate `MOTION_PLAN.json` with `python3 <skill_root>/tools/motion_plan_check.py <project_dir>/MOTION_PLAN.json` before authoring animation. If using an offline GSAP folder, also run `python3 <skill_root>/tools/gsap_check.py <gsap_directory>`.
5. Build an HTML composition with one paused, seekable GSAP timeline. Implement each node by its `recipe_id`; do not substitute one generic card animation for the complete plan.
6. Use transforms and opacity for motion: scale, y, autoAlpha, back.out, elastic.out, stagger, restrained pulse or shake.
7. Use only GSAP capabilities already present. Prefer core plus only the required production plugins. If a plugin is unavailable, apply the recipe's no-plugin fallback and keep the preview working.
8. Reduce motion density during evidence screenshots and demos.
9. Use the user's requested PiP or mask geometry. Preserve main audio.
10. Run HyperFrames lint and inspect commands when available.
11. Inspect every insert boundary, demo start/end, PiP transition, and final callout. Also inspect the computed font family and weight, caption line count, text baseline, longest label, and container alignment at representative states.
12. Start the official preview service and verify the URL responds.
13. Write the URL to state and set stage to `preview_ready`; approval remains pending.

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

## Completion

Return the official preview URL and a short list of requested insert times. Ask the user to confirm visible motion and layout.
