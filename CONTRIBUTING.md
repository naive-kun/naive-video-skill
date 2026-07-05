# Contributing

Thanks for improving this skill.

## Keep It Generic

Do not add:

- Personal absolute paths
- Private account names
- Private customer names
- Source video filenames from real projects
- API keys or tokens
- Local `.env` content
- Private screenshots or rendered frames

Use placeholders like:

```text
<main_video>
<output_dir>
<work_dir>
<accent_color>
```

## Before Opening A PR

Run:

```bash
bash scripts/doctor.sh --privacy-scan .
```

Check:

- `SKILL.md` frontmatter has only `name` and `description`.
- `agents/openai.yaml` has a short, accurate `default_prompt`.
- README examples do not contain private paths.
- New references are useful across many users, not just one creator.

## Style

- Keep `SKILL.md` concise.
- Put longer explanations in `references/`.
- Prefer reusable workflows over one creator's visual style.
