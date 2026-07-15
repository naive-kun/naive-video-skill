# Export Recipes

These are patterns, not mandatory commands. Adapt paths, codecs, and bitrates to the user's machine and target platform.

## Inspect Source

```bash
ffprobe -v error \
  -show_entries format=duration,size \
  -show_entries stream=index,codec_type,codec_name,width,height,r_frame_rate,duration,pix_fmt \
  -of json "<main_video>"
```

## Browser Preview Proxy

Use when the source video is HEVC, high bitrate, or stutters in browser preview.

```bash
ffmpeg -hide_banner -y \
  -i "<main_video>" \
  -vf "scale=1920:1080,fps=30,format=yuv420p" \
  -c:v libx264 -preset veryfast -crf 23 \
  -c:a aac -b:a 128k \
  "<work_dir>/assets/main-preview.mp4"
```

## Final From Full-Resolution Render And Original Audio

Use only when the rendered video is already at the requested final resolution. Do not upscale a low-resolution preview and call it a true high-resolution final.

```bash
ffmpeg -hide_banner -y \
  -i "<preview_render.mp4>" \
  -i "<main_video>" \
  -map 0:v:0 -map 1:a:0 \
  -vf "fps=30,format=yuv420p" \
  -c:v h264_videotoolbox -b:v 42000k -maxrate 52000k -bufsize 84000k \
  -c:a aac -b:a 192k -shortest -movflags +faststart \
  "<output_4k.mp4>"
```

## Stable Overlay Pipeline

Prefer this when the source is already high-quality 4K, HEVC/Main10, or the user explicitly wants the original video preserved as the base.

1. Render motion graphics as transparent overlay frames or a transparent MOV/WebM if supported.
2. Use the original source video as input 0.
3. Overlay graphics on top.
4. Map original audio.

Conceptual filter:

```text
[main_video][overlay_rgba] overlay=0:0:format=auto
```

When the source is 4K HEVC/Main10, this is the preferred path: render only transparent graphics in the motion renderer, composite over the original source with ffmpeg, and map the original main audio.

## Render Log Rule

Do not do this for long renders:

```bash
render-command | head -c 4000
```

That can terminate the render early. Instead:

```bash
render-command > render.log 2>&1
tail -n 40 render.log
```

If a render is progressing, keep waiting. Do not switch methods merely because the frame count advances slowly.
