# Z-Image-Turbo-4bit API

Base URL: `http://localhost:8080`
API KEY: `` (empty)

---

## POST /v1/images/generations

### 参数

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| `model` | string | 否 | `z-image-turbo` | |
| `prompt` | string | **是** | — | 图像描述，1–4000 字 |
| `negative_prompt` | string | 否 | `""` | 不想要的内容 |
| `steps` | int | 否 | `9` | 推理步数，1–100 |
| `guidance` | float | 否 | `0` | CFG 尺度，建议值 0，范围 0–20 |
| `seed` | int | 否 | `-1` | `-1`=随机；≥0 固定结果 |
| `width` | int | 否 | `512` | 可选: 512, 576, 768, 1024, 1280, 1440, 1920 |
| `height` | int | 否 | `512` | 同上 |
| `n` | int | 否 | `1` | 生成张数 |
| `response_format` | string | 否 | `url` | `url` 或 `b64_json` |

### 请求示例

```bash
curl http://localhost:8080/v1/images/generations \
  -H "Content-Type: application/json" \
  -d '{
    "model": "z-image-turbo",
    "prompt": "A serene mountain lake at sunset",
    "negative_prompt": "blurry, watermark",
    "steps": 9,
    "guidance": 0,
    "seed": 42,
    "width": 1024,
    "height": 768
  }'
```

### 响应

```json
{
  "created": 1778700000,
  "data": [
    {
      "url": "http://localhost:8080/output/images/xxx.png"
    }
  ]
}
```

`response_format=b64_json` 时返回 `b64_json` 字段替代 `url`。

---

## POST /v1/images/edits

### 参数

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| `image` | file | **是** | — | PNG / JPEG / WebP，建议 < 4MB |
| `prompt` | string | **是** | — | 编辑描述 |
| `mask` | file | 否 | — | RGBA 遮罩图，尺寸须与 image 一致 |
| `negative_prompt` | string | 否 | `""` | |
| `steps` | int | 否 | `9` | |
| `guidance` | float | 否 | `0` | 建议值 0 |
| `seed` | int | 否 | `-1` | |
| `image_strength` | float | 否 | `0.4` | 原图保留程度，0–1，越大越贴近原图 |
| `width` | int | 否 | 自动 | |
| `height` | int | 否 | 自动 | |
| `n` | int | 否 | `1` | |
| `response_format` | string | 否 | `url` | |

### 请求示例

```bash
curl http://localhost:8080/v1/images/edits \
  -F "image=@input.png" \
  -F "mask=@mask.png" \
  -F "prompt=Replace the object with a red flower" \
  -F "steps=12" \
  -F "guidance=0" \
  -F "image_strength=0.6"
```

---

## POST /v1/chat/completions

以对话方式生成图像。标准 OpenAI 流式接口。

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "z-image-turbo",
    "messages": [
      {"role": "user", "content": "A beautiful sunset over mountains"}
    ],
    "stream": true
  }'
```

---

## GET /v1/models

```bash
curl http://localhost:8080/v1/models
```

---

## 错误码

| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 400 | 参数错误 |
| 413 | 图像过大 |
| 500 | 服务错误 |

```json
{
  "error": {
    "code": "invalid_prompt",
    "message": "Prompt is required",
    "type": "invalid_request_error"
  }
}
```
