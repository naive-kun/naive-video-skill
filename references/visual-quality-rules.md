# Visual Quality Rules

Use this reference during design and preview work. It defines brand-neutral quality invariants, not a creator-specific palette or card style.

## Public and Private Boundary

- Keep creator colors, font choices, card geometry, recurring slogans, and brand-specific component names in the private local profile.
- Keep the public Skill configurable. Describe roles such as `primary-card`, `glass-notification`, and `evidence-frame` instead of prescribing one creator's look.
- Promote only reusable correctness rules: readable type, stable alignment, evidence safety, deterministic timing, and explicit fallbacks.

## Typography Contract

Write these decisions into `DESIGN.md` before preview authoring:

- explicit local font family or project-bundled font
- real display and body weights that the font actually provides
- caption maximum line count and wrap policy
- text alignment and baseline policy
- longest-label fit strategy
- font-load point used before measuring or splitting text

Default display text and captions to a verified semibold or bold face. Body copy may use a lighter weight when it remains readable. Do not rely on synthetic browser bolding.

Keep readable text level. Animate a containing card or wrapper when rotation is intentional; do not skew, rotate, or perspective-warp individual labels, button text, captions, or evidence text.

Choose a caption line policy once per layout. A one-line and two-line mixture is allowed only when `DESIGN.md` states the rule. Otherwise shorten copy, adjust the safe width, or use a bounded responsive font size before wrapping.

Wait for `document.fonts.ready` before measuring focus rectangles, line breaks, or SplitText targets.

## Component Families

Choose components by semantic role, then apply the project's visual profile.

### Structured card

Use for explanations, steps, comparisons, and claims that need hierarchy. It needs a surface, title, optional eyebrow, aligned rows, consistent padding, and an explicit exit.

### Glass notification

Use for compact status, warning, confirmation, or CTA moments. The glass treatment comes from translucency, background blur, a restrained border, and controlled shadow. Keep icons and text on a shared baseline. Do not imitate a branded operating-system screen.

### Evidence frame

Use only to clarify a screenshot or demo target. Preserve body text and controls. Avoid decorative frames that imply a scan or approval the evidence does not support.

### Focus frame

Use for a short word or label sequence inside a stable container. Move four corner marks or one outline between measured targets and apply only mild blur to inactive words. Keep all words readable enough to preserve context.

### Seekable type

Use for short auxiliary status text, never for primary captions or long paragraphs. Reveal a deterministic substring from the video playhead, or use a GSAP `steps()` tween. Do not use random speed, timers, deletion loops, or viewport visibility triggers.

### Split reveal

Use for a short title, warning, step label, or result inside a structured component. Split by words by default; use characters sparingly. Revert stale split instances before rebuilding, and create targets only after fonts load.

## Time-Based Video Adaptation

Web components often use `setInterval`, `setTimeout`, `IntersectionObserver`, React state, or ScrollTrigger. A rendered video must instead be deterministic at any seek position.

- Drive every effect from one paused, seekable GSAP timeline.
- Derive visible text, focus index, and active state from timeline time.
- Replace random or humanized timing with fixed values.
- Do not add React or another framework only to obtain one effect; adapt the behavior to the project's existing runtime.
- Do not use ScrollTrigger for a composition controlled by video seconds.
- Register optional plugins once and record a GSAP-core fallback.

## Failure Patterns

Reject the preview when any of these appear without an explicit style request:

- thin oversized loose typography floating over the source video
- hand-drawn-looking arrows, improvised strokes, crude boxes, or cheap grid and scan textures
- skewed readable text, crooked baselines, or icons that do not align with labels
- arbitrary switching between one-line and two-line captions
- full-screen kinetic typography where a structured card or evidence asset would communicate better
- a motion library being used as a substitute for typography, spacing, or component design
- a glass surface with weak contrast, excessive blur, or unreadable screenshot content underneath
- timer-driven, random, or scroll-driven effects that render differently after seeking
- a public default that embeds one creator's colors, fonts, or recurring card system

## Preview Review

At representative key states, verify:

1. the computed font family and weight match `DESIGN.md`
2. captions obey the declared maximum line count
3. text baselines are level and readable text nodes have no skew or rotation
4. icons, labels, and rows share consistent alignment and spacing
5. glass surfaces retain sufficient contrast
6. focus, type, and split effects reproduce the same state after seeking
7. screenshots, demos, faces, and captions remain protected

Record failures against the smallest responsible layer: typography, component geometry, animation, layout safety, or renderer state.
