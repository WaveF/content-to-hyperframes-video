# Content to HyperFrames Video

将任意内容（网页、文档、口述文本）生成为带旁白、配乐和配图的演示视频，基于 [HyperFrames](https://hyperframes.dev) 构建。

## 工作流程

1. **Phase 0** — 引导式参数补全（内容来源、风格、时长、配音等）
2. **Phase 1** — 内容获取（网页抓取 / 文档提取 / 文本整理）
3. **Phase 2** — 脚本设计（7 场景模板 + 领域适配）
4. **Phase 3** — 图片生成（本地或远程生图）
5. **Phase 4** — HTML 写作（GSAP 动效 + AI 字幕）
6. **Phase 5** — 验证（`npm run check`）
7. **Phase 6** — 渲染（`npm run render`）

## 本地图片生成

默认使用 **z-image-turbo-4bit** 模型（通过 [mlxstudio](https://github.com/jjang-ai/mlxstudio) 本地部署），端点位于 `http://localhost:8080`。

### 启动服务

```bash
# 克隆并启动 mlxstudio
git clone https://github.com/jjang-ai/mlxstudio
cd mlxstudio
pip install -r requirements.txt
python main.py --model z-image-turbo-4bit
```

### 文生图

```bash
curl http://localhost:8080/v1/images/generations \
  -H "Content-Type: application/json" \
  -d '{
    "model": "z-image-turbo",
    "prompt": "modern conference room, clean minimalist, blue ambient light",
    "negative_prompt": "blurry, watermark, text",
    "steps": 9,
    "width": 768,
    "height": 512,
    "n": 1
  }'
```

### 用法建议

- Prompt 使用英文，质量更稳定
- 结尾追加 `no text, no labels, no people`
- 推荐尺寸：768×512（横版封面）、512×512（方形配图）
- 图片仅做装饰/背景用，不要依赖 AI 生成文字

### 回退方案

当本地服务不可用时，自动依次尝试：
1. **framefly relay**（远程，需 `FRAMEFLY_API_KEY`，配置于 `.env`）
2. **纯 CSS 视觉设计**（玻璃质感、渐变色块，无需外部服务）
