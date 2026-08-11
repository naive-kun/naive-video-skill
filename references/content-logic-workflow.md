# Content Logic and Word-Timeline Workflow

Use this reference after captions are available and before semantic motion is planned. It separates what the speaker said from what the viewer needs to understand.

## Timing Sources

Prefer timing in this order:

1. Existing word-level transcript data.
2. A normalized `edit/word-timeline.json` with `text`, `startMs`, and `endMs` per token.
3. Cue-level SRT timing when word timing is unavailable.
4. Explicit manual anchors supplied by the user.

The spoken audio remains timing truth. A script may correct wording but must not replace real timing. Record `timing_precision` as `word-level`, `cue-level`, or `manual`; do not imply word precision when only cue starts are known.

## Logic Groups

Create project-local `CONTENT_LOGIC.json` from `templates/CONTENT_LOGIC.template.json`.

Group by complete viewer-facing reasoning units, not punctuation, paragraph breaks, or every detected keyword. Each group must state:

- the viewer question being answered;
- one short takeaway the viewer should retain;
- timed evidence from the actual speech;
- ordered beats such as `input`, `support`, `relation`, `warning`, `result`, or `cta`;
- when the complete group exits.

Keep card copy shorter than captions. Captions record what was said; logic beats record what should remain visible.

## Accumulation Contract

Inside one logic group:

1. Establish the input or claim.
2. Add supporting items or the relationship only when the speech reaches them.
3. Reveal the result last.
4. Keep earlier beats visible only when they help the viewer understand the current relationship.
5. Exit the complete group after its conclusion, before an unrelated group begins.

Do not clear every element after every sentence. Do not leave stale elements across unrelated groups. Evidence screenshots and demos may replace explanatory beats instead of stacking beneath them.

## Motion Handoff

Every `MOTION_PLAN.json` node derived from a ready logic file should record `logic_group_id` and `logic_beat_id`. One logic beat may intentionally have no motion when a caption or evidence asset already communicates it.

Validate before design approval:

```bash
python3 tools/content_logic_check.py <project_dir>/CONTENT_LOGIC.json
```

If timing precision is only cue-level, use cue boundaries or ask for an exact spoken-sentence anchor rather than inventing a keyword timestamp.

## Approval Boundary

For a first project, a new style, or a reasoning-heavy video, show the logic-group summary before building motion. The user may correct the takeaway, grouping, or accumulation order without paying the cost of rebuilding animation.
