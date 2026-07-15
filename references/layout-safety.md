# Layout Safety

Use evidence-first composition. Screenshots and demos explain the claim; motion graphics support them.

## Protected Regions

Before adding overlays, mark:

- face and hand-gesture region
- existing subtitles
- screenshot body text
- product navigation and buttons
- watermarks and legal labels
- user-specified no-cover areas

## Placement Order

1. Evidence asset.
2. Face or speaker PiP.
3. Main captions.
4. Semantic card in remaining empty space.
5. Decorative motion only if space remains.

## Screenshot Rules

- Prefer contain over crop when text matters.
- Do not blur, darken, or place a large translucent panel over screenshot text.
- Do not add scan boxes or moving outlines unless the user explicitly asks.
- Use short entrance and exit motion; keep the evidence still enough to read.
- When two screenshots share the frame, size them for legibility rather than symmetry.

## PiP Rules

- Use a circle or rounded crop only when requested or established by the user's profile.
- Keep PiP clear of captions and evidence.
- Animate position, scale, and opacity; do not warp the face.
- Preserve the main speaker audio even when the speaker image becomes PiP.

## Collision Check

At each insert boundary, verify:

- no overlap between caption and evidence
- no overlap between card and evidence
- no face occlusion
- text fits its container
- exit animation completes before the next protected asset begins

If the scene is crowded, remove the semantic card first.
