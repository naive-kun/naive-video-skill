# GSAP Runtime For Video Compositions

Use GSAP as the deterministic motion runtime for HyperFrames compositions. A video is driven by a timecode, not page scrolling or user input.

## Preferred Installation

For projects that already use npm:

```bash
npm install gsap
```

Register only the plugins the composition actually uses:

```js
import { gsap } from "gsap";
import { SplitText } from "gsap/SplitText";

gsap.registerPlugin(SplitText);
```

Do not run package installation silently. Obtain approval when adding a dependency to the user's project.

## Offline Browser Files

An already downloaded official GSAP distribution may be used without npm. Prefer the minified browser files and copy only the files required by the current project into a project-local runtime folder. Do not copy an arbitrary personal download directory into this public skill repository.

Minimum:

```text
gsap.min.js
```

Useful optional production plugins:

- `SplitText.min.js`: measured word/character reveals after fonts load; always provide a core-span fallback.
- `Flip.min.js`: deterministic layout-state transitions when the same component changes geometry.
- `ScrambleTextPlugin.min.js`: very short system/status text only; never normal captions or evidence text.
- `DrawSVGPlugin.min.js`: polished diagrams or UI paths only; never use it to imitate rough hand-drawn arrows.
- `MorphSVGPlugin.min.js` and `MotionPathPlugin.min.js`: occasional semantic shape/path transitions, only when they improve meaning.

Development only:

- `GSDevTools`: useful while authoring, never required in the delivered composition.

Normally exclude from fixed-time video compositions:

- `ScrollTrigger` and `ScrollSmoother`;
- `Observer`, `Draggable`, and `InertiaPlugin`;
- timers, intersection observers, random clocks, or user-input-driven state.

These tools solve webpage interaction, not deterministic video playback. Adapt the visual behavior to one paused GSAP timeline and seek it from the video clock.

## Version And License Check

Before using an offline folder:

```bash
python3 <skill_root>/tools/gsap_check.py <gsap_directory>
```

The checker verifies that a core runtime exists, reports detected versions, catches mixed plugin versions, and lists production/development/input-oriented files. Preserve the copyright/license header and review the official GSAP standard license before redistributing GSAP files. This repository's MIT license does not automatically relicense vendor JavaScript.

## Seek-Safe Contract

- Create one paused `gsap.timeline()`.
- Register plugins once.
- Wait for `document.fonts.ready` before text measurement or splitting.
- Build the full timeline before frame rendering.
- Seek by absolute composition time for every frame.
- Use fixed values; no randomness or wall-clock timers.
- Revert or clean up SplitText instances after rebuilding.
- Every plugin-based recipe needs a GSAP-core fallback.

See [motion-recipes.md](motion-recipes.md) and [visual-quality-rules.md](visual-quality-rules.md) for semantic and design constraints.
