# 图片生成

为 HyperFrames 视频生成配图。图片仅做装饰/背景用，不依赖文字（AI 生图文字不可靠）。

## 方案A：本机 z-image-turbo（推荐，快速）

端点：`http://localhost:8080/v1/images/generations`

特点：秒级出图，质量中等，**绝对不能含文字**（会乱码）。

### curl 调用

```bash
curl -s http://localhost:8080/v1/images/generations \
  -H "Content-Type: application/json" \
  -d '{
    "model":"z-image-turbo",
    "prompt":"modern conference room, clean minimalist, blue ambient light, no text",
    "n":1,
    "size":"768x512"
  }' | python3 -c "
import sys,json,base64
d=json.load(sys.stdin)
open('/tmp/output.png','wb').write(base64.b64decode(d['data'][0]['b64_json']))
print('OK')
"
```

### Prompt 规则

- 英文 prompt（中文 prompt 效果不稳定）
- 结尾加 `no text, no labels, no people`
- 风格词：`clean`, `minimalist`, `professional`, `blue/tech ambient`
- 尺寸建议：768×512（横版封面），512×512（方形配图）

### 常见故障

| 错误 | 原因 | 处理 |
|---|---|---|
| `model_load_timeout` | MLX 模型冷启动 | 等待 60s 重试，或重启 localhost:8080 |
| `KeyError: 'data'` | 返回错误信息 | 检查原始 JSON，可能是模型挂了 |
| curl exit 28 | 服务不可达 | 确认 localhost:8080 在线 |

---

## 方案B：framefly relay gpt-image-2（高质量远程）

端点：`https://relay.framefly.com.cn/v1/images/generations`

特点：质量高，数十秒出图，需要 API Key。

### 脚本方式（推荐）

使用本技能自带的 `scripts/generate.py`：

```bash
python3 scripts/generate.py "modern conference room, clean minimalist" --size 768x512
```

输出：`/tmp/framefly-img-<timestamp>.png`

### 直接 curl

```bash
curl https://relay.framefly.com.cn/v1/images/generations \
  -H "Authorization: Bearer $FRAMEFLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-image-2","prompt":"...","n":1,"size":"768x512"}'
```

响应格式：`{"data":[{"b64_json":"..."}]}` 或 `{"data":[{"url":"..."}]}`

---

## 方案C：纯CSS视觉设计（回退方案）

当 z-image-turbo 和 framefly 都不可用时，使用纯 CSS 实现视觉风格。适合玻璃质感/科技风。

### 适用场景

- z-image-turbo 返回 `model_load_timeout`
- framefly 返回 `no_available_channel` 或超时
- 用户指定了详细的视觉效果描述（如 "通透蓝色科技调性，半透明玻璃质感"）

### 实现方法

用 CSS `backdrop-filter: blur()`, 渐变, `box-shadow` 模拟玻璃质感：

```css
.glass-card {
  background: rgba(255,255,255,0.55);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.7);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(76, 128, 255, 0.10),
              inset 0 1px 0 rgba(255,255,255,0.8);
}
```

### 3D 玻璃装饰元素

```html
<div class="glass-3d" style="width:360px; height:360px; position:relative;
     background:linear-gradient(135deg, rgba(255,255,255,0.5), rgba(200,224,255,0.3));
     border-radius:24px; border:1px solid rgba(255,255,255,0.6);">
  <!-- 高光层 -->
  <div style="position:absolute; top:0; left:0; width:100%; height:50%;
       background:linear-gradient(180deg, rgba(255,255,255,0.3), transparent);
       pointer-events:none; border-radius:24px 24px 0 0;"></div>
</div>
```

### 背景光晕

```css
.bg-decor .orb {
  position:absolute; border-radius:50%;
  filter:blur(80px); opacity:0.25;
}
```

### 替换策略

当用户指定了自定义视觉风格且图片不可用时，在 Phase 0 确认清单中把 "配图来源" 自动设为 "纯CSS无图片"，并向用户说明原因。

| 数量 | 用途分配 |
|---|---|
| 2张 | 封面右列 + 功能展示 |
| 3张 | 封面 + 功能A + 功能B（推荐） |
| 4张 | 封面 + 功能A + 功能B + 数据/优势背景 |

## 图片存放

```bash
mkdir -p <项目名>/assets
cp /tmp/output*.png <项目名>/assets/
```
