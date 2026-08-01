---
name: storyboard-generator
description: Generate comprehensive video script storyboards from a script or specific scenes. Use this skill when the user provides story content, a script, or a screenplay and requests a storyboard, shot list, or AI image generation prompts for a video.
---

# AI Storyboard Generator

## Overview
This skill converts a provided script or story into a well-formatted storyboard. It uses a staged, user-confirmed workflow to ensure visual style and materials meet expectations before full storyboard generation.

## References
Load the following reference files as needed during the workflow:
- `references/video-styles.md` — Visual style options (Cinematic, Dark Fantasy, Ghibli, etc.)
- `references/shot-types.md` — Shot sizes, camera movements, and transition types
- `references/scene-types.md` — Scene categories and description templates

## Workflow

### Step 1: Information Extraction

Analyze the input script and extract:
- **Video Info**: Theme, target audience, duration, resolution, aspect ratio, tone, visual style.
  - Consult `references/video-styles.md` to suggest and confirm appropriate Visual Style.
- **Characters**: Names, appearances, consistent styling.
- **Scenes**: Environments, atmospheres, and settings.
  - Consult `references/scene-types.md` for scene description vocabulary.
- **Actions & Dialogues**: What happens and what is said.

If the script does not specify Visual Style, propose 1–2 suitable options from `references/video-styles.md` and ask the user to confirm before proceeding.

---

### Step 2: Character & Scene Style Preview *(User Confirmation Required)*

Before generating the full storyboard, generate **AI prompts** for the key characters and scenes so the user can verify that the visual style and material library match expectations.

Output the following and **wait for user confirmation**:

```
## 🎨 Style Preview

### Character Prompts
For each main character, generate a standalone AI image prompt:
> [Character Name]: [Detailed visual description, clothing, art style, lighting, quality tags]

### Scene Prompts
For each key scene/environment, generate a standalone AI image prompt:
> [Scene Name]: [Environment, atmosphere, lighting, color palette, art style, quality tags]

---
✅ Please review the style above. Reply "OK" or describe any adjustments needed before I generate the storyboard.
```

Do **not** proceed to Step 3 until the user explicitly confirms satisfaction (e.g., "OK", "looks good", "proceed").

---

### Step 3: Storyboard Grid Preview *(User Confirmation Required)*

Once the user confirms the style, generate a **single AI image prompt for a composite grid image** (contact sheet style). This prompt, when fed into an AI image tool, should produce one image where each cell/panel in the grid shows a key storyboard shot — similar to a film contact sheet or manga storyboard grid.

Consult `references/shot-types.md` to plan appropriate shot types and camera movements for each panel.

Output the following and **wait for user confirmation**:

```
## 🗂️ Storyboard Grid Preview

### Shot Plan
先列出每个宫格对应的分镜说明（供用户审核）：
| 格子 | Shot # | 场景 | 景别 | 动作摘要 |
|------|--------|------|------|----------|
| 1 | Shot 1 | [场景名] | [Wide Shot] | [一句话动作描述] |
| 2 | Shot 2 | … | … | … |
…

### 🖼️ Grid Image AI Prompt
生成下方这一个 Prompt，将其输入 AI 绘图工具（如 Nano Banana Pro、即梦AI）即可生成一张宫格合图：

> A storyboard contact sheet arranged in a [N]x[M] grid layout (e.g. 3x3), [visual style, e.g. cinematic dark fantasy, hand-drawn, etc.]. Each panel is labeled with a shot number. Panel 1: [shot type] of [subject + action + setting]. Panel 2: [shot type] of [subject + action + setting]. Panel 3: … [continue for all shots]. Each panel has a thin black border, clean composition, consistent character design, [color palette], high detail, professional storyboard aesthetic.

---
✅ Please review the shot plan and grid prompt above. Reply "OK" or suggest adjustments (e.g., add/remove shots, swap angles) before I generate the full storyboard.
```

Do **not** proceed to Step 4 until the user explicitly confirms (e.g., "OK", "approved", "proceed").

---

### Step 4: Full Storyboard Generation

Once the user confirms the grid, assemble the **complete storyboard file**. This file must include ALL of the following sections — do not skip or omit any:

1. **原始剧本内容** — Paste the original input script verbatim.
2. **Video Information** — Theme, audience, duration, resolution, tone, visual style.
3. **🎨 Style Preview** *(confirmed in Step 2)* — Copy the confirmed character prompts and scene prompts in full.
4. **🗂️ Storyboard Grid Preview** *(confirmed in Step 3)* — Copy the confirmed Shot Plan table and the Grid Image AI Prompt in full.
5. **🎭 Character Descriptions** — Detailed cross-shot consistent character descriptions.
6. **🏙️ Scene & Environment Overview** — Per-scene environment and lighting descriptions.
7. **🎞️ Shot-by-Shot Storyboard** — For each shot include:
   - **Shot Details**: Shot number, type (from `references/shot-types.md`), camera movement.
   - **Action & Dialogue**: Visual action and spoken dialogue.
   - **Audio & Sound Effects**: Foley SFX and BGM.
   - **Screen Text**: Subtitles, titles, or on-screen captions.
   - **AI Prompt (Nano Banana Prompt)**: Highly descriptive prompt referencing the confirmed visual style and character/scene descriptions from Step 2.

> ⚠️ **CRITICAL**: Sections 3 (Style Preview) and 4 (Storyboard Grid Preview) MUST be written into the saved file. They were confirmed by the user in previous steps and are an essential part of the final deliverable. Do NOT only save the Shot-by-Shot section.

---

### Step 5: Pre-Save Checklist & Consistency Verification

Before writing the file, run through the following checklist. Every item must be ✅ before saving:

**Content Completeness:**
- [ ] 原始剧本内容 is included at the top.
- [ ] Video Information section is filled in.
- [ ] 🎨 Style Preview section is present, with AI prompts for **every** main character and **every** key scene.
- [ ] 🗂️ Storyboard Grid Preview section is present, with the Shot Plan table AND the Grid Image AI Prompt.
- [ ] 🎭 Character Descriptions section is present.
- [ ] 🏙️ Scene & Environment Overview section is present.
- [ ] 🎞️ Shot-by-Shot Storyboard is present with all shots fully detailed.

**Consistency:**
- [ ] Characters maintain consistent appearance (clothing, hair, expression) across all shots.
- [ ] Environments remain visually consistent with the confirmed scene prompts from Step 2.
- [ ] AI prompts in each shot reference the same visual style confirmed in Step 1.
- [ ] Audio effects logically flow and match emotional intensity.

Only after all items are checked should the file be written to `assets/`.

---

## Output

Save the final storyboard as a Markdown file to the `assets/` directory.

**File naming convention**: `storyboard_[剧本名]_[版本号].md`
- Example: `assets/storyboard_营地归途_V1.md`

The file **must** follow the structure defined in `templates/storyboard_template.md`, which requires all of the following top-level sections to be present:

| # | 必须包含的章节 | 来源步骤 |
|---|---|---|
| 1 | 原始剧本内容 | 用户输入 |
| 2 | 📋 Video Information | Step 1 |
| 3 | 🎨 Style Preview（角色 & 场景 AI 提示词）| Step 2 ✅ 用户确认后 |
| 4 | 🗂️ Storyboard Grid Preview（Shot Plan + Grid AI Prompt）| Step 3 ✅ 用户确认后 |
| 5 | 🎭 Character Descriptions | Step 4 |
| 6 | 🏙️ Scene & Environment Overview | Step 4 |
| 7 | 🎞️ Shot-by-Shot Storyboard | Step 4 |

> ⚠️ **Common mistake to avoid**: Do NOT save a file that only contains sections 1–2 + 5–7 while skipping sections 3 and 4. The Style Preview and Grid Preview are core deliverables that have already been confirmed by the user and MUST be persisted in the output file.
