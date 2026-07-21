# Naive Video Skill

给 Codex 使用的开源口播视频成片工作流：从字幕轴、风格选择、HyperFrames + GSAP 预览，到保留原始音画时钟的最终成片。

它不只是一份提示词。它包含首次初始化、阶段路由、项目状态、体检、迁移、质量闸门和显式反馈学习，目标是让第一次剪视频的人也知道下一步该做什么。

## 三步开始

### 1. 下载并安装

```bash
git clone https://github.com/naive-kun/naive-video-skill.git
cd naive-video-skill
bash install.sh --codex
```

安装后重启 Codex，或新建一个任务。

### 2. 在素材目录打开 Codex

把原视频放在任意本地目录，然后在该目录打开 Codex。你不需要先创建工程。

### 3. 只说这一句

```text
用 $talking-head-video-pipeline 初始化视频项目，这是我的口播视频：<视频路径>
```

Skill 会检查环境、读取视频参数、询问最少量的风格问题，并告诉你下一句该说什么。

## 新手会经历什么

```text
初始化
  -> 字幕轴
  -> 风格与插入时间表
  -> 官方预览链接
  -> 你确认
  -> 最终成片
  -> 可选复盘与长期规则
```

默认不改原视频、不改变主音频时钟、不用低清代理冒充最终成片，也不会让截图被字幕或卡片盖住。

## 常用说法

```text
初始化视频项目，这是主视频：<path>
只抽字幕轴，不动视频
用现有 SRT 做动效预览
进度到哪了
体检这个视频项目
这个风格以后都这样，记住
复盘这条成片，把确认的问题变成下次的检查项
预览没问题，出最终成片
```

根 Skill 会自动路由到专门的子 Skill。完整示例见 [examples/prompts.md](examples/prompts.md)。

## 安装选项

```bash
bash install.sh --codex          # 默认：符号链接，更新仓库后立即生效
bash install.sh --codex --copy   # 冻结复制，更新后需重新安装
bash install.sh --claude         # 安装到 Claude Code
bash install.sh --all            # 两边都安装
```

卸载：

```bash
bash uninstall.sh --codex
```

安装器不会复制你的素材，也不会写入项目目录。真正开始任务时，`naive-video-init` 才会在你的项目中创建状态和输出目录。

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

转写能力不绑定某一个收费 API。Skill 会优先复用已有 SRT/CSV/JSON，其次使用已提供的 `hyperframes transcribe`，再检测本地 Whisper 类工具；都没有时会明确告诉你缺什么，而不是假装已经完成转写。纯音、静音或没有可识别语音的测试素材仍会如实停止。

## 四种风格起点

- `clean`: 白色轻卡片，适合教程和专业复盘。
- `dark`: 深色高对比，适合技术和产品演示。
- `sticker`: 贴纸式动效，适合轻松口播。
- `minimal`: 只保留字幕和少量重点提示。

颜色、字幕、卡片、动效密度和安全区域都写入项目自己的 `DESIGN.md`。公开仓库不包含作者个人品牌规则。

## 项目状态与恢复

初始化后，项目中会出现：

```text
.naive-video-state.json
EDIT_PLAN.md
DESIGN.md
VIDEO_LESSONS.md
VIDEO_RETRO.md
edit/
preview/
final/
qa/
```

状态文件让新任务知道已经做到字幕、预览还是导出阶段。渲染中断时，Skill 会先检查进度和产物，不会无故推倒重来。

## 自我迭代

当你明确说“这个风格以后都这样”或“以后不要再这样”，Skill 才会把规则写进项目的 `VIDEO_LESSONS.md`。成片交付后，`naive-video-retro` 会把成功项、失败根因和预防检查写入 `VIDEO_RETRO.md`，但不会擅自把推测变成长期偏好。

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
├── skills/                  # 11 个阶段子 Skill
├── references/              # 状态、质量、字幕、版式、导出协议
├── templates/               # 项目初始化模板
├── migrations/              # 状态 schema 迁移
├── tools/                   # 无第三方依赖的检查与初始化工具
├── scripts/                 # 安装、体检入口
├── tests/                   # 干净环境冒烟测试
└── agents/openai.yaml
```

## English Summary

Naive Video Skill is a stateful Codex workflow for talking-head video production. It routes initialization, captions, motion preview, export, revision, diagnosis, status, explicit-feedback learning, and state migration while preserving source timing, audio, evidence readability, and privacy.

## License

MIT
