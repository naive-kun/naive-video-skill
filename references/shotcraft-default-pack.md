# Curated ShotCraft-Inspired Default Pack

This pack gives new users a stronger visual baseline without requiring ShotCraft, Remotion, copied templates, or third-party effect bundles. It is an independently authored set of HyperFrames + GSAP adaptations linked to native semantic recipes.

## Automatic Selection

- New projects default to `automatic`; existing approved projects are not rewritten.
- Match both `semantic_tag` and `recipe_id`. Never add a shot merely because it looks attractive.
- Maximum references: restrained 1, balanced 3, energetic 4.
- Use one instance of a card before repeating it. Prefer a different information role.
- Skip nodes that overlap evidence intervals, cover protected regions, have no fallback, or last too briefly for the card.
- The default pack requires neither the ShotCraft repository nor Remotion.

Run the deterministic selector after the native plan passes its basic schema checks:

```bash
python3 <skill_root>/tools/shotcraft_default_plan.py \
  <project_dir>/MOTION_PLAN.json --in-place
```

Then run `motion_plan_check.py` again.

## Quality Baseline

All components use stable dimensions, level text, measured fonts, one paused seekable GSAP timeline, and deterministic positions. Use `back.out(1.4-1.8)` for a single settle, not repeated bouncing. Keep blur brief and below roughly 8px. Decorative particles use fixed coordinates rather than runtime randomness.

### spotlight-hero-card

- Trigger: a real question, causal reveal, or verification claim using `spotlight-mask` or `focus-frame`.
- Composition: one compact side card plus a local focus frame; never a full-screen black veil.
- Motion: card `autoAlpha 0 -> 1`, `y 24 -> 0`, `scale .96 -> 1`; focus corners resolve after the card, then one 1.02 pulse.
- Exit: clear any blur first, then fade the complete component.
- Skip: unknown target coordinates, face overlap, evidence-heavy frames, or a caption-only question with no visual target.

### list-reveal

- Trigger: two or more steps or list items using `stagger-list` or `split-reveal`.
- Composition: fixed-height rows in one structured card with a short header and one accent rail.
- Motion: wrapper settles first; rows enter from `y 20` with `autoAlpha` and 0.10-0.16s stagger; the active row gets one short accent sweep.
- Exit: reverse the row stagger only when there is enough time; otherwise fade the group together.
- Skip: dense screenshot lists, one-item claims, or text that cannot fit without shrinking below the design contract.

### counter-confetti

- Trigger: a trustworthy result or number using `counter-roll` or `impact-pop`.
- Composition: fixed-width number, unit, short label, and at most 6-10 tiny deterministic accent pieces.
- Motion: label appears first, number rolls with a numeric object tween, then accent pieces expand once from fixed coordinates and fade.
- Exit: group scales to .97 and fades; particles never loop.
- Skip: IDs, dates, phone numbers, unverifiable figures, evidence screenshots, or restrained mode unless the number is the main result.

### type-and-filter

- Trigger: check, filter, scan, or confirmation using `scan-verify`.
- Composition: short query field, 2-4 filter chips, and one result indicator.
- Motion: deterministic seekable typing reveals a short phrase; chips activate with stagger; a local scan line crosses only the declared result rectangle; check state resolves last.
- Exit: scan line retracts before the component fades.
- Skip: long text, branded UI recreation, full-screen scanning, or any tint that reduces evidence readability.

### timeline-travel

- Trigger: ordered process, task transfer, or timeline lock using `timeline-lock` or `connector-flow`.
- Composition: 3-5 fixed nodes and local connectors routed around protected regions.
- Motion: nodes appear in order; connectors grow with `scaleX`; the active dot travels only between adjacent nodes; the destination receives one settle pulse.
- Exit: destination holds briefly, then the whole track fades together.
- Skip: ambiguous direction, decorative networks, paths crossing a face, or claims that imply the source audio was retimed.

### document-typewriter-reveal

- Trigger: a document/result reveal using `seekable-type`.
- Composition: one compact document surface with a title and at most three short lines.
- Motion: title settles, lines reveal by word spans or a deterministic clipped width, then one finite cursor blink resolves to a stable result state.
- Exit: fade the whole document; never run a deletion loop.
- Skip: captions, paragraphs, copied branded documents, or body text that must be read as evidence.

## Optional Remotion Bridge

Do not use Remotion for this default pack. Reserve it for a user-approved complex subclip whose motion cannot be reproduced economically in the native timeline. Check or plan the isolated runtime first:

```bash
python3 <skill_root>/tools/remotion_runtime.py --project <project_dir> --check
python3 <skill_root>/tools/remotion_runtime.py --project <project_dir> --plan
```

After explicit approval only:

```bash
python3 <skill_root>/tools/remotion_runtime.py \
  --project <project_dir> --install --yes
```

The generated runtime stays under the project, not the public Skill. Review the separate [Remotion license](https://www.remotion.dev/license) before commercial use. Any Remotion subclip is rendered muted, inserted as a visual layer, and retains a native GSAP fallback.
