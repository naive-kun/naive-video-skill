# Naive Video Init

Create a resumable project without modifying source media.

Resolve `<skill_root>` by locating the installed `talking-head-video-pipeline/SKILL.md`; do not assume the user's current directory is the skill directory.

## Workflow

1. Resolve `project_dir` and `main_video` from the user's message and attachments.
2. If `.naive-video-state.json` exists, do not reinitialize. Run project doctor and route to status or the requested stage.
3. Run environment checks:

   ```bash
   bash <skill_root>/scripts/doctor.sh
   ```

4. Inspect the source with `ffprobe`. Record duration, resolution, frame rate, codecs, pixel format, and audio stream.
5. When it is unclear whether the source is raw, ask one question: `这段视频已经粗剪好了吗？` If no, read `references/video-use-integration.md` and load `references/workflows/rough-cut.md` before captions. Do not ask about transcription services when the video is already rough-cut.
6. Ask whether the user wants `quick` or `guided` setup only when they did not already request speed or provide a style reference.
7. Run:

   ```bash
   python3 <skill_root>/tools/bootstrap.py \
     --project <project_dir> \
     --video <main_video> \
     --mode <quick-or-guided>
   ```

8. If a private default profile exists, tell the user it was loaded. Use `--profile none` when the user wants a clean project without prior preferences.
9. In guided mode, ask one question at a time using `references/style-onboarding.md`, then update `DESIGN.md` and the state style profile.
10. Read `references/asset-onboarding.md`. Ask whether screenshots, recordings, product images, charts, or demo videos should appear. If yes, record whether placement will be `semantic`, `exact`, or `hybrid`; explain that user-supplied seconds or spoken-sentence anchors are more precise.
11. Add all supplied assets and known anchors to `EDIT_PLAN.md`. Do not load the media into the public skill.
12. Run:

   ```bash
   python3 <skill_root>/tools/video_doctor.py --project <project_dir>
   ```

## Adoption

For an older project with existing files, use `--adopt-existing`. Detect files but do not move or rename them. Set the stage only to the last quality gate that passes.

## Completion

Report:

- project directory
- source duration and resolution
- files created
- missing optional tools
- next phrase: `先帮我粗剪` when raw footage needs it, otherwise `抽字幕轴` or `用现有字幕做预览`
