# Example Prompts

## Full Pipeline

```text
Use $talking-head-video-pipeline to process this talking-head video:
<path-to-video>

Generate caption timing first, ask me for visual style, build a preview, then wait for my approval before final export.
```

## Captions Only

```text
Use $talking-head-video-pipeline to generate only caption files for this video:
<path-to-video>

Do not modify the source video. Output SRT, CSV, and transcript JSON.
```

## Use Existing Script As Correction Guide

```text
Use $talking-head-video-pipeline to transcribe this video:
<path-to-video>

Use this script as a correction guide, but prefer what I actually said in the video if they differ:
<paste script>
```

## Existing Captions To Styled Preview

```text
Use $talking-head-video-pipeline with:
- video: <path-to-video>
- srt: <path-to-script-aligned.srt>
- csv: <path-to-caption-table.csv>

Ask me for card and subtitle style, then build a preview.
```

## Direct Final Export

```text
Use $talking-head-video-pipeline to build the final video directly.
Use my existing captions and this style: dark tech panels, cyan accent, clean lower-third subtitles.
Do not extract visual QA frames; only confirm file parameters.
```

## Style Customization

```text
Use $talking-head-video-pipeline.
Brand color: #55D83F.
Cards: frosted white tool cards.
Subtitles: bold brush subtitles with green keyword highlights.
Never cover my face or screenshots.
```
