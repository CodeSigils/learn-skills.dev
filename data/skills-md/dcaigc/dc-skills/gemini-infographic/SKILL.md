---
name: gemini-infographic
description: Generate infographic images from user descriptions using Gemini API (Nano Banana Pro). Converts natural language descriptions into structured infographic prompts, then calls Gemini image generation to produce PNG images. Supports 11 visual styles (sketchnote, kawaii, professional, scientific, anime, claymation, editorial, storyboard, bento grid, bricks), 3 orientations (landscape/portrait/square), 3 detail levels (brief/standard/detailed), and multiple languages. Use when user asks to create infographics, generate visual summaries, make data visualizations, or produce illustrated explanations. Trigger words include 信息图, infographic, 生成图, 可视化, visual summary, data visualization.
---

# Gemini Infographic Generator

Generate professional infographic images from text descriptions using Gemini Nano Banana Pro SDK (`@google/genai`).

## Prerequisites

1. **API Key**: Configured in skill `.env` file with `GEMINI_API_KEY=...` and `HTTPS_PROXY=...` (if needed).
2. **Node.js 18+**: Dependencies pre-installed in `scripts/node_modules/`.

## Workflow

### Step 1: Understand the User's Request

Extract from the user's description:
- **Topic**: What the infographic is about
- **Style**: Preferred visual style (see [styles.md](references/styles.md))
- **Orientation**: landscape (default), portrait, or square
- **Detail level**: brief, standard, or detailed (default)
- **Language**: zh-CN (default), en, ja, ko, etc.

Defaults when not specified: style=`auto`, orientation=`landscape`, detail=`detailed`, language=`zh-CN`.

### Step 2: Generate the Infographic

Run the generation script:

```bash
node {SKILL_DIR}/scripts/generate_infographic.mjs \
  --prompt "user's description here" \
  --style professional \
  --orientation landscape \
  --detail detailed \
  --language zh-CN \
  --output "{WORKSPACE}/infographic/{DATE}" \
  --name "descriptive_filename"
```

Replace `{WORKSPACE}` with the current workspace root, `{DATE}` with today's `YYYY-MM-DD`.

**Parameters:**

| Parameter | Values | Default |
|-----------|--------|---------|
| `--style` | auto, sketchnote, kawaii, professional, scientific, anime, claymation, editorial, storyboard, bento, bricks | auto |
| `--orientation` | landscape, portrait, square | landscape |
| `--detail` | brief, standard, detailed | detailed |
| `--language` | zh-CN, en, ja, ko, or any language name | zh-CN |
| `--model` | gemini-3-pro-image-preview, gemini-3.1-flash-image-preview | gemini-3-pro-image-preview |
| `--resolution` | 512, 1K, 2K, 4K | 2K |

### Step 3: Verify and Report

After generation, confirm the output file exists and report its path. Re-run with modified parameters for adjustments.

## Examples

**User**: "做一个关于全球气候变化的信息图，专业风格"
```bash
node {SKILL_DIR}/scripts/generate_infographic.mjs \
  --prompt "全球气候变化：温度趋势、碳排放数据、冰川融化、海平面上升" \
  --style professional --detail detailed \
  --output "./infographic/2026-03-17" --name "climate_change"
```

**User**: "Create a cute infographic about photosynthesis"
```bash
node {SKILL_DIR}/scripts/generate_infographic.mjs \
  --prompt "Photosynthesis: sunlight + water + CO2 → glucose + oxygen" \
  --style kawaii --detail standard --language en \
  --output "./infographic/2026-03-17" --name "photosynthesis"
```

## Style & Prompt Tips

- Data-heavy → `professional` or `scientific`
- Educational → `storyboard` or `sketchnote`
- Social media → `portrait` + `kawaii` or `anime`
- Enrich user descriptions with data points and section breakdowns before passing to script
- See [styles.md](references/styles.md) and [prompt_template.md](references/prompt_template.md) for details
