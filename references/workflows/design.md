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

1. Read `references/style-onboarding.md`, `references/asset-onboarding.md`, `references/content-logic-workflow.md`, `references/layout-safety.md`, `references/visual-quality-rules.md`, and `references/gsap-runtime.md`.
2. Reuse active confirmed profile rules. Project-specific instructions override the profile for this video only.
3. If style is still unknown, use quick defaults or ask one guided question at a time. Offer beginners an optional screenshot reference; do not require one.
4. If visual assets exist and placement mode is not already known, ask whether the user wants semantic placement or exact seconds/spoken-sentence anchors. Recommend semantic placement for speed, but say exact anchors are more precise; accept a hybrid.
5. Inspect image dimensions and video durations. Never guess how long a supplied demo runs.
6. Fill `EDIT_PLAN.md` with the placement mode and every requested insert: original anchor, resolved start, end or duration, layout, source-audio behavior, entrance, exit, caption evidence, and protected regions.
7. Build `CONTENT_LOGIC.json` from complete viewer-facing reasoning units rather than punctuation. Use word timing when available; otherwise declare cue-level or manual precision. Let input/support/relation/result beats accumulate only while they help explain one group, then exit the group together.
8. Run `python3 <skill_root>/tools/content_logic_check.py <project_dir>/CONTENT_LOGIC.json`. For a first project, new style, or reasoning-heavy video, show the group summaries before motion authoring.
9. Read `references/motion-recipes.md`. Match logic beats and caption evidence to recipes and write `MOTION_PLAN.json` from `templates/MOTION_PLAN.template.json`. Every derived node needs `logic_group_id`, `logic_beat_id`, caption evidence, start/end, region, visual role, and fallback behavior.
10. For newly initialized projects, run the curated automatic ShotCraft reference branch after native recipes are selected unless the user chose `skip`. Existing approved projects keep their recorded setting. Record evidence intervals before selecting cards.
11. Add semantic cards only in intervals without screenshot or demo conflicts. Evidence intervals reduce density and may suppress decorative nodes.
12. Write `DESIGN.md` with CSS-friendly color variables, an explicit typography contract, caption maximum lines and wrap policy, component families, motion density, PiP/mask geometry, and safe zones. Keep creator-specific styling in the private profile rather than the public default.
13. Check the intended font family and real weight, text baseline, longest-label fit, caption line policy, and glass-surface contrast.
14. Run `design_check.py`, `content_logic_check.py`, and `motion_plan_check.py`, then G2 from `references/quality-gates.md`.
15. Set stage to `design_ready` with `tools/state.py` only after G2 passes.

## Screenshot Reference Branch

Trigger on phrases such as `参考这张截图设计视频风格` or `按这张图的视觉语言做，但不要复制其中的品牌和内容`.

1. Read `references/style-reference-workflow.md`.
2. Confirm the image path and infer reference strength only when the user already states it; otherwise recommend `medium` in plain language.
3. Inspect the image and write project-local `STYLE_REFERENCE.md` from `templates/STYLE_REFERENCE.template.md`.
4. Extract colors, typography class and hierarchy, card geometry, spacing, information hierarchy, density, composition zones, reusable visual elements, and prohibited copied elements.
5. Mark motion directions inferred from a static image as `inferred`; never claim exact reconstruction of the source animation.
6. Translate the resulting visual language into `DESIGN.md`, then select compatible recipes from `references/motion-recipes.md`.

Never copy a logo, watermark, person, brand UI, original wording, or a complete recognizable interface. Keep the reference image path in the user's project only.

## ShotCraft Reference Branch

Trigger for new projects whose `Shot references` setting is `automatic`, or when the user asks for ShotCraft, selects a card, or enables cinematic shot recommendations.

1. Read `references/shotcraft-integration.md`, `references/shotcraft-default-pack.md`, and the local `references/shotcraft-mapping.json`.
2. Keep the already selected native `recipe_id`; ShotCraft never becomes the semantic source of truth.
3. For automatic mode, run `python3 <skill_root>/tools/shotcraft_default_plan.py <project_dir>/MOTION_PLAN.json --in-place`. This adds only safe, semantically matching references and never installs a provider. For manual browsing, query `shotcraft_catalog.py --defaults --semantic <tag> --density <density> --json`.
4. Respect the density cap from the default pack. Prefer different semantic roles instead of repeating one card.
5. Write screenshot, demo, and product-UI ranges to top-level `evidence_intervals`. Do not assign a mapped reference across those intervals.
6. Add `reference.provider`, `reference.card`, `reference.implementation`, and `reference.provider_required_at_runtime=false` to the selected nodes.
7. Use `gsap-adapted` or `hyperframes-custom` by default. If a selected complex card genuinely needs Remotion, explain the added runtime, download, license, and render cost first. Only after explicit approval may `remotion_runtime.py --install --yes` be used and the node changed to `remotion-subclip`.
8. Continue normally when the provider is absent; `reference-only` recommendations do not require installation.

## Rules

- Evidence takes priority over decorative motion.
- Do not invent a personal brand when the user did not provide one.
- Keep colors configurable; do not bake one creator's palette into the public skill.
- Explain semantic cards with short readable text, not full transcript paragraphs.
- Keep captions and cards separate: captions preserve speech; logic beats preserve the takeaway.
- Keep readable text level and baseline-aligned. Animate a wrapper instead of skewing or rotating labels, captions, or button text.
- Treat GSAP as the motion layer, not a substitute for typography, spacing, surface, or component geometry.
- Use focus-frame, seekable-type, split-reveal, and glass-notification only for their declared semantic roles and record a deterministic fallback.
- Use only GSAP capabilities already available in the project. If a plan names an unavailable plugin, use the recorded no-plugin fallback.
- Never install ShotCraft or Remotion during design. The automatic default pack requires neither. Offer the project-local Remotion setup only after explicit user consent for a specific complex node.
- A ShotCraft reference enriches composition and pacing; it must not replace its node's native recipe or appear during readable evidence.
- Do not vendor a personal GSAP download into the public skill. Use project-local npm installation or selected official browser files after `tools/gsap_check.py` passes.
- `energetic` is a coverage goal, not permission to cover evidence or stack effects mechanically.

## Completion

Return the chosen preset, accent, protected regions, number of planned inserts, and next phrase: `按这个设计做官方预览。`
