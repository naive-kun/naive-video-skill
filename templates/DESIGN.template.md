# DESIGN

## Profile

- Preset: clean
- Accent: #2F7DF4
- Aspect ratio: preserve source
- Motion density: balanced
- Reference image: none
- Reference strength: none

## Typography

- Font family: system sans-serif stack or project-bundled local font
- Display weight: 700 bold
- Body weight: 500 medium
- Text transform: level readable text; animate the container; no rotation or skew on labels

## Captions

- Style: bold readable captions
- Position: safe lower area
- Keyword behavior: one accent color, restrained emphasis
- Maximum lines: 1
- Wrap policy: shorten copy or reduce font within bounds before allowing a second line

## Components

- Primary family: structured card with explicit hierarchy and aligned rows
- Notification family: compact glass notification for status, warning, confirmation, or CTA
- Surface: configurable; high contrast against the underlying frame
- Maximum simultaneous components: 1 unless evidence layout requires otherwise

## Safe Zones

- Face: protect
- Existing captions: protect
- Screenshots and product UI: protect body text and controls

## Motion

- Semantic plan: `MOTION_PLAN.json`
- Timeline driver: one paused, seekable GSAP timeline
- Font measurement: after `document.fonts.ready`
- Enter: scale, y, autoAlpha, back.out
- Emphasis: short pulse or subtle shake
- Exit: autoAlpha and y, complete before next protected asset

## Do Not

- Do not change source timing or master audio.
- Do not cover evidence.
- Do not blur screenshots.
- Do not use thin oversized loose type, hand-drawn-looking graphics, or skewed readable text unless explicitly requested.
- Do not embed a creator-specific palette or component system in a public default.
