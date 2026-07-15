# Style Onboarding

Collect the smallest style profile that can produce a safe preview.

## Guided Mode

Ask one question at a time:

1. What format: preserve source, 16:9, 9:16, or 1:1?
2. Which preset: clean, dark, sticker, or minimal?
3. What accent color? Accept a color name or hex. Offer to keep the preset default.
4. What must never be covered?
5. Motion density: restrained, balanced, or energetic?

Skip questions whose answers can be inferred from a supplied reference.

## Quick Mode

When the user says to decide for them:

- Preserve source aspect ratio.
- Use `clean`.
- Use an accessible neutral-blue accent.
- Use balanced motion.
- Protect face, existing captions, screenshots, and product UI.

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
