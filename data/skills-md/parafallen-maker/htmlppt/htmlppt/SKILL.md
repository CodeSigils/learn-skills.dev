---
name: htmlppt
description: 生成可分享、可导出 PDF 的 HTML 演示文稿。适用于从零创建演示、把 PPT/PPTX 转成网页幻灯片，或增强现有 HTML 演示。
version: 1.0.0
---

# htmlppt

生成单文件、动效丰富、适配桌面与移动端的 HTML 演示文稿。

## 核心原则

1. **单文件优先**：默认输出单个 HTML，CSS / JS 尽量内联，不引入构建步骤。
2. **先看风格再定方向**：用户通常说不清审美，要先给视觉预览。
3. **每页锁定视口**：每张幻灯片必须适配 `100vh` / `100dvh`，严禁页内滚动。
4. **中文优先考虑字形覆盖**：中文内容不能只用拉丁展示字体，必须有 CJK fallback。
5. **内容过密就拆页**：不要把超长文案硬塞进一页。

## 设计规则

### 避免廉价 AI 风格

- 不要默认紫色渐变白底
- 不要无差别居中、大圆角卡片、套模板式 hero
- 不要只用 Inter / Roboto / Arial 这类安全但平庸的字体

### 字体策略

如果演示里有明显中文内容，必须使用下面的回退链之一：

- 中文无衬线：`"Noto Sans SC", "Source Han Sans SC", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", sans-serif`
- 中文衬线：`"Noto Serif SC", "Source Han Serif SC", "Songti SC", "STSong", "SimSun", serif`

如果需要有设计感的拉丁标题字体，可以放在最前面，但后面必须接中文 fallback。示例：

```css
--font-display: "Clash Display", "Noto Sans SC", "Source Han Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
```

### 视口规则

每个 `.slide` 都必须满足：

- `height: 100vh;`
- `height: 100dvh;`
- `overflow: hidden;`

所有字号和间距都要用 `clamp()`。图片默认限制：

```css
max-height: min(50vh, 400px);
```

必要断点：

- `max-height: 700px`
- `max-height: 600px`
- `max-height: 500px`

并始终支持：

- `prefers-reduced-motion`

### 单页内容上限

| 页型 | 建议上限 |
| --- | --- |
| 标题页 | 1 个标题 + 1 个副标题 + 可选一句标语 |
| 内容页 | 1 个标题 + 4 到 6 个要点，或 2 段短文 |
| 卡片页 | 6 个卡片以内 |
| 代码页 | 8 到 10 行代码以内 |
| 引言页 | 1 段引言 + 署名 |
| 图片页 | 1 个标题 + 1 张主图 |

超出上限就拆成多页，不能滚动。

## 模式判断

优先判断用户处于哪一种模式：

- **模式 A：新建演示**
- **模式 B：PPT / PPTX 转 HTML**
- **模式 C：增强已有 HTML 演示**

## 模式 A：新建演示

### 第一步：一次性收集上下文

如果宿主支持结构化问题，就一次性收集下面 4 项；如果不支持，就用一条简洁消息把这 4 项一起问完：

1. 演示用途：路演 / 教学 / 内部汇报 / 发布会 / 其他
2. 页数范围：5-10 / 10-20 / 20+
3. 内容准备程度：完整文案 / 粗略提纲 / 只有主题
4. 是否需要浏览器内直接改字：需要 / 不需要

如果用户已经给了文案、提纲、图片目录，就不要重复问。

### 第二步：评估图片素材

如果用户给了图片或 logo：

1. 列出图片文件
2. 判断每张图能否直接上屏
3. 提取颜色、主体、适合放在哪类页面
4. 用素材反推页结构，而不是先定页结构再硬塞图片

### 第三步：风格选择

风格选择有两种方式：

- **看 3 个预览后再选**，推荐
- **直接选预设**

如果走预览流程，先问用户希望观众感受到什么，可以多选最多 2 个：

- 专业可信
- 激动振奋
- 冷静聚焦
- 有感染力

然后根据情绪，从 `STYLE_PRESETS.md` 里选 3 套差异足够大的风格，生成 3 个单页 HTML 预览给用户挑。

### 第四步：生成整套演示

生成前必须读取：

- `STYLE_PRESETS.md`
- `viewport-base.css`
- `html-template.md`
- `animation-patterns.md`

输出要求：

- 单个 HTML 文件
- `<style>` 中完整包含 `viewport-base.css`
- 字体链必须兼容中文
- 必须有清晰的段落注释，便于后续手改
- 键盘、滚轮、触摸滑动、导航点、进度条要可用

## 模式 B：PPT / PPTX 转 HTML

先执行：

```bash
python3 scripts/extract-pptx.py <input.pptx> <output_dir>
```

如果缺依赖，安装：

```bash
pip install python-pptx
```

然后：

1. 向用户确认抽取结果，包括页标题、图片数、备注
2. 告知这是“内容抽取 + 重新设计”，不是原版布局复刻
3. 继续走风格选择和 HTML 生成流程

## 模式 C：增强已有 HTML

先读原始 HTML，确认：

- `.slide` 是否存在
- 是否已经使用 `100vh / 100dvh`
- 是否存在页内滚动
- 是否有中文但字体链只写了拉丁字体

增强时遵守：

1. 加文字前先判断是否超出单页上限
2. 加图片前先检查当前页是否已经满了
3. 修改后验证每一页仍然可在 `1280x720` 下完整显示
4. 如果会溢出，主动拆页

## 交付

生成完成后：

1. 告知文件路径、页数、所选风格
2. 说明导航方式：
   - 键盘方向键 / Space
   - 滚轮或触控滑动
   - 导航点点击
3. 说明怎么改主题：
   - `:root` 颜色变量
   - 字体链接和字体变量
   - `.reveal` 动效类
4. 如果启用了浏览器内编辑，说明：
   - 鼠标移到左上角或按 `E`
   - 点文本直接编辑
   - `Ctrl+S` / `Cmd+S` 导出保存

## 分享与导出

交付后可以继续两步：

### 部署 URL

```bash
bash scripts/deploy.sh <html-or-folder>
```

用途：

- 手机、平板、电脑都能直接打开
- 适合发微信、Slack、邮件、Notion

### 导出 PDF

```bash
bash scripts/export-pdf.sh <path-to-html> [output.pdf]
bash scripts/export-pdf.sh <path-to-html> [output.pdf] --compact
```

说明：

- 导出是逐页截图后合并 PDF
- 动画不会保留，只保留最终静态画面
- 脚本会先查找现有 Playwright，缺失时再做临时安装

## 宿主兼容规则

这个 skill 设计成宿主无关：

- 不假设必须存在某个专用插件系统
- 如果宿主支持结构化问答，就一次收集信息
- 如果宿主只支持普通对话，就用一条消息把问题集中问完
- 如果宿主支持额外 frontmatter 元数据，可以单独在宿主分发包里补充，但核心工作流保持一致

## 支撑文件

| 文件 | 作用 | 何时读取 |
| --- | --- | --- |
| `STYLE_PRESETS.md` | 12 套风格预设与字体搭配 | 选风格时 |
| `viewport-base.css` | 视口适配基础样式 | 生成 HTML 前 |
| `html-template.md` | 结构模板、交互与内联编辑实现 | 生成 HTML 前 |
| `animation-patterns.md` | 动效模式参考 | 生成 HTML 前 |
| `scripts/extract-pptx.py` | PPT 内容抽取 | PPT 转换时 |
| `scripts/deploy.sh` | Vercel 部署 | 分享链接时 |
| `scripts/export-pdf.sh` | PDF 导出 | 导出静态版时 |
