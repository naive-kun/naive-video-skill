---
name: naive-video-preview
description: Build and validate an official HyperFrames plus GSAP motion preview for a Naive Video Skill project. Use when captions and an edit plan exist and the user asks for animation, semantic cards, screenshot or demo inserts, picture-in-picture, masks, style preview, or an official preview link before final export.
---

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
- `references/motion-recipes.md` when `MOTION_PLAN.json` exists

Require G0, G1 when captions are used, and G2. If G2 is incomplete, route to `naive-video-design` instead of inventing layout during rendering.

## Workflow

1. Verify every requested asset exists and every insert has a start and end or duration.
2. Mark face, screenshot, UI, and caption protected regions.
3. If browser playback of the source is unreliable, create an H.264 preview proxy. Record that it is preview-only.
4. Validate `MOTION_PLAN.json` with `python3 <skill_root>/tools/motion_plan_check.py <project_dir>/MOTION_PLAN.json` before authoring animation.
5. Build an HTML composition with a seekable GSAP timeline. Implement each node by its `recipe_id`; do not substitute one generic card animation for the complete plan.
6. Use transforms and opacity for motion: scale, y, autoAlpha, back.out, elastic.out, stagger, restrained pulse or shake.
7. Use only GSAP capabilities already present. If a plugin is unavailable, apply the recipe's no-plugin fallback and keep the preview working.
8. Reduce motion density during evidence screenshots and demos.
9. Use the user's requested PiP or mask geometry. Preserve main audio.
10. Run HyperFrames lint and inspect commands when available.
11. Inspect every insert boundary, demo start/end, PiP transition, and final callout.
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

## Completion

Return the official preview URL and a short list of requested insert times. Ask the user to confirm visible motion and layout.
