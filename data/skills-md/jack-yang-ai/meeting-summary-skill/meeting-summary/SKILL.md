---
name: meeting-summary
description: |
  会议录音转结构化纪要的编排型 skill。支持 Step ASR 转写、pyannote 说话人分割、声纹实名匹配、结构化摘要生成，以及长录音的 chunk 化增量处理。

  触发条件：
  (1) 用户发送会议录音文件（mp3/wav/ogg/opus/m4a/flac）
  (2) 用户说"总结会议"、"会议纪要"、"帮我总结录音"、"meeting summary"
  (3) 用户说"注册声纹"、"记住我的声音"、"enroll voiceprint"
  (4) 用户说"谁在说话"、"识别说话人"、"identify speaker"
  (5) 用户发送音频文件并要求转写、标注说话人
  (6) 用户要求先快速出纪要、再补 speaker 精度
  (7) 用户要求参考历史纪要风格生成新的会议摘要

  使用模型：
  - ASR 转写：`step-asr`（文件上传接口）
  - LLM（估人数 + 纪要生成）：`step-3.5-flash`（可通过环境变量 MEETING_SUMMARY_LLM_MODEL 覆盖）

  依赖：
  - StepFun API Key（ASR + LLM）— 申请地址 https://platform.stepfun.com/interface-key
  - ffmpeg（音频预处理）
  - Python: numpy, scipy, soundfile, onnxruntime
  - 可选：pyannote.audio（独立 venv，需 PyTorch）
  - 本地模型（wespeaker / pyannote）需从 https://huggingface.co/ 注册账号并获取权限后下载
  - 详见 references/setup-guide.md
version: 2.1.0
tags:
  - meeting
  - asr
  - speaker-diarization
  - voiceprint
  - summary
  - transcription
  - step-asr
  - pyannote
---

# Meeting Summary Skill

把会议录音处理成**可交付的结构化纪要**。默认策略不是追求一次完美，而是：**先出可用结果，再逐步补精度**。

## 使用原则

1. **优先交付，再补精度**  
   长录音或 CPU 机器上，不要默认整场重跑 diarization。优先使用缓存和快速模式，先产出一版可读纪要。

2. **已知信息直接传入**  
   已知参会人数 → 传 `--num-speakers`；已知人名映射 → 传 `--speaker-map`。不要把可以确定的信息交给模型猜。

3. **LLM 估计只是参考**  
   说话人数估计在多人插话场景会偏低。若转写文本明显存在多角色切换，主动上调人数或提示用户确认。建议保守下限：`max(4, llm_estimate)`。

4. **长录音先怀疑方法，不硬跑**  
   pyannote 在 CPU 上对 30+ 分钟音频会很慢。优先考虑 `--max-new-chunks 2-3`、分段、缓存复用，而不是整场硬跑。

5. **Unknown 是正常现象**  
   未注册声纹、录音太短或太吵时，`Unknown` 占比高是预期行为，不是脚本故障。

## 依赖与安装

完整安装说明：读取 `{baseDir}/references/setup-guide.md`

最小检查清单：
- [ ] ffmpeg 已安装
- [ ] `~/.stepfun_api_key` 或 `STEPFUN_API_KEY` 已配置
- [ ] `pip3 install numpy scipy soundfile onnxruntime`
- [ ] wespeaker ONNX 模型已放到工作区模型目录（从 [Hugging Face](https://huggingface.co/) 下载）
- [ ] （可选）pyannote 独立 venv 已配置，`MEETING_SUMMARY_PYANNOTE_PYTHON` 已设（需 Hugging Face 账号 + 接受模型协议）

## 默认执行流程

```text
1. ffmpeg 预处理 → 16kHz 单声道 WAV
2. Step ASR 全文转写（优先命中缓存）
3. LLM 估计说话人数
4. 切 chunk，计算信息量 / region count
5. 对高价值 chunk 跑 pyannote diarization（优先命中缓存）
6. 应用已知声纹和 speaker-map
7. 生成结构化 summary + markdown 纪要
```

## 标准调用

### 完整会议处理

```bash
python3 {baseDir}/scripts/meeting-summarize.py \
  --audio /path/to/meeting.m4a \
  --out /tmp/meeting-summary.json \
  --minutes-out /tmp/meeting-summary.md
```

### 已知人数 + 人名映射

```bash
python3 {baseDir}/scripts/meeting-summarize.py \
  --audio /path/to/meeting.m4a \
  --num-speakers 4 \
  --speaker-map /tmp/speaker-map.json \
  --out /tmp/meeting-summary.json \
  --minutes-out /tmp/meeting-summary.md
```

`speaker-map.json` 格式：

```json
{
  "Speaker_A": "张三",
  "Speaker_B": "李四",
  "Speaker_C": "王五",
  "Speaker_D": "赵六"
}
```

### 快速模式（优先交付）

```bash
python3 {baseDir}/scripts/meeting-summarize.py \
  --audio /path/to/meeting.m4a \
  --max-new-chunks 2 \
  --out /tmp/summary.json \
  --minutes-out /tmp/summary.md
```

### 仅转写

```bash
python3 {baseDir}/scripts/meeting-summarize.py \
  --audio /path/to/meeting.m4a \
  --transcript-only
```

### 参考历史纪要风格

```bash
python3 {baseDir}/scripts/meeting-summarize.py \
  --audio /path/to/meeting.m4a \
  --reference /path/to/older-summary.md \
  --out /tmp/summary.json
```

## 声纹管理

```bash
# 注册声纹（建议 3-10 秒、清晰、单人语音）
python3 {baseDir}/scripts/voiceprint-manager.py enroll --name "张三" --audio /path/to/voice.wav

# 识别说话人
python3 {baseDir}/scripts/voiceprint-manager.py identify --audio /path/to/audio.wav --json

# 查看已注册声纹
python3 {baseDir}/scripts/voiceprint-manager.py list

# 删除声纹
python3 {baseDir}/scripts/voiceprint-manager.py delete --name "张三"
```

## Agent 调用策略

### 收到"帮我总结会议/录音"时

1. 跑主脚本，获取 JSON 输出
2. 优先展示 `summary_markdown`，不要把底层 JSON 原样甩给用户
3. 如有 `open_questions` 或 `confidence_flags`，一并告诉用户哪些地方待确认
4. 用户补充人名、人数或角色信息后，用 `--speaker-map` / `--num-speakers` 复跑

### 收到"谁在说话 / 标注说话人"时

1. 先判断是否已有声纹库可用
2. 若没有，明确告诉用户可以先注册常见参会人声纹
3. 若有大量 `Unknown`，优先解释为音频质量/样本不足/声纹未注册，而不是归因脚本错误

### 收到"先快点给我个纪要"时

直接使用：
- `--max-new-chunks 2` 或 `3`
- 已知人数就传 `--num-speakers`
- 不要默认整场重型 diarization

## 判断与降级规则

### 说话人数判断
- 默认 LLM 估计值可能偏低，尤其是口语化、多人插话时
- 若转写里明显存在 3+ 角色切换、多个称呼或问答往返，不要机械接受低估值
- 保守策略：用户未指定时，把估计值当参考，必要时提示"可能不止 X 人"

### 长录音处理
- 30+ 分钟音频：默认认为 pyannote CPU 推理可能很慢
- 优先用快速模式先出纪要，再决定是否补跑更多 chunk
- 改人名、改格式时，应优先复用缓存，不要重复 ASR / diarization

### 大文件处理
- 大文件不要默认硬传整段
- 如遇上传或转写受限，优先考虑压缩、分段或 transcript-only

## 输出字段

| 字段 | 用途 |
|------|------|
| `summary_markdown` | 优先展示给用户的可读纪要 |
| `open_questions` | 告诉用户哪些信息仍待确认 |
| `confidence_flags` | 告诉用户哪里置信度低 |
| `speakers` | 查看说话人映射质量 |
| `speaker_review` | 复核 speaker_hint → 最终 speaker |
| `speaker_count_estimate` | 仅作参考，不要盲信 |
| `diarization_meta` | 查看 chunk 计划、优先级、命中情况 |
| `segments` | 需要细粒度核查时再看 |

## 缓存机制

缓存目录：`cache/meeting-summary/`

- **ASR 缓存**：`<音频哈希>--asr--<语言>.json`
- **Diarization chunk 缓存**：`<音频哈希>--chunk-diarization--<说话人数>--<chunk序号>--<起始>--<结束>--<模式>.json`

使用原则：
- 改 speaker-map 时，不重跑 ASR
- 改纪要风格时，不重跑 diarization
- 只补缺失 chunk，不整场重算

## 已知限制

- pyannote CPU 推理慢，30 分钟音频可能需要较长时间
- 声纹匹配受音频质量、说话时长、噪音影响明显
- LLM 估人数在多人打断场景容易低估
- 未注册声纹时，`Unknown` 占比高是正常现象
- 不支持实时转写，仅离线处理

## 参考文件

- **完整安装 / 环境排障**：`{baseDir}/references/setup-guide.md`
