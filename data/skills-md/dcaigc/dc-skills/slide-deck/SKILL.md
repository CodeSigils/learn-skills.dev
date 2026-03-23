---
name: slide-deck
description: Generates professional presentation slide decks from text content or topics. Use this skill when the user asks to "create a presentation", "generate slides", "make a slide deck", "create PPT", or mentions presentations, slides, or decks. Produces AI-generated slide images assembled into a PDF.
---

# Slide Deck Generation

Generate professional presentation slides using AI through a 4-step workflow:

1. **Initialize Task** - Create task workspace with unique ID
2. **Generate Outline** - Create structured outline (YAML)
3. **Generate Images** - Run script to create slide images
4. **Assemble PDF** - Combine images into final PDF

## Prerequisites

**API Key** - Set in `.env` file at skill root (auto-loaded by script):
```
GEMINI_API_KEY=your-api-key
```

**Dependencies:**
```bash
pip install -r requirements.txt
```

---

## Workflow

### Step 0: Initialize Task Workspace

When the user starts creating a PPT, immediately generate a Task ID and create a workspace under the **project root directory**:

```powershell
$TASK_ID = (Get-Date -Format "yyyyMMdd_HHmmss") + "_" + -join ((1..6) | ForEach-Object { '{0:x}' -f (Get-Random -Maximum 16) })
New-Item -ItemType Directory -Force -Path "{workspace}/output/$TASK_ID"
```

> `{workspace}` refers to the user's project root directory, **not** the skill directory.

All files will be saved under `{workspace}/output/<task-id>/`.

---

### Step 1: Generate Outline

You are a world-class presentation designer and storyteller.

**First, ask the user to choose:**

| Option | Values | Description |
|--------|--------|-------------|
| **Format** | detailed / medium / presentation | Detailed (standalone reading) / Medium (speech + reading) / Minimal (speech-only aid) |
| **Length** | short / default | Short (5-10 slides) / Default (10-20 slides) |
| **Language** | auto | Auto-detect from user's prompt language; user may also specify explicitly |
| **Other** |  | Target audience, style preferences |

**Then generate outline as YAML**, save to `{workspace}/output/<task-id>/outline.yaml`:

```yaml
style_instructions:
  format: detailed          # detailed | medium | presentation
  length: default           # short | default
  language: <auto-detected or user-specified language>
  design_aesthetic: <design aesthetic description>
  background_color: "#F8F7F5"
  primary_font: <heading font>
  secondary_font: <body font>
  color_palette:
    primary_text: "#2F3542"
    primary_accent: "#007AFF"
  visual_elements: <visual element style description>

slides:
  - slide_number: 1
    slide_type: cover         # cover | content | closing
    narrative_goal: <narrative goal>
    key_content:
      title: <title>
      subtitle: <subtitle>
      body: |
        <body text, adjust density based on format>
    visual:
      description: <detailed visual description for the image generation model>
      elements: [<element1>, <element2>]
    layout:
      composition: <composition description>
      hierarchy: <visual hierarchy>

_metadata:
  task_id: "<task-id>"
  topic: <topic>
  format: detailed
  slide_count: 10
```

**Critical Rules:**

1. **Slide 1 must be a cover page** - Poster-style layout, bold typography, full-bleed imagery
2. **Last slide must be a closing page** - Meaningful visual summary, **never end with "Any questions?" or "Thank you"**
3. **Never exceed 20 slides**
4. **Avoid "Title: Subtitle" format** - Use narrative thematic sentences to connect slides
5. **Avoid AI cliché patterns** - Never use phrases like "It's not just X, it's Y"
6. **Visual descriptions must be thorough** - Detailed enough for an image generation model to understand
7. **Adjust content density based on format**

**Show the outline to the user for approval before proceeding.**

For format-specific outline examples and style templates, see [references/outline_generation.md](references/outline_generation.md).

---

### Step 2: Generate Slide Images

After user approves the outline:

```bash
python scripts/generate_slides.py {workspace}/output/<task-id>/outline.yaml \
  --output-dir {workspace}/output/<task-id>/slides
```

**Common options:**

| Argument | Default | Description |
|----------|---------|-------------|
| `--resolution` | 4K | 1K, 2K, 4K |
| `--max-concurrent` | 4 | Concurrency (reduce to 2 if rate-limited) |
| `--proxy` | None | HTTP proxy URL |
| `--slides` | all | Specify slides: `1,3,5` or `2-5` |

---

### Step 3: Assemble PDF

```bash
python scripts/assemble_pdf.py {workspace}/output/<task-id>/slides/ {workspace}/output/<task-id>/presentation.pdf
```

Optional: `--compress`, `--watermark logo.png`, `--watermark-position bottom-right`, `--watermark-opacity 0.5`

---

## Task Workspace Structure

```
{workspace}/
└── output/
    └── 20240111_143052_a1b2c3/
        ├── outline.yaml
        ├── slides/
        │   ├── slide_01.png
        │   └── ...
        └── presentation.pdf
```

## Error Handling

- **Rate Limits**: Reduce `--max-concurrent` to 2
- **Failed Slides**: Use `--slides` to regenerate specific ones
- **Connection Error**: Check proxy settings, script auto-retries (max 3, exponential backoff)

For detailed script API reference, see [references/REFERENCE.md](references/REFERENCE.md).
