# Style Onboarding

Collect the smallest style profile that can produce a safe preview.

## Guided Mode

Ask one question at a time:

1. What format: preserve source, 16:9, 9:16, or 1:1?
2. Do you have a screenshot whose color, hierarchy, card shape, or composition you like? Explain that this is optional and will not copy its brand, logo, person, wording, or complete UI.
3. If a screenshot is supplied, recommend `medium` reference strength unless the user chooses `low` or `high`.
4. Otherwise, which preset: clean, dark, sticker, or minimal?
5. What accent color? Accept a color name or hex. Offer to keep the preset default.
6. What must never be covered?
7. Motion density: restrained, balanced, or energetic?

Skip questions whose answers can be inferred from a supplied reference.

## Quick Mode

When the user says to decide for them:

- Preserve source aspect ratio.
- Use `clean`.
- Use an accessible neutral-blue accent.
- Use balanced motion.
- Protect face, existing captions, screenshots, and product UI.

Tell beginners they can start with no reference image and change the style after the first preview.

## Reference Strength

- `low`: borrow color and overall tone only.
- `medium`: also borrow hierarchy, card geometry, spacing, and composition. Recommended default.
- `high`: closely match the visual language while still prohibiting copied branding, people, wording, or a complete recognizable UI.

Static screenshots cannot prove the original motion. Any motion direction derived from them must be labeled `inferred`.

## Motion Density

- `restrained`: essential transitions and emphasis only; best for dense evidence.
- `balanced`: regular semantic motion with quiet intervals around screenshots and demos.
- `energetic`: broader semantic coverage and varied recipes. It must not collapse into captions plus one recurring corner card. The duration-aware checker recommends at least six independent semantic nodes for a 15-second showcase and scales more slowly for longer videos.

## Presets

### clean

Light translucent cards, dark text, one accent color, restrained shadows, clear hierarchy. Good for tutorials and professional recaps.

### dark

Dark high-contrast cards, light text, one bright accent. Good for technical or cinematic content. Never place dark panels over dark evidence screenshots.

### sticker

Compact sticker-like labels with spring motion and limited rotation. Good for energetic short-form content. Keep screenshot scenes restrained.

### minimal

Captions, keyword emphasis, and only essential callouts. Good for dense evidence and long demos.

## DESIGN.md Contract

Write:

```md
# DESIGN

## Profile
- Preset:
- Accent:
- Aspect ratio:
- Motion density:
- Reference image: none | project-local path
- Reference strength: none | low | medium | high

## Captions
- Style:
- Position:
- Keyword behavior:

## Cards
- Surface:
- Typography:
- Maximum simultaneous cards:

## Safe Zones
- Face:
- Existing captions:
- Screenshots/UI:

## Motion
- Enter:
- Emphasis:
- Exit:

## Do Not
- Do not change source timing or master audio.
- Do not cover evidence.
```

Use CSS variables such as `--accent`, `--surface`, `--text`, and `--muted` so a user can change color without rewriting motion logic.
