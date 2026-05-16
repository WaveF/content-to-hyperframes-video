---
name: content-to-hyperframes-video
description: |
  用 HyperFrames 制作演示视频。无论用户输入多笼统（"用hyperframes做视频"）或多具体（指定URL/风格/时长），
  都会先执行引导式参数补全（Phase 0），再进入多阶段生产流程。
  适用所有领域：企业方案、电商产品、教育课程、资讯报道、路演PPT等。
  单一目录自包含，复制即用，无需外部技能依赖。
version: 2.2.0
metadata:
  hermes:
    tags: [hyperframes, video, presentation, content-to-video, image-generation, workflow, portable]
  portable: true
  self_contained: true
---

# 任意内容 → HyperFrames 视频

输入可以是网页、文档、口述、文本 —— 也可以什么都不给，Phase 0 会帮你补全。
输出统一为带旁白+配乐+配图的演示视频。领域无关，方法论通用。

## 触发条件（宽泛匹配）

以下任何说法都应触发本技能：

- "用 HyperFrames 做/制作/生成/创建一个视频"
- "HyperFrames 视频"
- "把这个网站/文档/内容做成视频"
- "基于这些资料生成演示视频"
- "做一个介绍/宣传 XXX 的视频"
- "生成 PPT 风格视频"
- 任何提到 HyperFrames 且有视频制作意图的对话

关键是：**只要用户提到用 HyperFrames 产出视频，就触发。** 具体参数有没有无所谓 —— Phase 0 会主动问。

## 核心原则

**用户说什么就做什么，用户没说的主动问。**
不要因为 prompt 简短就自行脑补全部参数 —— 每个缺失的维度都是决策点，用引导式问答补全。

---

## Phase 0：参数补全（必须先执行）

触发本技能后，**立即**检查以下全部维度是否已明确。任何维度未明确就进入问答。

### 用 clarify() 问的（阻塞性问题，不回答无法继续）

**第一轮 — 内容来源（三选一必答）：**

> 视频基于什么内容制作？
> A. 网页链接（我会抓取内容）
> B. 你口述/粘贴内容
> C. 本地文档/PDF

### 用清单方式呈现的（有默认值，让用户一键确认或逐条修改）

**第二轮 — 全部参数确认清单：**

| 维度 | 默认值 | 说明 |
|---|---|---|
| **内容/分页** | （从prompt推断） | 若不明确，主动问 |
| **主题/产品名** | （从内容推断） | 若不明确，主动问 |
| **领域** | 企业方案 | 企业方案 / 电商产品 / 教育课程 / 资讯报道 / 其他 |
| **时长** | 70s（有旁白） | 短版30-45s / 标准60-70s / 长版90-110s / 自定义 |
| **视频尺寸** | 16:9 (1920×1080) | 16:9 横版 / 9:16 竖版 / 1:1 方形 |
| **风格/色调** | 深蓝科技风 | 深蓝科技 / 品牌色 / 温暖明亮 / 黑金高端 / 新闻红 / **用户自定义描述** |
| **品牌色** | 无 | 如有品牌色/Logo，请提供色值或参考 |
| **动画程度** | 标准动效 | 极简（仅淡入淡出） / 标准（GSAP入场+卡片串行） / 动感（shader过渡+弹性缓动） |
| **配音** | AI自动选择音色并生成 | 让用户选择音色后AI自动生成 / 用户提供现成的配音文件 |
| **接受配音导致时长增加** | 是 | 旁白会扩展视频时长 / 改变语速以适应视频时长 |
| **背景音乐** | 不需要 | 需要无版权BGM / 用户提供 / 不需要 |
| **AI 字幕** | 需要 | 需要（叠加字幕轨道，见 `references/subtitle-system.md`） / 不需要 |
| **配图来源** | 本地AI生图服务（需检测,检测不可用就跟用户沟通） | 网络无版权素材站 / 用户提供已有图片 / 纯CSS无图片 |
| **图片服务器地址** | z-image-turbo | 见 `references/z-image-turbo-api.md` |
| **输出目录** | 当前工作目录 | 默认当前目录 / 指定路径 |
| **其他要求** | 无 | 任何特殊需求（特定字体、必须含某元素、禁止某元素等） |

### 问答流程

1. 先检查用户 prompt 中已经提供了哪些信息，标记为「已明确」
2. 对未明确的阻塞项（内容来源、主题），用 `clarify()` 问
3. 阻塞项明确后，把清单中所有未明确的维度汇总成一条消息发给用户，标注默认值
4. 用户回复「全部默认」则直接进入 Phase 1，否则按修改项执行

---

## 技能结构（单目录自包含）

```
content-to-hyperframes-video/
  SKILL.md                                    ← 主编排（Phase 0 + 6阶段 + 领域适配）
  references/
    scene-design-system.md                     ← 7场景模板 + 设计令牌 + 时序公式
    hyperframes-composition.md                 ← HTML规则 + GSAP模式 + 10条铁律 + 字幕系统
    image-generation.md                        ← 图片生成（z-image-turbo + framefly + CSS回退）
    z-image-turbo-api.md                       ← 本地图像生成服务
    content-extraction.md                      ← 内容获取方法
    subtitle-system.md                         ← AI字幕轨道（JS时序驱动）
  scripts/
    generate.py                                ← FrameFly 图片生成脚本
```

---

## Phase 1：内容获取

见 `references/content-extraction.md`
- 网页：delegate_task + browser 工具抓取结构化内容
- 文档/PDF：ocr-and-documents 技能提取
- 口述/文本：整理为结构化提纲
- 提取关键数据点（数字、功能列表、案例）用于后续场景

## Phase 2：脚本设计

见 `references/scene-design-system.md`
- 7场景通用模板（可调整顺序和数量）
- 设计令牌（CSS变量、颜色、字体）— 按 Phase 0 确定的风格选择
- 场景时序计算公式
- 领域适配指南（电商/教育/资讯/企业各有侧重）

## Phase 3：图片生成

见 `references/image-generation.md`
- 按 Phase 0 确定的配图来源执行
- **回退链**：z-image-turbo → framefly relay → 纯CSS视觉设计（当服务不可用时，沿链向下尝试，无需中断流程向用户报错）
- 如选生成服务且服务器信息未持久化，询问是否保存到 memory
- 建议 2-4 张，做装饰背景

## Phase 4：HTML 写作

见 `references/hyperframes-composition.md`
- 10条硬规则、GSAP 动效模板
- 按 Phase 0 的尺寸/动画程度/配音/字幕设置
- 如用户自定义了视觉风格描述而非预设风格，用 CSS `backdrop-filter` + 渐变 + 光晕模拟玻璃/塑料/科技质感（参考 `references/image-generation.md` 方案C）
- **AI 字幕**：如 Phase 0 确认需要，见 `references/subtitle-system.md` 叠加 JS 时序驱动字幕轨道
- 音频轨道设置、countUp 动画
- 关键坑：visibility 与 clip 冲突

## Phase 5：验证与修复

```bash
cd <项目名> && npm run check
```

## Phase 6：渲染

```bash
npm run render
```

---

## 领域适配速查

| 领域 | 场景调整 | 色调 | 特点 |
|---|---|---|---|
| 企业方案 | 标准7场景 | 深蓝科技风 | 数据+案例+CTA |
| 电商产品 | 封面→痛点→产品展示×2→优势→数据→CTA | 品牌色 | 产品图占比大 |
| 教育课程 | 封面→目标→内容大纲×2→学习效果→CTA | 温暖明亮 | 文字为主 |
| 资讯报道 | 封面→背景→关键信息×2→影响→CTA | 新闻红/黑白 | 快节奏 |
