# Visual Asset Onboarding

Ask about screenshots, screen recordings, product images, charts, or demo videos before the design plan is finalized.

## Beginner Questions

Ask one question at a time and skip answers already supplied by the user.

1. `这条视频里有没有想展示的截图、录屏、产品图或演示视频？`
2. If yes: `你想让我按口播语义自动安排，还是你自己指定出现的秒数或那句话？`

Explain the placement modes without forcing a choice:

- `semantic`: the agent selects enter, hold, and exit timing from caption meaning. Recommended when the user wants speed or does not know the timeline.
- `exact`: the user supplies a start second, time range, or exact spoken sentence. This is more precise.
- `hybrid`: the user fixes important assets and the agent places the rest semantically.

If the user says `你帮我定`, select `semantic`. If the user supplies seconds or a spoken sentence, select `exact` for that asset. Never ask the same question again after the mode is clear.

## Exact Anchors

Accept either format:

```text
12.5 秒出现，停留 2 秒
说到“这里就是最终效果”时出现，播放完飞出
```

Resolve sentence anchors against SRT, CSV, or word-level timing. Record both the original sentence and resolved seconds in `EDIT_PLAN.md`. If the sentence appears more than once, ask which occurrence before rendering.

## Semantic Placement

For each asset:

1. identify the spoken claim it proves or explains;
2. enter close to that claim, not at an arbitrary decorative beat;
3. keep enough hold time for the asset's readable content;
4. choose an exit that does not cut off the evidence;
5. reduce decorative motion while the asset is visible;
6. record the caption evidence and confidence.

## Evidence Rules

- Inspect dimensions and duration instead of guessing.
- Keep screenshot body text, product UI, faces, and user-marked regions readable.
- Do not crop key evidence or cover it with captions and cards.
- Muting an inserted video does not mute the talking-head master audio.
- A demo video must visibly advance; a frozen first frame is not a valid insert.
- Use a deterministic GSAP enter and exit attached to the video timeline.

## Plan Contract

Record:

- placement mode: `none`, `semantic`, `exact`, or `hybrid`;
- asset path and type;
- requested second or spoken-sentence anchor;
- resolved start/end;
- layout and scale;
- asset audio behavior;
- enter/exit recipe;
- protected regions and review notes.
