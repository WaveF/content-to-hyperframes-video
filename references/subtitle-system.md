# AI 字幕系统

当 Phase 0 中 `AI 字幕 = 需要` 时使用的字幕轨道方案。

## 方案：JS 时序驱动字幕（推荐）

无需外部 ASR/Whisper 服务，基于已知的 TTS 旁白时序生成字幕。

### 数据准备

每段字幕文本 = 对应场景旁白文案。时间范围 = 旁白音频起止时间（不是场景 `data-duration`）。

| 场景 | 字幕文本 | 开始 | 结束 |
|---|---|---|---|
| 封面 | 旁白文案 | 0 | 旁白结束 |
| 痛点 | 旁白文案 | 场景2 start | 场景2旁白结束 |
| ... | ... | ... | ... |

注意：字幕的 end 时间应在旁白音频结束处（通常比 scene 的 data-duration 小 0.5s），确保字幕与语音同步而非与场景过渡同步。

### HTML

```html
<div id="subtitle" class="clip" data-start="0" data-duration="92" data-track-index="N"></div>
```

字幕容器放在 `#root` 内的末尾，`data-duration` 覆盖全片总时长。

### CSS

```css
#subtitle {
  position: absolute; bottom: 60px; left: 50%; transform: translateX(-50%);
  z-index: 100;
  padding: 12px 40px;
  background: rgba(0,0,0,0.55);
  backdrop-filter: blur(8px);
  border-radius: 16px;
  font-size: 28px;
  color: #fff;
  text-align: center;
  white-space: nowrap;        /* 单行，长文会自动截断 */
  pointer-events: none;       /* 不阻挡点击 */
  max-width: 80%;             /* 防止超出屏幕 */
  overflow: hidden;
  text-overflow: ellipsis;
}
```

### JS 实现

```js
var subtitleData = [
  { start: 0, end: 7.7, text: "旁白文案..." },
  { start: 8.2, end: 20.9, text: "旁白文案..." },
  // ... 每场景一条
];
var subEl = document.getElementById("subtitle");
var checkSubtitle = function() {
  var now = tl.time();
  var found = "";
  for (var i = 0; i < subtitleData.length; i++) {
    var s = subtitleData[i];
    if (now >= s.start && now < s.end) { found = s.text; break; }
  }
  subEl.textContent = found;
};
tl.eventCallback("onUpdate", checkSubtitle);
```

### 注意事项

- 文本长度超过底部宽度时会被截断 + ellipsis——控制每段字幕在 40 字以内，或使用多行模式（去掉 `white-space: nowrap`）
- 字幕消失时机应与旁白结束对齐，否则用户会看到静音字幕
- 无需在 `tl.set()` 硬查杀中处理字幕——它自带 `class="clip"`，框架在 `data-duration` 结束后自动隐藏
