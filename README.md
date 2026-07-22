# Naive Video Skill

给 Codex 使用的开源口播视频成片导师工作流：原片可以先走可选粗剪，也可以从现成粗剪或字幕轴开始，再完成素材插入、风格选择、HyperFrames + GSAP 预览和最终成片。

它不只是一份提示词。它包含首次初始化、可选 `video-use` 粗剪、阶段路由、项目状态、体检、迁移、质量闸门和显式反馈学习，目标是像导师一样一次问一个问题，让完全没有剪辑基础的人也能一步步拿到可播放成片。

## 三步开始

### 1. 下载并安装

```bash
git clone https://github.com/naive-kun/naive-video-skill.git
cd naive-video-skill
bash install.sh --codex
```

安装后重启 Codex，或新建一个任务。

### WorkBuddy 用户

新版本整个仓库只暴露一个 `SKILL.md`，所以 WorkBuddy 新安装时只应出现一个技能：

```text
talking-head-video-pipeline
```

初始化、粗剪、字幕、设计、预览和导出都是这个技能内部的工作流，不会再显示成十几个独立开关。如果旧版已经出现多个 `naive-video-*` 技能，请在 WorkBuddy 里停用或卸载这些旧条目，只保留 `talking-head-video-pipeline`；更新后的仓库不会再次创建它们。

### 2. 在素材目录打开 Codex

把原视频放在任意本地目录，然后在该目录打开 Codex。你不需要先创建工程。

### 3. 只说这一句

```text
用 $talking-head-video-pipeline 初始化视频项目，这是我的口播视频：<视频路径>
```

Skill 会检查环境、读取视频参数、询问最少量的风格问题，并告诉你下一句该说什么。你可以什么都不准备直接用默认风格，也可以补一张喜欢的截图，让 Skill 参考它的配色、层级、卡片和构图。

## 新手会经历什么

```text
初始化
  -> 可选粗剪（原片才需要）
  -> 字幕轴
  -> 截图 / 录屏插入方式
  -> 风格与插入时间表
  -> 官方预览链接
  -> 你确认
  -> 最终成片
  -> 可选复盘与长期规则
```

默认不改原视频、不改变主音频时钟；只有你明确同意粗剪策略后，才会把新生成的粗剪版作为后续工作时钟。它也不会用低清代理冒充最终成片，或让截图被字幕和卡片盖住。

## 原片也能开始：可选 Video Use 粗剪

如果你拿来的是多次重拍、带口误和长停顿的原片，Skill 会先问：`这段视频已经粗剪好了吗？`

- 已经粗剪好：直接进入字幕和设计，不会拿一堆转写选项打断你。
- 还没粗剪：可选调用独立的 [`video-use`](https://github.com/browser-use/video-use) Skill，先盘点素材、提出保留/删除策略，得到你确认后再生成一个不覆盖原片的粗剪版。
- 没安装 `video-use`：会告诉你它是可选能力，并在你同意后再教你安装；不会偷偷装依赖。

需要靠转写找口误和剪切点时，会说明两条路，但不强制选择：

- 云端词级转写：精准粗剪的推荐路线，尤其适合口误、重复和多 take；通常需要自己的 API Key，并可能产生费用。
- 本地词级转写：可离线、可避免云端转写费，但速度、机器要求、口头语保留和时间戳稳定性取决于模型与设备。

已有 SRT、CSV 或词级 JSON 会优先复用，不会重复花钱转写。原片始终保留；确认后的粗剪只会作为后续字幕、动效和成片的工作视频。

## 截图、录屏和产品图怎么插

在设计前，Skill 会问有没有需要展示的截图、录屏、产品图、图表或演示视频，然后让你选择：

- `semantic`：你只给素材，由 Skill 根据字幕语义决定飞入、停留和飞出时间，适合不熟悉时间轴的新手。
- `exact`：你指定第几秒，或者指定“说到哪句话时出现”；这种方式更精准。
- `hybrid`：重要素材由你定，其余交给 Skill。

如果你直接说“你帮我定”，就走语义插入；如果你给了秒数或原话，就按精准锚点执行。所有素材都会在 `EDIT_PLAN.md` 里记录原始要求和换算后的时间。

## 常用说法

```text
初始化视频项目，这是主视频：<path>
这还是原片，先帮我删掉口误、重复和明显停顿
只抽字幕轴，不动视频
用现有 SRT 做动效预览
这些截图你按字幕语义帮我安排飞入飞出：<paths>
说到“这里就是最终效果”时插入 <image-path>，停留 2 秒
参考这张截图设计视频风格：<image-path>
根据字幕语义自动匹配 GSAP 动效，动效密度 balanced
进度到哪了
体检这个视频项目
这个风格以后都这样，记住
复盘这条成片，把确认的问题变成下次的检查项
预览没问题，出最终成片
```

公开安装只会出现一个根 Skill。初始化、粗剪、字幕、设计、预览、导出等步骤是它内部按需读取的工作流，不会在 WorkBuddy 里展开成一排独立技能。完整示例见 [examples/prompts.md](examples/prompts.md)。

## 安装选项

```bash
bash install.sh --codex          # 默认：符号链接，更新仓库后立即生效
bash install.sh --codex --copy   # 冻结复制，更新后需重新安装
bash install.sh --claude         # 安装到 Claude Code
bash install.sh --all            # 两边都安装
bash install.sh --codex --force  # 无交互升级，但仍会先备份旧安装
```

卸载：

```bash
bash uninstall.sh --codex
```

安装器不会复制你的素材，也不会写入项目目录，也不会批量清除已有文件：

- 首次安装只创建一个根 Skill。
- 升级时，旧安装先移动到 `~/.naive-video-skill/backups/<客户端>/<时间戳>/`。
- 旧版 `naive-video-*` 多入口会移动到同一备份的 `legacy/` 目录。
- 安装失败时会恢复先前版本；失败副本会保留在 `~/.naive-video-skill/failed/` 供检查。
- 卸载不是永久清除，而是移动到 `~/.naive-video-skill/uninstalled/`，可以恢复。

这些目录位于 Codex、Claude Code 和 WorkBuddy 的技能发现目录之外，因此备份中的旧 `SKILL.md` 不会再次显示成技能卡片。

安装器本身不会创建 `/tmp/naive-video-skill` 或 `_audit_naive_video` 之类的审计副本；这类目录通常来自外部安装器或安全审计。如果用户取消了清理，它们只是额外的仓库副本，可以先保留，不影响 Skill 使用。

真正开始任务时，内部初始化工作流才会在你的视频项目中创建状态和输出目录。

## 环境体检

```bash
bash scripts/doctor.sh
```

至少需要：

- `ffmpeg` / `ffprobe`
- `python3`
- `node` / `npm` / `npx`（使用 HyperFrames 时）

macOS 常用安装：

```bash
brew install ffmpeg node python
```

HyperFrames 可按需运行：

```bash
npx --yes hyperframes --help
```

转写能力不绑定某一个收费 API。Skill 会优先复用已有 SRT/CSV/词级 JSON。只有原片需要粗剪或确实需要重新转写时，才会说明云端词级转写与本地词级转写的差别：精准粗剪优先推荐云端词级方案并明确费用可能性，本地方案保持可选。都没有时会明确告诉你缺什么，而不是假装已经完成。

## 四种风格起点

- `clean`: 白色轻卡片，适合教程和专业复盘。
- `dark`: 深色高对比，适合技术和产品演示。
- `sticker`: 贴纸式动效，适合轻松口播。
- `minimal`: 只保留字幕和少量重点提示。

颜色、字幕、卡片、动效密度和安全区域都写入项目自己的 `DESIGN.md`。公开仓库不包含作者个人品牌规则。

## 截图参考风格

第一次用时可以直接说：

```text
参考这张截图设计视频风格：<图片路径>
按它的视觉语言做，但不要复制品牌和内容。参考强度 medium。
```

- `low`: 只参考配色和气质。
- `medium`: 还参考层级、卡片、间距和构图，适合大多数新手。
- `high`: 尽量贴近视觉语言，但仍不会复制 Logo、水印、人物、原文或完整品牌 UI。

提取结果写入当前视频项目的 `STYLE_REFERENCE.md`。静态截图不能证明原视频怎么运动，因此由截图推断的动效会明确标记为 `inferred`，并通过官方预览让你确认。

## GSAP 语义动效

Skill 会把字幕里的数字、列举、对比、警告、流程、因果、任务转移、确认、结果和提问映射到本地 GSAP 配方，而不是给整条视频反复套同一种角落卡片。

动效密度可选：

- `restrained`: 克制，优先证据可读性。
- `balanced`: 默认，语义节点和留白兼顾。
- `energetic`: 更丰富，但仍避开人脸、字幕和截图；15 秒展示建议至少 6 个独立语义节点，长视频按时长缓慢增加。

详细计划写入项目的 `MOTION_PLAN.json`，预览前由离线检查器验证配方、时间、字幕证据和安全区域。默认只使用项目已有 GSAP；插件缺失时自动走 core fallback，不会让整个预览失败。

如果项目使用 npm，推荐安装官方包：

```bash
npm install gsap
```

如果已经下载了官方浏览器分发包，也可以只把当前项目需要的 `gsap.min.js` 和插件复制到项目自己的 runtime 目录。先检查版本和许可证头：

```bash
python3 tools/gsap_check.py <gsap-directory>
```

视频常用的可选插件是 SplitText、Flip、ScrambleText、DrawSVG、MorphSVG 和 MotionPath；其中 ScrambleText 只用于很短的系统状态，DrawSVG 不能拿来做廉价手绘箭头。GSDevTools 只用于开发。ScrollTrigger、ScrollSmoother、Observer、Draggable 等网页滚动/交互插件通常不进入固定时间轴视频，视频仍由一个暂停、可 seek 的 GSAP timeline 驱动。

本仓库不会直接打包个人下载目录里的 GSAP 文件。GSAP 文件保留自己的版权和标准许可证，MIT 只覆盖本仓库自行编写的内容。

## 视觉质量与通用组件

公开版不会内置作者个人的颜色、字体或固定卡片系统。每个项目必须在 `DESIGN.md` 里明确字体、真实字重、字幕最大行数、换行策略、文本基线、组件类型和最长标签适配，再通过离线检查：

```bash
python3 tools/design_check.py <project-dir>/DESIGN.md
```

通用组件包括：

- `structured card`：解释、步骤和对比。
- `glass notification`：短状态、提醒、确认和 CTA。
- `focus-frame`：在稳定容器内切换关键词焦点。
- `seekable-type`：由视频时间轴驱动的短文本输入效果。
- `split-reveal`：卡片标题、步骤和警告的逐词或克制逐字入场。

这些组件只规定信息角色和质量门槛，不规定某个创作者的配色。GSAP 负责运动，字体、间距、对齐、表面和层级仍由设计契约负责。

网页组件里的 `setInterval`、随机打字速度、`IntersectionObserver` 和 `ScrollTrigger` 不会直接搬进视频。Skill 会把它们改成暂停、可 seek、任意时间点都能稳定复现的 GSAP timeline。

默认拒绝未经要求的手绘感箭头、粗糙框线、细体大字、倾斜正文、错位基线和无规则的单双行字幕切换。

## 项目状态与恢复

初始化后，项目中会出现：

```text
.naive-video-state.json
EDIT_PLAN.md
DESIGN.md
STYLE_REFERENCE.md   # 使用参考图时创建
MOTION_PLAN.json     # 使用语义动效时创建
VIDEO_LESSONS.md
VIDEO_RETRO.md
edit/
  rough-cut.mp4          # 需要粗剪时才有
  rough-cut-edl.json     # 可选剪切决策记录
preview/
final/
qa/
```

状态文件让新任务知道已经做到字幕、预览还是导出阶段。渲染中断时，Skill 会先检查进度和产物，不会无故推倒重来。

## 自我迭代

当你明确说“这个风格以后都这样”或“以后不要再这样”，Skill 才会把规则写进项目的 `VIDEO_LESSONS.md`。成片交付后，内部复盘工作流会把成功项、失败根因和预防检查写入 `VIDEO_RETRO.md`，但不会擅自把推测变成长期偏好。

需要跨视频复用时，确认后的脱敏规则会保存到本机私有配置：

```text
~/.naive-video/profiles/default.json
```

新项目会检测并复用它；你也可以要求某个项目忽略旧风格。

长期规则带有稳定 ID、启用状态和确认时间；规则冲突时可以显式替代或停用旧规则。新项目会把当前启用规则导入自己的 `VIDEO_LESSONS.md`，所以“记住”会真正影响下一条视频。

反馈分三层：

- 当前视频专用
- 当前用户长期风格
- 可脱敏的通用产品改进

个人路径、品牌名、截图、客户信息和素材内容不会自动回流到公开仓库。

## 隐私与发布检查

```bash
bash scripts/doctor.sh --privacy-scan .
python3 tools/validate_skill.py .
bash tests/smoke.sh
```

CI 会执行同样的无密钥检查。不要提交 `.env`、真实客户素材、转写缓存、渲染文件或本机绝对路径。

## 仓库结构

```text
naive-video-skill/
├── SKILL.md                 # 总路由与硬规则
├── references/              # 状态、质量、视觉规则，以及 12 个内部阶段工作流
├── templates/               # 项目初始化模板
├── migrations/              # 状态 schema 迁移
├── tools/                   # 无第三方依赖的检查与初始化工具
├── scripts/                 # 安装、体检入口
├── tests/                   # 干净环境冒烟测试
└── agents/openai.yaml
```

仓库中只能存在根目录这一个 `SKILL.md`。CI 会检查这个约束，避免 WorkBuddy 等递归扫描器把内部工作流误装成多个技能。

## English Summary

Naive Video Skill is a beginner-first, stateful Codex workflow for talking-head video production. It routes optional non-destructive rough cutting, captions, asset placement, motion preview, export, revision, diagnosis, status, explicit-feedback learning, and state migration while preserving originals, evidence readability, and privacy.

## License

MIT
