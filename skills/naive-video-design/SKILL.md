---
name: naive-video-design
description: Design the visual system and complete the timeline plan for a Naive Video Skill project before rendering. Use when the user asks for color or style choices, semantic cards, screenshot and demo placement, PiP or mask layout, richer motion without covering evidence, or wants the agent to decide the visual treatment from captions and supplied assets.
---

# Naive Video Design

Turn captions, assets, and spoken meaning into a render-ready `DESIGN.md` and `EDIT_PLAN.md`.

Resolve `<skill_root>` by locating the installed `talking-head-video-pipeline/SKILL.md`; do not assume the user's current directory is the skill directory.

## Inputs

- project state
- SRT/CSV or transcript
- user-specified inserts and timing
- available screenshots, logos, and demo videos
- explicit style reference or private profile when present

## Workflow

1. Read `references/style-onboarding.md` and `references/layout-safety.md`.
2. Reuse active confirmed profile rules. Project-specific instructions override the profile for this video only.
3. If style is still unknown, use quick defaults or ask one guided question at a time. Offer beginners an optional screenshot reference; do not require one.
4. Inspect image dimensions and video durations. Never guess how long a supplied demo runs.
5. Fill `EDIT_PLAN.md` with every requested insert: start, end or duration, layout, source-audio behavior, exit, and protected regions.
6. Read `references/motion-recipes.md`. Match caption intent to recipes and write `MOTION_PLAN.json` from `templates/MOTION_PLAN.template.json`. Every node needs caption evidence, start/end, region, visual role, and fallback behavior.
7. Add semantic cards only in intervals without screenshot or demo conflicts. Evidence intervals reduce density and may suppress decorative nodes.
8. Write `DESIGN.md` with CSS-friendly color variables, caption rules, card hierarchy, motion density, PiP/mask geometry, and safe zones.
9. Check text contrast and longest-label fit.
10. Run `python3 <skill_root>/tools/motion_plan_check.py <project_dir>/MOTION_PLAN.json`, then G2 from `references/quality-gates.md`.
11. Set stage to `design_ready` with `tools/state.py` only after G2 passes.

## Screenshot Reference Branch

Trigger on phrases such as `参考这张截图设计视频风格` or `按这张图的视觉语言做，但不要复制其中的品牌和内容`.

1. Read `references/style-reference-workflow.md`.
2. Confirm the image path and infer reference strength only when the user already states it; otherwise recommend `medium` in plain language.
3. Inspect the image and write project-local `STYLE_REFERENCE.md` from `templates/STYLE_REFERENCE.template.md`.
4. Extract colors, typography class and hierarchy, card geometry, spacing, information hierarchy, density, composition zones, reusable visual elements, and prohibited copied elements.
5. Mark motion directions inferred from a static image as `inferred`; never claim exact reconstruction of the source animation.
6. Translate the resulting visual language into `DESIGN.md`, then select compatible recipes from `references/motion-recipes.md`.

Never copy a logo, watermark, person, brand UI, original wording, or a complete recognizable interface. Keep the reference image path in the user's project only.

## Rules

- Evidence takes priority over decorative motion.
- Do not invent a personal brand when the user did not provide one.
- Keep colors configurable; do not bake one creator's palette into the public skill.
- Explain semantic cards with short readable text, not full transcript paragraphs.
- Use only GSAP capabilities already available in the project. If a plan names an unavailable plugin, use the recorded no-plugin fallback.
- `energetic` is a coverage goal, not permission to cover evidence or stack effects mechanically.

## Completion

Return the chosen preset, accent, protected regions, number of planned inserts, and next phrase: `按这个设计做官方预览。`
