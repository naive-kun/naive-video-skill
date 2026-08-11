# ShotCraft Integration

Use ShotCraft as an optional shot-language reference provider. The bundled beginner pack is independently implemented with native HyperFrames + GSAP, so it works even when ShotCraft and Remotion are absent. ShotCraft does not replace this Skill's state machine, semantic recipe, master-audio clock, protected regions, preview gate, or final export path.

## Beginner Choices

New projects use the recommended automatic pack. In guided mode, offer one plain-language choice:

1. `automatic` (recommended): adapt a few suitable cards with native HyperFrames + GSAP, capped by density.
2. `gallery`: use card names the user selected from ShotCraft.
3. `skip`: use the base native GSAP recipe library without the curated shot layer.

Quick mode selects `automatic`. Explain that the default pack is local and that this Skill never clones, installs, or updates ShotCraft or Remotion silently. Preserve existing approved projects instead of injecting the new default retroactively.

## Discovery

`tools/shotcraft_catalog.py` checks, in order:

1. an explicit `--root` path;
2. `VIDEO_SHOTCRAFT_HOME`;
3. `~/.naive-video/providers/video-shotcraft`;
4. `~/.codex/skills/video-shotcraft`;
5. `~/.claude/skills/video-shotcraft`;
6. `~/.agents/skills/video-shotcraft`.

Without a local provider it still returns the bundled mapping as `reference-only`. It never uses the network and never blocks native motion planning.

## Planning Contract

Every ShotCraft-inspired node keeps its native `recipe_id`. Add only this optional metadata:

```json
{
  "reference": {
    "provider": "video-shotcraft",
    "card": "list-reveal",
    "implementation": "gsap-adapted",
    "provider_required_at_runtime": false
  }
}
```

The native recipe is the deterministic fallback and remains the semantic source of truth. A reference card may refine composition, pacing, or transition language; it must not introduce copied branding, text, or product UI.

Use the density-aware cap in `default_pack`: restrained 1, balanced 3, energetic 4. These are maxima, not quotas. Do not mechanically assign a reference to every caption.

Set top-level `evidence_intervals` in `MOTION_PLAN.json` for screenshots, demos, product UI, or other readable proof. The checker rejects mapped cards that overlap evidence when `allow_during_evidence` is false.

## Implementation Modes

- `gsap-adapted`: rebuild the shot language with existing seekable GSAP primitives. Default for lists, counters, typing, and filtering.
- `hyperframes-custom`: author a custom HyperFrames component while keeping one paused, seekable GSAP timeline. Default for spotlight, mask, and timeline compositions.
- `remotion-subclip`: exceptional route for complex motion that cannot be adapted economically. The included `tools/remotion_runtime.py` can plan, check, or explicitly install an isolated project-local runtime. Require user approval, dependency and license review, a pre-rendered muted asset, and a native fallback. Never let it retime or replace the master audio.

The first two modes must not require the ShotCraft repository at preview or export time. If a selected provider disappears, implement the recorded native recipe and continue.

## Evidence And Safety

- Evidence intervals override cinematic density.
- Do not cover faces, captions, screenshot body text, product UI, or user-marked safe zones.
- Do not blur or darken evidence to make a reference shot fit.
- Keep readable text level and adapt web interaction or scroll behavior to the video timeline.
- Any `remotion-subclip` is muted before composition; the approved working video's audio remains the clock.

## License Boundary

[video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) is an external Apache-2.0 project. This adapter contains an independently authored mapping and links only; it does not redistribute ShotCraft code, audio, previews, or templates. Remotion has a separate [license](https://www.remotion.dev/license) that must be reviewed before an approved install or commercial use. If a future version copies or modifies upstream code or documentation, preserve the required license and notices and document the copied files.
