# HyperFrames HTML 写作规则

全部强制性规则，来自 HyperFrames 框架要求和真实项目验证。

## 10条硬规则

1. 定时元素必须有 `data-start="N"`, `data-duration="N"`, `data-track-index="N"`
2. 可见定时元素必须加 `class="clip"`（框架用此管理可见性）
3. GSAP timeline 创建时 `paused: true`
4. 注册到 `window.__timelines["main"] = tl`（或对应组合 ID）
5. **禁止** `Math.random()` / `Date.now()` / 运行时网络请求
6. 内容容器用 `flex + padding`，**禁止** `position: absolute` 定位内容
7. 先写静态 CSS 定最终位置，再用 `gsap.from()` 做入场
8. 每个场景 exit 必须跟 `tl.set(sel, {opacity:0}, endTime)` 硬查杀
9. **禁止在 clip 元素上设置 `visibility`**（触发 `gsap_animates_clip_element` 错误）
10. 视频标签加 `muted` + 单独的 `<audio>` 元素做音频轨道

## 项目初始化

```bash
npx --yes hyperframes@latest init <项目名>
cd <项目名>
mkdir assets
```

## GSAP 动效模板

### 场景入场
```js
tl.from("#scene1 .title", { y: 60, opacity: 0, duration: 0.8, ease: "power3.out" }, startTime);
tl.from("#scene1 .subtitle", { y: 40, opacity: 0, duration: 0.6, ease: "power3.out" }, startTime + 0.3);
```

### 卡片串行出现
```js
tl.from("#scene2 .card", { y: 50, opacity: 0, duration: 0.5, stagger: 0.15, ease: "power3.out" }, startTime + 0.3);
```

### 场景出场 + 硬查杀（关键）
```js
// exit tween 在 scene 结束前 0.5s 开始
tl.to("#scene1", { opacity: 0, duration: 0.5, ease: "power2.in" }, startTime + duration - 0.5);
// 硬查杀精确在 scene 结束时刻（绝对值 = startTime + duration）
tl.set("#scene1", { opacity: 0 }, endTime);
```

### 数字 countUp 动画
```js
var countUp = function(sel, target, suffix) {
  var el = document.querySelector(sel);
  var obj = { val: 0 };
  el.textContent = "0" + suffix;
  tl.to(obj, { val: target, duration: 2.5, ease: "power2.out",
    onUpdate: function() { el.textContent = Math.round(obj.val) + suffix; }
  }, startTime);
};
countUp("#num1", 60, "%+");
```

## 音频轨道

### 旁白
每段旁白一个 `<audio>` 标签，时长精确匹配 TTS 输出：
```html
<audio id="nar1" class="audio-hidden" data-start="0" data-duration="9.5"
       src="assets/narration_scene1.mp3" preload="auto"></audio>
```

### 背景音乐
一个 `<audio>` 标签覆盖全片：
```html
<audio id="bgm" class="audio-hidden" data-start="0" data-duration="110"
       src="assets/bg_music.mp3" preload="auto"></audio>
```

### 生成方法
- 旁白：Hermes `text_to_speech` 工具（Edge TTS，中文支持好）
- **格式处理**：`text_to_speech` 输出 `.ogg` 格式，需转换为 `.mp3` 以确保浏览器兼容：
  ```bash
  ffmpeg -y -i assets/narration_scene1.ogg -codec:a libmp3lame -b:a 128k assets/narration_scene1.mp3
  ```
- 获取每段音频精确时长以计算场景时序：
  ```bash
  ffprobe -v error -show_entries format=duration -of csv=p=0 assets/narration_scene1.mp3
  ```
- 场景 `data-duration` = 音频时长 + 0.5s 缓冲
- 背景音乐：`ffmpeg -f lavfi -i "sine=..."` 生成简单环境垫音，或下载 CC0 曲目

## AI 字幕系统

当 Phase 0 中 `AI 字幕 = 需要` 时，在 HTML 中叠加字幕轨道。

### HTML 结构

```html
<!-- 字幕容器，置于 #root 末尾，覆盖全片 -->
<div id="subtitle" class="clip" data-start="0" data-duration="92" data-track-index="8"></div>
```

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
  white-space: nowrap;
  pointer-events: none;
}
```

### JS 驱动（在 timeline 注册）

```js
var subtitleData = [
  { start: 0, end: 7.7, text: "当AI智能体成为企业标配..." },
  { start: 8.2, end: 20.9, text: "会议开始前30分钟还在打印材料？..." },
  // ... 每场景一条，start/end 匹配场景时间
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

### 字幕数据来源

每段字幕文本 = 对应场景的 TTS 旁白原文。`start`/`end` 使用旁白音频的实际起止时间（不是 scene 的 `data-duration`，因为场景包含 0.5s 出场缓冲，字幕应在音频结束时消失）。

## 验证命令

```bash
npm run check   # lint → validate → inspect 三合一
```

## 修复清单（按优先级）

| 错误/警告 | 修复方式 | 优先级 |
|---|---|---|
| `gsap_exit_missing_hard_kill` | 加 `tl.set(sel, {opacity:0}, endTime)` | **必须** |
| `WCAG AA contrast` | 调大背景不透明度 + 加 `color:#fff` | 建议 |
| **`gsap_animates_clip_element`** | 删除 `visibility:hidden`，只保留 `opacity:0` | **必须** |
| `scene_layer_missing_visibility_kill` | **不修复**（clip 框架矛盾，忽略） | 忽略 |
| `composition_file_too_large` | 拆子组合（可选） | 可选 |

## 关键坑

### visibility 与 clip 冲突

```
❌ tl.set("#scene", { opacity: 0, visibility: "hidden" }, t)  → 9 errors
✅ tl.set("#scene", { opacity: 0 }, t)                         → 0 errors
```
原因：HyperFrames 通过 `class="clip"` 管理可见性，禁止在 clip 元素上设置 `visibility`。
scene_layer_missing_visibility_kill 警告是 linter 与 clip 的已知矛盾，安全忽略。

### Linter 假阳性：root_missing_composition_id / root_missing_dimensions

即使 `#root` 元素已有 `data-composition-id="main"`、`data-width="1920"`、`data-height="1080"`，linter（v0.6.4）仍可能报错。这是已知 linter bug，不影响 `validate` 和 `render`。确认属性确实存在后可直接忽略此错误继续。

验证方法是检查 `npm run check` 中的 validate 和 inspect 步骤是否通过——如果 validate 无报错则视频可正常渲染。
