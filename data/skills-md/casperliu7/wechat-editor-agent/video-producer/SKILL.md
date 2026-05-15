---
name: Video Producer
version: 1.0.0
description: Automated short video production workflow combining TTS, screen recording, and AI video generation via FFmpeg.
allowed-tools: Bash, Write, Edit, Read, generate_video, ask_user
user-invocable: true
---
# Skill: Video Producer (工业级短视频自动化工作流)

## Prerequisites
- `ffmpeg` (处理视频比例、运镜、拼接、混音)
- `edge-tts` (生成带有情绪的连续主音轨)
- 内置工具 `generate_video` (仅用于生成无文字、非实操的情感类/人物类空镜)

## Workflow (工作流步骤)

当用户要求生成短视频时，请严格按以下步骤执行，**并必须在关键节点等待用户确认**：

### Step 0: 素材盘点与确认 (Asset Check)
- 当用户仅提供文案时，**首先【强制停顿】**询问用户：“是否有参考素材（图片、录屏、官方视频或网页 URL 等）需要穿插在视频中？”
- 如果用户回答“没有”，则规划为**100% 纯 AI 生成画面**的分镜脚本。
- 如果用户回答“有”或已经上传了素材，则先分析这些原始素材的内容。**针对用户上传的视频素材，必须主动使用 `ffprobe` 提取准确的物理时长（精确到秒）**。如果提供的是网页 URL，Agent 需准备调用浏览器自动化工具进行截屏或录制。

### Step 1: 提炼分镜与脚本确认 (Human-in-the-loop 强制等待)
- 根据 Step 0 的资产盘点，将文案拆分为具体的分镜脚本（Blocks）。
- **【基于时长的字数约束】**：规划旁白时，必须严格参考原视频素材的物理时长匹配对白字数。按照中文 TTS 正常语速（约 4.5字/秒）计算。例如：一段 10 秒的录屏切片，分配的对白必须控制在 40-45 字之间，防止音画严重脱节。
- **【快节奏与静态画面限时】**：为了保持短视频的快节奏，静态截图或图片的展示时间必须**严格限制在 3 秒以内**。如果该段旁白配音超过 3 秒，**必须拆分分镜**：前 3 秒展示截图，剩余时间使用相关的 AI 生成动态画面（B-roll）来无缝填充，绝不能删减原旁白文字或让单张图片定格过久。
- **【结尾 CTA 动态化】**：视频结尾的 Call to Action (CTA) 或 Logo 展示，不能仅用一张静止图片。必须将其规划为使用 `generate_video` 结合 Logo 素材（作为 attachment）生成的 3D 动态视频片段，提升结尾的商业质感。
- **【标准分镜表排版】**：必须以清晰的 Markdown 表格形式输出分镜脚本，绝对不能为了精简而忽略画面提示词的丰富度。表格必须包含以下列，且内容需满足：
  - **分镜编号**：如 Block 1。
  - **旁白 (VO) / 断句**：严格按 15 字以内切分换行，绝对不加表演指导或情绪废话。
  - **时长**：预估或物理提取的确切时长。
  - **画面资产与视觉表现 (Visuals & Prompts)**：
    - 实操素材写明截取区间与处理方式（如：等比居中+高斯模糊底板）。
    - **AI 生成画面写明极度详细的英文 Prompt**，必须包含：主体、动作、环境、光影（如 volumetric lighting, cinematic）、运镜（如 fast-paced dolly zoom）和风格（如 Pixar 3D animated style）。
- **【强制停顿】**：将这份详细的分镜表格发送给用户，并明确询问：“请确认分镜脚本与画面规划是否需要修改？”
- **注意：只有在用户明确回复“确认”或确认无误之后，才能继续执行后续的步骤。绝对不允许跳过此环节擅自开始渲染或总装。**

### Step 2: 生成主音轨与精确字幕 (Master Audio & Subtitles)
- 严禁分段生成音频！
- **【长句切分约束】**：在生成语音之前，如果是竖屏或 3:4 比例，必须将长句文案切割为极短的断句（单句尽量不超过 12-15 个字符），例如把“它自带云端电脑Yolo模式下写代码全包了”切分为多段。这能防止单行字幕溢出屏幕边缘，并让视频节奏显得更加干脆。
- 使用 `edge-tts` 将完整文案一键生成为一个音频文件（如 `master_audio.mp3`），**并务必加上 `--write-subtitles subtitles.srt` 参数，提取与声音完美对齐的字幕文件**。
- 推荐使用情绪饱满的音色，如 `zh-CN-XiaoxiaoNeural` 或 `zh-CN-YunxiNeural`，可适度提高语速（如 `--rate=+10%`）以符合短视频快节奏。

### Step 3: 原画质资产处理 (UI / 截图 / URL) - FFmpeg / Playwright
对于所有带有文字、代码、UI 界面的截图或视频，**绝对不要丢给 AI 生成**：
- **普通图片/截图**：根据该分镜对应配音的字数，计算出图片需要停留的时间（例如 3-5 秒）。使用 FFmpeg 将其转换为静态视频。**【严禁任何动效】**：绝对不要做任何微动效（如缓慢的中心放大 Zoom-in 或呼吸动效）。处理方式非常简单：只需将原图居中显示，并在底层垫上一层该图片的高斯模糊（Gaussian Blur）背景以填充多余区域，彻底保持原画面的纯粹稳定与极简美观。
- **网页 URL 素材（快速滚动录像）**：如果用户提供的是 URL，调用浏览器自动化工具（如 Playwright）打开页面。录制滚动视频时，**保持常规的宽屏或自适应比例**（严禁直接强行录制为 3:4 或窄边比例以免左右信息被暴力裁切）。录像的实现原则：
  1. **首屏零等待**：忽略网络加载和长时间停留，直奔主题。
  2. **高频快滑**：写自动化脚本时（如 `setInterval` 控制），必须将滚动步长增大（如 12 像素），间隔缩短（如 16ms），实现飞速且丝滑的滚动效果。
  3. **去头去尾**：录制完成后，务必使用 FFmpeg/ffprobe 精确截取掉开头的 Loading 或白屏时间，只保留高密度信息的**纯滚动干货画面**，时长控制在 5 秒以内，以适配短视频的极快节奏。
- **视频与录屏素材处理（高斯模糊底板）**：对于尺寸不一致的实操录屏或上面生成的 URL 滚动视频，在转换至目标比例（如 3:4）时，**绝对不能使用黑边填充（Pad 黑边）**。必须像处理截图那样：将原视频居中等比缩放显示，同时在底层垫上一层该视频画面的高斯模糊（Gaussian Blur）作为动态背景以填充多余区域，彻底保持画面的连贯和高级感。

### Step 4: AI 氛围片段生成 (B-roll / 角色) - generate_video
对于钩子、转场、人物喝咖啡等不含复杂文字的情绪镜头：
- **【严格控时，干脆利落】**：调用 `generate_video` 时，`durationSeconds` 参数必须**严格匹配**分镜脚本中该段旁白所需的物理时长（API允许范围4-15秒）。旁白念完画面即止，绝对不要生成过长、拖泥带水的无用废镜头。
- **【成本与分辨率控制】**：为了严格控制 API 成本和大幅提升生成效率，调用 `generate_video` 时必须将 `resolution` 参数设定为最低画质（即 `480p`），除非用户有明确的高清交付需求。
- **【具象化 Prompt 编写】**：AI 视频生成 Prompt 必须高度细节化，且**视觉表现必须与旁白概念精准对应**。严禁使用模糊的抽象词汇。例如：当旁白提到“微信和飞书”，不能只写“social media integration”，必须写成“a glowing green chat bubble and a blue paper plane icon floating in a 3D tech space”；当提到“AI大脑”，必须具体到“a glowing futuristic mechanical brain pulsing with neon blue lights”。
- **【动作节奏约束】**：在 Prompt 中主动加入 `fast-paced, decisive action, quick motion` 等词汇，强制 AI 加快动作执行速度，避免 AI 视频常见的“慢动作拖沓感”。
- 设定 `generateAudio: false`（无声生成）。
- 为了规避真人隐私审查和保持人物一致性，在 Prompt 中加入 "Pixar style 3D animated character"，并将用户的“人物卡”作为 `attachments` 传入。
- 设定好对应的 `aspectRatio`。

### Step 5: 强制标准化与总装拼接 (Normalization & Assembly)
- **【格式绝对统一】**：在最终拼接前，所有生成的素材（不论静图、截图还是生成视频），必须通过 FFmpeg 强行重塑为统一的**目标分辨率（如 720x960）和目标帧率（如 -r 30）**。若参数不一致，后续合成必将导致黑屏或音频断裂。
- 创建 `concat_list.txt`，按顺序排列所有标准化后的视频片段，将其无声拼接为一整段主视频。

### Step 6: 混音与商业字幕烧录 (Final Mix & Hardcoded Subtitles)
- **BGM (全自动配乐)**：**必须自动添加 BGM，绝不要向用户索要**。用 `curl`/`wget` 从公共库下载带有明显节奏感的真实 BGM，截取对应时长并加上音频淡入淡出（afade）。
- **全局混流**：使用 FFmpeg `amix` 滤镜，将 100% 音量的原声主音轨（`master_audio.mp3`）与降至 15%-25% 音量的 BGM 进行平滑混合，确保不会覆盖人声。
- **商业字幕参数**：调用 FFmpeg `subtitles` 滤镜，将 Step 2 提取的 `.srt` 烧录进画面底端。
  - **绝不溢出的防翻车设置**：竖屏短视频中，必须设置相对适中的字号（如 `FontSize=14`）、留出底部安全区避开评论栏（如 `MarginV=35`），并开启描边和阴影确保任何背景下都可见。
  - **推荐模板**：`subtitles=subtitles.srt:force_style='Fontname=SimHei,FontSize=14,Bold=-1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=1,Shadow=1,MarginV=35,Alignment=2'`
- 使用 `-shortest` 截断多余的音频或画面，输出带字幕与精美配乐的终极版成片 MP4。

## Notes
- 永远记住：AI 只负责生成“气氛”和“非特定人脸”，FFmpeg 负责保障“信息清晰度（文字/UI）”和“全局对齐”。
- 处理素材时，严格使用 `force_original_aspect_ratio=decrease` 防止任何素材被拉伸变形。