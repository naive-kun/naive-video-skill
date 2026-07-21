# Screenshot Style Reference Workflow

Use a screenshot to extract visual language, not protected identity or content. The output belongs in the user's project as `STYLE_REFERENCE.md`; never copy the source path or extracted private content into this repository.

## Trigger

Examples:

- `参考这张截图设计视频风格：<图片路径>`
- `按这张图的视觉语言做，但不要复制其中的品牌和内容。`

## Strength

- `low`: color palette and overall tone only.
- `medium`: color, hierarchy, typography class, card geometry, spacing, and composition. Recommended default.
- `high`: closely match the visual language while still prohibiting copied logos, watermarks, people, original wording, branded UI, or a complete recognizable interface.

## Required Extraction

Record:

1. Primary, secondary, background, surface, text, and muted colors.
2. Typography category and size hierarchy, not a copyrighted font claim unless verified.
3. Card shape, corner radius, border, and shadow character.
4. Whitespace, grid, gaps, and internal padding.
5. Primary/secondary information hierarchy.
6. Visual density.
7. Person, evidence, caption, and card composition zones.
8. Reusable abstract elements such as dividers, chips, highlights, or frames.
9. Prohibited copying: logos, watermarks, people, brand UI, original wording, complete layouts that remain uniquely recognizable.
10. Motion directions inferred from the static image. Mark each as `inferred` and connect it to a compatible recipe ID.

## Accuracy Boundary

A still image contains no timing evidence. Never claim to reproduce its original animation, easing, choreography, or duration. Phrase motion choices as design inferences and validate them through the official preview.

## Handoff To Motion Planning

Use extracted hierarchy and composition to choose safe regions first, then select recipes from `motion-recipes.md`. High visual similarity never overrides evidence readability, face safety, captions, or source timing.
