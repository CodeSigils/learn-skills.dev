---
name: video-understanding
description: Video understanding through ModelScope's OpenAI-compatible free API quota. Use when Codex needs to analyze local video files or video URLs, summarize videos, inspect scenes, run custom video prompts, validate video sources, or replace DashScope/Bailian video analysis flows with ModelScope.
---

# Video Understanding

Use this skill to understand video content with ModelScope's OpenAI-compatible API. It supports local video paths and HTTP(S) video URLs, and provides comprehensive analysis, summarization, scene analysis, custom prompts, and source validation without requiring a separate service.

## Core Workflow

1. Prefer the bundled script:

   ```bash
   python scripts/modelscope_video_understanding.py analyze "media/sample.mp4"
   ```

2. Configure a ModelScope token before calling the API. Copy `.env.example` to `.env`, or set environment variables directly. The script resolves credentials in this order:

   1. Process environment variables, such as `MODELSCOPE_API_KEY` or `MODELSCOPE_ACCESS_TOKEN`.
   2. A `.env` file in the current working directory.
   3. The skill directory `.env` next to this `SKILL.md`, such as `.agents/skills/video-understanding/.env`.

   Optional `.env` example:

   ```dotenv
   MODELSCOPE_API_KEY=ms-...
   MODELSCOPE_MODEL=Qwen/Qwen3.5-397B-A17B
   MODELSCOPE_BASE_URL=https://api-inference.modelscope.cn/v1/
   ```

   Do not hard-code real tokens in Python files, docs, or prompts.

3. Use `--json` when the caller needs machine-readable output, metadata, timing, or errors.

4. For local files, the script converts the video to a `data:<mime>;base64,...` URL. For remote URLs, it sends the URL directly.

5. For long or high-bitrate local videos, prefer preprocessing before analysis:

   ```bash
   python scripts/modelscope_video_understanding.py analyze "media/demo.mp4" --preprocess --fps 0.1 --json
   ```

   Use `--auto-preprocess` when you want the script to retry automatically after ModelScope returns an empty `choices` response for a local video.

## Commands

- `analyze <video>`: comprehensive content analysis.
- `summarize <video> --summary-type general|detailed|brief`: summary generation.
- `scenes <video> [--no-scene-detection] [--detailed-analysis]`: scene structure and transitions.
- `custom <video> --prompt "..." [--focus ...] [--output-format ...] [--language zh-CN|en|auto]`: custom analysis.
- `validate <video> [--check-url] [--json]`: source validation without model analysis.

Common options:

- `--model`: defaults to `Qwen/Qwen3.5-397B-A17B` or `MODELSCOPE_MODEL`.
- `--max-tokens`: defaults to `4096`.
- `--temperature`: defaults to `0.7`.
- `--fps`: frame sampling rate, defaults to `2.0`.
- `--timeout`: request timeout in seconds, defaults to `300`.
- `--max-retries`: defaults to `3`.
- `--max-file-size-mb`: defaults to `100`.
- `--preprocess`: normalize local videos with ffmpeg before sending them to ModelScope.
- `--auto-preprocess`: retry local videos once with preprocessing when ModelScope returns an empty response.
- `--preprocess-width`: defaults to `640`.
- `--preprocess-crf`: defaults to `30`.
- `--no-preprocess-audio`: remove audio during preprocessing; by default audio is kept as AAC `64k`.

## Model Selection

- Prefer `Qwen/Qwen3.5-397B-A17B` when accuracy matters, especially for longer videos, narration-heavy videos, text-heavy videos, or tasks requiring cross-modal reasoning. It has been more stable in tests, but free quota may be exhausted faster.
- Use `Qwen/Qwen3.5-122B-A10B` as a fallback when the primary model quota is exhausted. It can continue processing, but tests showed it may lean toward visual description and can miss details that require combining audio, visible text, and temporal context.
- Keep the model configurable through `MODELSCOPE_MODEL` instead of hard-coding it.

## Robustness Rules

- Validate file existence, extension, readability, and size before API calls.
- Validate URL scheme and supported video extension when one is present.
- Retry transient API failures with exponential backoff and jitter.
- For local videos that fail with empty `choices`, retry with ffmpeg preprocessing when `--auto-preprocess` is enabled.
- Return structured failures instead of throwing raw tracebacks when `--json` is used.
- Parse OpenAI-compatible responses defensively: handle plain strings, content lists, dict parts, empty choices, and usage metadata.
- Keep prompts explicit about output language and format for custom analysis.

## Local Video Limits

ModelScope failures are not controlled by duration alone. Empirical testing showed local video success depends on a combined media budget: encoded size, codec shape, frame sampling, audio, and resulting prompt tokens. A 5m15s source video failed in its original 31.8MB form, but succeeded after preprocessing to 640px H.264 with AAC audio at about 8.8MB and `--fps 0.1`.

Do not only tune `--fps`. For long videos, reduce resolution and bitrate too. A 320px-wide preprocessed segment can reduce prompt tokens dramatically compared with 640px while still preserving enough visual and textual information for many analysis tasks.

Recommended defaults for unstable local videos:

```bash
python scripts/modelscope_video_understanding.py analyze "media/demo.mp4" --preprocess --fps 0.1 --max-tokens 8192 --json
```

For long videos or token-heavy videos, start with:

```bash
python scripts/modelscope_video_understanding.py analyze "media/demo.mp4" --preprocess --preprocess-width 320 --preprocess-crf 36 --fps 0.1 --max-tokens 8192 --json
```

For unattended usage:

```bash
python scripts/modelscope_video_understanding.py analyze "media/demo.mp4" --auto-preprocess --fps 0.1 --json
```

For videos longer than about 10 minutes, prefer manual segmentation and final aggregation. Current CLI does not yet automate segmentation.

## Remote Video Notes

- Plain direct MP4 URLs may work through `video_url`, but ModelScope can return empty `choices` depending on server-side fetch behavior and sampling parameters.
- Some CDN, signed, anti-hotlinking, expiring, or header-sensitive URLs may validate as accessible but still fail during ModelScope server-side fetching or processing. They may require request headers that the current CLI does not inject for remote `video_url` requests.
- For unstable remote URLs, the more stable workflow is to download or transcode the video with appropriate access settings, then analyze the resulting local file or short segments.

## Supported Formats

The script accepts `.mp4`, `.webm`, `.mov`, `.avi`, `.mkv`, and `.flv`.

## Examples

```bash
python scripts/modelscope_video_understanding.py analyze "media/demo.mp4" --prompt "请提取画面中的人物、动作、事件和可见文字。"
python scripts/modelscope_video_understanding.py analyze "media/demo.mp4" --preprocess --fps 0.1 --json
python scripts/modelscope_video_understanding.py summarize "https://example.com/video.mp4" --summary-type detailed --json
python scripts/modelscope_video_understanding.py scenes "media/demo.mp4" --detailed-analysis
python scripts/modelscope_video_understanding.py custom "media/demo.mp4" --focus commercial --output-format structured --prompt "分析这个视频适合作为广告素材的原因。"
python scripts/modelscope_video_understanding.py validate "media/demo.mp4" --json
```

## When Editing

- Keep `scripts/modelscope_video_understanding.py` as the single source of truth for ModelScope API calls.
- Do not reintroduce DashScope-specific SDK calls or `DASHSCOPE_API_KEY`.
- Do not store real API tokens in the repository.
