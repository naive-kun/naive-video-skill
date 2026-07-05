# Style Onboarding

Use this when the user has not provided a visual style.

## Quick Questions

Ask only what is needed. If the user is in a hurry, ask the first two questions and infer the rest.

1. What is your accent color? Provide a hex value if you have one.
2. What style should cards use?
   - Frosted white tool cards
   - Dark tech panels
   - Sticker/pop cards
   - Minimal captions only
3. What subtitle style should the video use?
   - Bold brush subtitle
   - Clean lower-third
   - Platform-style captions
   - Existing brand style
4. What format?
   - 16:9
   - 9:16
   - 1:1
   - Preserve source
5. What should never be covered?
   - Face
   - Screenshots
   - Product UI
   - Existing subtitles
   - Other

## DESIGN.md Schema

Write project-local style choices like this:

```md
# DESIGN

## Visual Style

Short paragraph describing the intended look.

## Colors

- Accent: `<accent_color>`
- Text:
- Card background:
- Subtitle background:

## Captions

Caption style, keyword color, placement, and line rules.

## Cards

Card structure, typography, animation style, and safe zones.

## Motion

GSAP primitives and pacing.

## Do Not

- Do not cover faces.
- Do not cover evidence screenshots.
- Do not change source audio timing.
```
