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

## Raw Footage With Optional Rough Cut

```text
用 $talking-head-video-pipeline 处理这批原片：<paths>
我不会粗剪。请先告诉我可以删哪些口误、重复和明显停顿，等我确认策略后再执行。
如果要转写，请说明云端词级转写的费用可能性和本地词级转写的差别，不要替我强制选择。
```

## Semantic Asset Placement

```text
这些截图和录屏需要放进视频：<paths>
我不会看时间轴，请根据字幕语义决定每个素材的飞入、停留和飞出，并把依据写进 EDIT_PLAN.md。
```

## Exact Asset Placement

```text
说到“这里就是最终效果”时插入 <image-path>，停留 2 秒后飞出。
72.16 秒左右同时插入 <image-a> 和 <image-b>。
请用字幕轴解析准确时间；如果原话重复出现，先问我是哪一次。
```

## Hybrid Asset Placement

```text
关键演示视频固定在 28.09 秒全屏播放，其他截图你按口播语义安排。
告诉我：我指定的时间会更精准，自动安排的部分会先在官方预览里让我确认。
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

## Screenshot Style Reference

```text
参考这张截图设计视频风格：<image-path>
按这张图的视觉语言做，但不要复制其中的品牌和内容。
我是第一次用，请使用推荐的 medium 强度，并先告诉我你提取了哪些设计规则。
```

## Semantic GSAP Motion

```text
根据现有字幕自动匹配 GSAP 语义动效。
数字、列举、对比、警告、流程、确认和结果要用不同的本地动效配方。
动效密度 energetic，但不能遮挡人脸、字幕或截图；先检查 MOTION_PLAN.json，再做官方预览。
```

## Offline GSAP Package

```text
我已经下载了官方 GSAP 文件夹：<gsap-directory>
先用 gsap_check.py 检查版本和可用插件，不要把整个下载目录复制进公开 Skill。
这个视频只挑真正有语义价值的插件，并给每个插件动效准备 core fallback。
```

## Brand-Neutral Visual Quality

```text
先为这个项目写清字体、真实字重、字幕最多一行还是两行、换行规则和组件类型。
正文和按钮文字必须水平对齐，不要细体大字、手绘感箭头或歪斜文字。
需要状态提醒时可以用玻璃通知；Focus、Type 和 Split 动效必须由可 seek 的 GSAP 时间轴驱动。
先运行 design_check.py，再做官方预览。
```

## Combined Beginner Setup

```text
用 $talking-head-video-pipeline 初始化这个口播项目：<video-path>
我没有剪辑经验。请提醒我可以补一张喜欢的参考截图；如果我不提供，就用安全默认风格。
设计完成后按字幕语义匹配 balanced GSAP 动效，先给官方预览，确认后再导出。
```

## Resume

```text
用 $talking-head-video-pipeline 看一下这个视频项目做到哪一步，继续未完成的部分。
```

## Diagnose

```text
用 $talking-head-video-pipeline 只做体检，不要改文件，也不要重跑渲染。
```

## Explicit Learning

```text
这个圆形人物画中画是正确的。以后我的演示视频都用圆形，不要用矩形。
请用 $talking-head-video-pipeline 记成长期风格规则。
```

## Direct Export

```text
我明确跳过预览，直接导出最终成片。
保留原始主音频，只做文件参数检查，不抽帧。
```

## Delivery Retrospective

```text
用 $talking-head-video-pipeline 复盘这条成片。
先区分具体故障、环境问题和我的长期风格偏好；只有我确认后，才把规则带到下一条视频。
```
