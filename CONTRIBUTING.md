# Contributing

Contributions should make a stranger's first successful run shorter, safer, or more reliable.

## Before Editing

Classify the change:

- routing or invariant -> root `SKILL.md`
- one stage -> matching child skill
- detailed protocol -> `references/`
- deterministic repeated action -> `tools/`
- user-project scaffold -> `templates/`
- state change -> `migrations/`

Do not duplicate the same rule across many child skills. Put shared correctness rules in a reference and link to it.

## Privacy

Never add:

- personal absolute paths
- account or customer names
- real project filenames
- screenshots, transcripts, or rendered frames from private work
- API keys, tokens, `.env` contents, or login state
- creator-specific brand rules as public defaults

Use placeholders such as `<main_video>`, `<project_dir>`, and `<accent_color>`.

## Self-Iteration Contributions

A user lesson is eligible for the public skill only when it is sanitized, testable, general, and reviewed. Taste preferences remain project-local. Hard correctness failures may be promoted immediately after a reproducible test is added.

Use `VIDEO_RETRO.md` to document evidence. Promotion requires either two independent project observations or one hard correctness failure with a regression test.

## Required Checks

```bash
bash scripts/doctor.sh --privacy-scan .
python3 tools/validate_skill.py .
bash tests/smoke.sh
```

The test path must work without PyYAML or other unlisted Python packages.

## Pull Requests

Explain:

1. The beginner or reliability failure being fixed.
2. Which stage owns the fix.
3. How the change was tested.
4. Whether state schema or migration behavior changed.
