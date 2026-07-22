# Optional Rough-Cut Integration

Use this branch only when the user has raw takes, repeated lines, filler words, long pauses, multiple clips, or explicitly asks for a rough cut. Do not interrupt an already rough-cut project with transcription choices.

## Beginner Conversation

Ask one question at a time.

1. `这段视频已经粗剪好了吗？`
2. If no, explain the visible result first: `我可以先帮你删掉口误、重复和明显空白，生成一个不覆盖原片的粗剪版。`
3. Ask for strategy confirmation before cutting. Never silently choose what content to remove.
4. Only when transcription is needed, offer the available timing sources in this order:
   - existing SRT, CSV, or word-level transcript JSON;
   - installed `video-use` with hosted word-level transcription;
   - a compatible local word-level ASR adapter;
   - user-provided timing/text when no adapter is available.

## How To Explain Transcription

Use plain language:

- **Hosted word-level transcription — recommended for precise rough cutting.** It is normally the best fit for retakes, filler words, and exact cut boundaries, but the service may charge by usage and requires the user's own API key. The current public `video-use` setup uses ElevenLabs Scribe; always confirm the installed skill because its adapter may evolve.
- **Local word-level transcription — optional.** It can avoid cloud transcription fees and keep audio local, but setup, speed, filler-word retention, and timestamp quality depend on the machine and model.
- **Existing timing files — reuse first.** If usable SRT, CSV, or word-level JSON already exists, do not transcribe again.

Do not frame either cloud or local transcription as mandatory. Do not claim that a sentence-level local transcript is equivalent to word-level timing for precise cuts.

## `video-use` Route

If the `video-use` skill is installed, route the rough-cut task to it and follow its own workflow. If it is not installed:

1. Say that it is an optional companion skill, not a hidden dependency.
2. Point the user to the public project: <https://github.com/browser-use/video-use>.
3. Offer to help install it only after the user asks or approves.
4. Never install packages, request an API key, or upload media without explicit approval.

The rough-cut contract remains:

- inventory sources before editing;
- preserve every original file;
- propose the keep/remove strategy and wait for confirmation;
- cut only at verified word or silence boundaries;
- avoid cutting inside a word;
- pad verified cut edges by roughly 30–200 ms when needed so words are not clipped;
- add 30 ms audio fades at new boundaries to prevent pops;
- cache transcript data;
- provide a reviewable rough cut and edit decision record;
- make the accepted rough cut the `working_video` for captions, design, preview, and export.

## State Handoff

After the user approves the rough cut, record it without changing `main_video`:

```bash
python3 <skill_root>/tools/state.py \
  --project <project_dir> \
  working-video <rough_cut_path>
```

The original `main_video` remains the immutable source. Downstream stages use `working_video` when present and otherwise fall back to `main_video`.

## Exit To Main Pipeline

Return:

- original source path;
- rough-cut path;
- transcription route used and whether it may incur cost;
- strategy approval status;
- unresolved ambiguous cuts;
- next phrase: `粗剪确认，继续做字幕和画面设计。`
