# Self-Iteration Protocol

Improve from explicit feedback without turning one user's private preferences into public defaults.

## Eligible Feedback

Record feedback only when the user clearly confirms a preference, for example:

- "Use this subtitle style from now on."
- "Never use rectangular face PiP for my videos."
- "This card is correct; keep it."
- "Do not interrupt a render just because it is slow."

Do not learn from silence, a single preview with no comment, or your own guess.

## Classification

Classify each lesson:

- `project`: only this video or campaign.
- `profile`: future projects for this user.
- `product`: generic reliability or usability improvement with all private context removed.

If scope is ambiguous, use `project`.

## Record Format

Append to the user's `VIDEO_LESSONS.md`:

```md
## YYYY-MM-DD - Short lesson

- Scope: project | profile | product-candidate
- User feedback: "short exact or faithful paraphrase"
- Confirmed rule: one testable sentence
- Affected stage: captions | design | preview | render | QA
- Supersedes: none | prior lesson heading
```

## Promotion Rules

A lesson may become a reusable public rule only when:

1. It contains no identity, private path, brand, customer, or media detail.
2. It solves a general failure mode rather than a taste preference.
3. It has been observed in at least two independent projects or is a hard correctness issue.
4. It is expressed as a testable invariant or quality gate.
5. The maintainer reviews it before publication.

Never automatically push lessons to GitHub.

## Private Cross-Project Profile

Project lessons stay in `VIDEO_LESSONS.md`. When the user explicitly wants a rule to apply across future projects, store a sanitized version in a private local profile:

```bash
python3 tools/profile.py init
python3 tools/profile.py add-rule --stage preview --rule "Use circular speaker PiP during full-screen demos"
```

Rules receive a stable ID and remain active until explicitly replaced or deactivated:

```bash
python3 tools/profile.py add-rule \
  --stage preview \
  --rule "Keep speaker PiP away from evidence text" \
  --supersedes <old-rule-id>
python3 tools/profile.py deactivate-rule --id <rule-id>
```

The default profile path is `~/.naive-video/profiles/default.json`. It must contain only reusable style values and testable rules, never source paths, media names, customer details, transcript text, or screenshots.

On initialization, `tools/bootstrap.py` loads this default profile automatically and imports its active rules into the project's `VIDEO_LESSONS.md`. Use `--profile none` for a project that must ignore it.

After final delivery, use `naive-video-retro` and `VIDEO_RETRO.md` to distinguish reproducible failures from one-off taste feedback before promoting rules.

## Conflict Rules

- New explicit feedback may supersede an older profile rule by ID.
- Keep only the active rule in `DESIGN.md`.
- Keep the supersession note in `VIDEO_LESSONS.md` for project traceability.
- Never silently merge contradictory preferences.
