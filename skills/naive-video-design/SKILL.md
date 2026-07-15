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
3. If style is still unknown, use quick defaults or ask one guided question at a time.
4. Inspect image dimensions and video durations. Never guess how long a supplied demo runs.
5. Fill `EDIT_PLAN.md` with every requested insert: start, end or duration, layout, source-audio behavior, exit, and protected regions.
6. Add semantic cards only in intervals without screenshot or demo conflicts.
7. Write `DESIGN.md` with CSS-friendly color variables, caption rules, card hierarchy, motion density, PiP/mask geometry, and safe zones.
8. Check text contrast and longest-label fit.
9. Run G2 from `references/quality-gates.md`.
10. Set stage to `design_ready` with `tools/state.py` only after G2 passes.

## Rules

- Evidence takes priority over decorative motion.
- Do not invent a personal brand when the user did not provide one.
- Keep colors configurable; do not bake one creator's palette into the public skill.
- Explain semantic cards with short readable text, not full transcript paragraphs.

## Completion

Return the chosen preset, accent, protected regions, number of planned inserts, and next phrase: `按这个设计做官方预览。`
