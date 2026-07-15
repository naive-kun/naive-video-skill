# Example Prompts

## First Project

```text
用 $talking-head-video-pipeline 初始化视频项目。
主视频：<path>
我是第一次用，你帮我按默认流程走。
```

## Full Pipeline With Assets

```text
用 $talking-head-video-pipeline 制作成片。
主视频：<path>
字幕：<srt-path>

12.5 秒插入截图 <image-path>，停留 2 秒。
35 秒全屏播放 <demo-path>，素材静音，人物放左下角画中画。

先给我官方预览，确认后再导出。
```

## Captions Only

```text
只抽字幕轴，不动原视频。
视频：<path>
输出 SRT、CSV 和 transcript JSON。
```

## Existing Captions

```text
我已经有字幕轴，不需要重新转写。
视频：<path>
SRT：<path>
CSV：<path>
请进入风格设计和预览阶段。
```

## Fast Style Setup

```text
风格你帮我定，干净专业、蓝色强调、动效克制。
截图正文和人脸绝对不能挡。
```

## Custom Style

```text
卡片用深色高对比，强调色 #FF4D4F。
字幕用粗白字，关键词用强调色。
动效 energetic，但展示截图时收敛。
```

## Resume

```text
用 $naive-video-status 看一下这个视频项目做到哪一步，继续未完成的部分。
```

## Diagnose

```text
用 $naive-video-doctor 只做体检，不要删文件，也不要重跑渲染。
```

## Explicit Learning

```text
这个圆形人物画中画是正确的。以后我的演示视频都用圆形，不要用矩形。
请用 $naive-video-learn 记成长期风格规则。
```

## Direct Export

```text
我明确跳过预览，直接导出最终成片。
保留原始主音频，只做文件参数检查，不抽帧。
```

## Delivery Retrospective

```text
用 $naive-video-retro 复盘这条成片。
先区分具体故障、环境问题和我的长期风格偏好；只有我确认后，才把规则带到下一条视频。
```
