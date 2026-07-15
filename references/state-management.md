# State Management

The project-local `.naive-video-state.json` lets a later task resume safely.

## Schema

Current schema: `1.0`.

Required top-level fields:

```json
{
  "schema_version": "1.0",
  "skill_version": "2.0.0",
  "project_name": "example-video",
  "stage": "initialized",
  "main_video": "<project-local-or-user-provided-path>",
  "master_audio": "main_video",
  "preview_required": true,
  "approval": {
    "status": "pending",
    "approved_at": null,
    "preview_url": null
  },
  "style_profile": {},
  "profile": {
    "name": null,
    "path": null,
    "loaded": false,
    "rules_loaded": 0
  },
  "outputs": {},
  "last_error": null,
  "updated_at": "<ISO-8601>"
}
```

## Write Rules

- Update state atomically: write a temporary file, validate JSON, then replace.
- Never store API keys, transcript bodies, customer names, screenshot contents, or render logs in state.
- Keep user-supplied absolute paths only in the user's private project state. They must never be copied into this public skill repository.
- Preserve unknown fields during migration.
- Set `last_error` only for an unresolved blocker; clear it after the relevant gate passes.
- Use stage values from the root `SKILL.md` only.

## Approval Rules

- `pending`: no approved preview.
- `approved`: the linked preview version is approved.
- `skipped_by_user`: the user explicitly requested direct export.
- Any visible revision returns approval to `pending`.

`tools/state.py approval approved` advances `preview_ready` to `approved`. Recording `pending` after a visible revision returns downstream stages to `preview_ready`.

## Resume Rules

1. Read state.
2. Check that declared outputs still exist.
3. Run the gate for the declared stage.
4. If the gate fails, move only to the last verified stage.
5. Continue from the next incomplete stage.

Use `python3 tools/video_doctor.py --project <project_dir>` for a read-only consistency check.

Use `tools/state.py` for atomic updates instead of ad-hoc JSON string edits:

```bash
python3 tools/state.py --project <project_dir> show
python3 tools/state.py --project <project_dir> stage captions_ready
python3 tools/state.py --project <project_dir> approval approved --url <preview_url>
python3 tools/state.py --project <project_dir> output final <final_video>
```

Stage regression requires `--force` and should be used only for a revision or a failed downstream gate.

Post-delivery retrospectives do not add a production stage. Record `VIDEO_RETRO.md` as `outputs.retro` while leaving a completed project at `final_ready`.
