---
name: storytelling
description: "Plan presentations using the Storytelling Canvas framework — from raw content to a complete slide-by-slide blueprint with speaker scripts and visual evidence notes. Use this skill whenever the user wants to plan a presentation, create a slide deck outline, structure a pitch, design a talk, write presentation scripts, or prepare content before generating slides. Also triggers on: '/storytelling', 'วางแผน presentation', 'ทำ slide plan', 'plan slides', 'presentation outline', 'pitch deck plan', 'เตรียม slide', 'วางโครง presentation'. Use this even when the user just says 'I need to present X' or pastes content and says 'turn this into slides'. This skill creates the storytelling plan — the actual slide generation happens via /gslide afterward."
---

# Storytelling — Presentation Planning Skill

Turn any content into a structured presentation plan with speaker scripts and visual evidence notes. Built on the Storytelling Canvas framework (Kernbach) and slide design principles (Duarte, Reynolds, Alley).

## What This Skill Produces

A `storytelling.json` file containing:
1. **Presentation Blueprint** — shared context for the entire deck (topic, audience, goal, style)
2. **Per-Slide Plan** — for each slide: headline, speaker script, visual evidence, and story metadata

This file is a format-agnostic content plan — usable by `/gslide`, social media skills, TikTok scripts, or any other output format.

## Workflow — 6 Steps

### Step 1: Receive Content

Accept content from any source:
- User types/pastes directly
- Reference to a NotebookLM notebook
- File path to a document
- URL

Read or gather the raw content. Don't ask the user to restructure it — that's your job.

### Step 2: Clarify (ask only what's missing)

Check what information you already have from the content and conversation. Only ask for what's genuinely missing. Never ask more than 3 questions at once.

**Required inputs (must have before proceeding):**

| Field | Why it matters |
|---|---|
| **Audience** | Determines vocabulary, depth, emotional appeals |
| **Goal (Before → After)** | What should the audience think/feel/do differently after? |
| **Duration** | Determines slide count (~1-2 min per slide) |

**Optional inputs (use smart defaults):**

| Field | Default if not specified |
|---|---|
| Tone | "professional" |
| Visual style | "flat vector, clean minimal" |
| Color palette | "navy + accent on white" |
| Language | Same as input content |

If the user gives a brief like "pitch to investors, 10 min" — you already know audience (investors), goal (get funding), duration (10 min). Don't re-ask. Just confirm your interpretation.

### Step 3: Create Presentation Blueprint

Synthesize everything into a per-presentation blueprint. Read `references/storytelling-canvas.md` for the full framework, but here's the core:

```
Presentation Blueprint
──────────────────────
Topic:          [what it's about]
Audience:       [who + what they care about]
Goal:           Before: [current state]
                After:  [desired state]
One Big Idea:   [single sentence — the thesis]
Storyline:      [Report / Explanation / Pitch / Drama]
Sparkline:      [What Is ↔ What Could Be pattern]
Slide Count:    [derived from duration]
Style:          [visual style]
Colors:         [primary / accent / background]
Tone:           [professional / casual / inspiring]
```

**Choosing the storyline type:**
- **Pitch** — user wants approval, budget, buy-in → alternate what-is/what-could-be
- **Explanation** — user wants to teach or inform → progressive complexity
- **Report** — user presents findings/results → data-driven narrative
- **Drama** — user tells a story to inspire → classic hero's journey arc

Show the blueprint to the user for confirmation before proceeding.

### Step 4: Generate Slide Plan

Create a slide-by-slide plan as a table. Read `references/slide-design.md` for detailed guidance on slide types and sequencing.

**Recommended structures by storyline type:**

For **Pitch** (most common):
```
Title → Problem → Data → Unexpected → Divider →
Solution → Process → ROI → S.T.A.R. → Comparison →
Reward → CTA
```

For **Explanation**:
```
Title → Agenda → Concept 1 → Example → Concept 2 →
Example → Concept 3 → Example → Synthesis → Takeaway
```

For **Report**:
```
Title → Executive Summary → Finding 1 → Finding 2 →
Finding 3 → Comparison → Implications → Recommendations → CTA
```

**Display as a table:**

```
| #  | Type      | Story Role       | Sparkline   | Headline (assertion)                 | ⏱   |
|----|-----------|------------------|-------------|--------------------------------------|------|
| 1  | Title     | Opening          | —           | [presentation title]                 | 30s  |
| 2  | Problem   | Start with Why   | What Is     | [full-sentence assertion 8-14 words] | 90s  |
| ...| ...       | ...              | ...         | ...                                  | ...  |
```

**Rules for the plan:**
- **Every headline — including title, divider, and CTA slides — must be a full-sentence assertion** (Alley model) of at least 20 Thai characters or 8 English words. Not a topic label, not a single phrase. Even the title slide needs a full sentence: "IFCG Digital Transformation: ลงทุนวันนี้เพื่อเติบโตอย่างยั่งยืนพร้อมรับอนาคต" not "IFCG Digital Transformation". Even a divider: "ถึงเวลาเปลี่ยนแปลงครั้งสำคัญที่สุดของ IFCG" not "ถึงเวลาเปลี่ยน"
- Each slide has exactly **one idea**
- Alternate between dense slides (data/process) and breathing slides (quote/divider/image) — never more than 3 dense slides in a row
- Total time must fit within the stated duration (use the 80% rule — plan for 80% of available time)

Ask the user: "แก้ไขอะไรไหม? เพิ่ม/ลด/สลับ slide ได้เลย" and iterate until they approve.

### Step 5: Generate Per-Beat Details

Once the plan is approved, generate full details for every beat. Each beat has **2 layers**:

#### Layer 1: Briefing (for humans)

```
Core Takeaway:  [1 sentence — if the audience forgets everything, they remember this]
Transition IN:  [sentence connecting from previous beat — needed for every beat except the first]
Script:         [what the presenter/author says — at least 100 Thai characters or 50 English words,
                 even for short beats like dividers and CTAs. Complement, not duplicate the content]
Transition OUT: [sentence setting up the next beat — needed for every beat except the last]
```

**Why transitions matter:** Each beat must flow into the next — without transitions, the story feels like disconnected information. The transition_in reminds the audience where they are; the transition_out creates anticipation for what comes next. Beat 1 has no transition_in (it's the opening). The last beat has no transition_out (it ends with the CTA).

Every beat needs a script, even short ones. A divider beat still has a spoken line that carries the audience across the arc.

Read `references/storytelling-canvas.md` Section "SUCCESS Formula" for how to craft each script based on the beat's story role.

#### Layer 2: Beat Spec (format-agnostic)

```
SUCCESS Element:[which element of the Canvas this beat addresses:
                 simplicity / unexpectedness / concreteness / credibility / emotions / storyline / star_moment
                 — null for opening, divider, reward, and CTA beats]
Visual Evidence:[what should be shown to support the headline — described as content intent,
                 not as a prompt. e.g. "bar chart comparing 3 competitors" not "flat vector infographic"]
Emotional Tone: [alarming / confident / curious / relieved / inspiring / shocking / nostalgic]
Duration:       [seconds — pacing guide for delivery, not tied to any format]
```

**Why SUCCESS element matters:** The middle section of a story must cover all dimensions of the Canvas — Simplicity, Unexpectedness, Concreteness, Credibility, Emotions. Tagging each beat keeps the story balanced and prevents over-indexing on one type (e.g., 5 data slides in a row).

**Show progress to the user** as you generate:
```
กำลังสร้างรายละเอียด 12 beats...
✅ Beat 1/12 — Opening
✅ Beat 2/12 — Common Ground
...
```

### Step 6: Save storytelling.json

Write the complete output to `storytelling.json` in the current working directory.

**Schema:**

```jsonc
{
  "canvas": {
    // — General Conditions (Kernbach) —
    "topic": "string",
    "audience": "string",
    "audience_type": "doer | supplier | influencer | innovator",
    "audience_analysis": {
      "before": {
        "think": "string — what they currently believe",
        "feel": "string — how they currently feel",
        "know": "string — what they currently know",
        "want": "string — what they currently want to do"
      },
      "after": {
        "think": "string — what they should believe",
        "feel": "string — how they should feel",
        "know": "string — what they should know",
        "want": "string — what they should want to do"
      }
    },
    "goal": {
      "before": "string — summary of audience state before",
      "after": "string — summary of desired state after"
    },
    "one_big_idea": "string — single thesis sentence, the one thing they must remember",
    "common_ground": "string — shared experience or vision between presenter and audience",

    // — Story Architecture —
    "storyline": "pitch | explanation | report | drama",
    "plot_type": "man_in_a_hole | rags_to_riches | cinderella | icarus | riches_to_rags | oedipus",
    "conflict_type": "self_vs_self | self_vs_others | self_vs_environment",
    "sparkline_type": "what_is_vs_what_could_be | progressive | data_driven | hero_journey",
    "star_moment_index": "number — index of the S.T.A.R. moment beat",

    // — Ending —
    "reward": {
      "personal": "string — how the audience personally benefits",
      "sphere": "string — how it benefits people around them",
      "humanity": "string — how it contributes to something larger"
    },

    // — Delivery —
    "tone": "string",
    "duration_minutes": "number",
    "beat_count": "number",
    "language": "string"
  },
  "beats": [
    {
      "index": 1,
      "type": "opening | common_ground | problem | data | star_moment | divider | solution | process | roi | comparison | reward | cta | ...",
      "story_role": "string — e.g. beginning/start_with_why, middle/credibility, end/reward",
      "success_element": "simplicity | unexpectedness | concreteness | credibility | emotions | storyline | star_moment | null",
      "sparkline_position": "what_is | what_could_be | shift | neutral",
      "emotional_tone": "string",

      "headline": "string — full-sentence assertion (Alley model)",
      "visual_evidence": "string — what should be shown to support the headline, described as content intent",
      "content": ["array of specific data/text items to include"],
      "core_takeaway": "string — 1 sentence: if they forget everything else, they remember this",

      "transition_in": "string | null",
      "script": "string — spoken words, 100+ Thai chars or 50+ English words",
      "transition_out": "string | null",
      "duration_seconds": "number"
    }
  ]
}
```

After saving, tell the user:
```
📄 Saved: storytelling.json (X beats)
👉 Next: use /gslide to generate slides, or any other output skill
```

Note: `storytelling.json` เป็น format-agnostic content plan — gslide, Facebook post skill, TikTok script skill หรือ skill ใดก็ได้รับไปเป็น context แล้วตีความสู่ output format ของตัวเอง

## Important Principles

**On headlines:** Every slide headline is a full-sentence assertion (Michael Alley's model). "ต้นทุนซ่อนเร้นสูงถึง 1.2 ล้านต่อปี" not "ต้นทุน". This is backed by research — audiences understand and remember assertion headlines significantly better than topic labels.

**On content density:** Follow the Glance Test (Nancy Duarte) — if someone can't grasp the slide's point in 3 seconds, there's too much on it. Max 30 words of text per slide. Use visual evidence instead of bullet points.

**On emotional arc:** Stories that just dump information are forgettable. The Sparkline pattern (Duarte) alternates between "what is" (current reality, problems) and "what could be" (vision, solutions). This tension and resolution keeps the audience engaged and makes the final vision feel earned. For Pitch storylines, this is essential — tag each beat's `sparkline_position` carefully to maintain the rhythm.

**On SUCCESS elements:** The middle section of a story must cover all 7 elements of the Canvas (Simplicity, Unexpectedness, Concreteness, Credibility, Emotions, Storylines, S.T.A.R. moment). Tagging each beat keeps you honest — if you look at your `success_element` tags and see only "data/credibility" beats, the story is too dry. Balance information with emotion.

## Reference Files

Read these when you need deeper knowledge:

| File | When to read |
|---|---|
| `references/storytelling-canvas.md` | Step 3 (blueprint) — for SUCCESS formula, story roles, audience types |
| `references/slide-design.md` | Step 4 (plan) — for slide types, sequencing, layout patterns, timing |
