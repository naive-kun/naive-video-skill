# Talking Head Video Pipeline Skill

An open, reusable Codex skill for turning talking-head videos into captioned, motion-packaged final videos.

It covers:

- Word-level transcription
- Editable `script-aligned.srt`
- Editable `caption-table.csv`
- Cached transcript JSON
- Style onboarding for different brands/colors
- HTML + GSAP motion graphics preview
- Final export while preserving source timing/audio

## Install

Copy or clone this folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R talking-head-video-pipeline ~/.codex/skills/
```

Then start a new Codex session and ask:

```text
Use $talking-head-video-pipeline to process this talking-head video.
```

## Quick Start

1. Put your source video somewhere local.
2. Start a new Codex session.
3. Attach or paste the video path.
4. Ask:

```text
Use $talking-head-video-pipeline to generate captions first, then ask me for a visual style and build a preview.
```

If you already have captions:

```text
Use $talking-head-video-pipeline with this video and my existing SRT. Build a preview before final export.
```

See [examples/prompts.md](examples/prompts.md) for more prompts.

## Privacy

This public version intentionally contains no personal paths, private account names, API keys, or creator-specific brand rules.

Before publishing your fork, run:

```bash
bash scripts/doctor.sh --privacy-scan .
```

## Requirements

The skill assumes the agent can access suitable local tools, depending on the task:

- `ffmpeg` / `ffprobe`
- A transcription workflow or API available in the user's environment
- A video composition renderer such as HyperFrames, Remotion, or equivalent HTML/GSAP capture tooling
- Node.js if using HyperFrames or another browser renderer
- A browser runtime available to the renderer

Check the current machine:

```bash
bash scripts/doctor.sh
```

This skill does not bundle a transcription API key or proprietary model. Users must provide their own transcription setup, or give the agent an existing transcript/SRT/CSV.

Common install hints:

```bash
# macOS with Homebrew
brew install ffmpeg node

# HyperFrames on demand
npx --yes hyperframes --help
```

## Customizing Style

If no style is provided, the skill asks for:

- Accent color
- Caption style
- Card style
- Output aspect ratio
- Safe zones

The chosen style should be written to a project-local `DESIGN.md`.

## Expected Outputs

Caption phase:

```text
<video_dir>/edit/script-aligned.srt
<video_dir>/edit/caption-table.csv
<video_dir>/edit/transcripts/<video_name>.json
```

Preview/final phase:

```text
<video_dir>/final/
```

Exact paths can be changed per project.

## Repository Layout

```text
talking-head-video-pipeline/
├── SKILL.md
├── README.md
├── agents/openai.yaml
├── examples/prompts.md
├── references/
│   ├── caption-workflow.md
│   ├── export-recipes.md
│   └── style-onboarding.md
├── scripts/doctor.sh
├── LICENSE
└── .gitignore
```

## What This Skill Does Not Do

- It does not include your private brand style.
- It does not include sample source videos.
- It does not include API keys.
- It does not guarantee a specific renderer is installed.
- It does not edit source media unless the user asks for cuts.

## Publishing To GitHub

From the folder that contains this skill:

```bash
git init
git add .
git commit -m "Initial talking-head video pipeline skill"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

Before pushing:

```bash
bash scripts/doctor.sh --privacy-scan .
```
