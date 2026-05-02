---
name: repurpose-talk
description: Use when you've delivered a talk and want to convert it into blog posts, social content, newsletter sections, and republishing pitches — or when you have presentation materials (slides, transcript, speaker notes) that could reach wider audiences. Produces multiple content pieces from a single talk.
---

Before doing anything else:
1. Check if `~/.devadvokit.md` exists.
2. If it does, read it silently and use it throughout this skill.
3. If it does not, stop and tell the user: "I need your DevRel context before I can run this skill. Please run /setup-devadvokit first."

---

## What NOT to Do

This skill produces outlines, angles, and frameworks — not full drafts. Specifically:

- **No full blog posts** — outlines only. Full drafts are scope creep and end up generic without heavy editing.
- **No video scripts** — that's a different skill.
- **No SEO metadata** — separate concern, different skill.

The goal is multiple content directions from one talk, not finished pieces. Editing produces the final versions.

---

## Q&A

Ask these questions one at a time. Wait for each answer before asking the next.

1. What's the talk title and abstract? (Paste or type — this is required. If you only have a title and need help with an abstract, say so and I'll help you draft one.)

2. Do you have a script, speaker notes, or transcript? Paste it here or provide a file path. This allows me to ground outputs in your actual content rather than infering from the abstract alone. If you only have the abstract, I can still work with that.

3. Who's the target audience for the repurposed content, and what's their familiarity level? (Beginner / practitioner / expert — this affects depth and terminology)

4. What tone should the repurposed content have? (Technical and depth-focused? Conversational and approachable? Thought leadership and industry perspective?)

5. What conference or event was this presented at, and when? (This gives context and provides "as I presented at X" framing for the repurposed content)

---

## Quality Gates (if transcript/notes provided)

If transcript or notes were provided, process them before generating outputs:

1. **Pull 2–3 pull quotes** — direct lines that work as standalone social copy. Memorable, quotable, out-of-context friendly.

2. **Flag demo or live content** — anything that won't translate to written formats. Note what needs adaptation or removal.

3. **Note claims needing sources** — assertions, data points, or claims requiring a source link before publishing.

If only the abstract was provided, skip this section and work from what you have.

---

## Output

Produce all of the following once the Q&A is complete and quality gates (if applicable) have been processed.

### 1. Blog post outline

H2 structure with per-section notes (not the full draft). Each section has a brief note on what it covers and the key point it makes. Grounded in the actual talk content if transcript/notes were provided.

### 2. LinkedIn post angles (5 options)

Each with a different hook strategy:
- Personal story angle
- Hot take / contrarian angle
- Data or observation angle
- Question angle (sparks discussion)
- How-to angle (practical takeaway)

Each angle should be distinct in tone and approach. Include a brief note on why this angle works for this content.

### 3. Tweet thread starters (3 options)

Opening tweet only, with a brief note on thread direction. Each starter should lead in a different way — anecdote, provocative statement, practical tip, etc.

### 4. Newsletter section

150–200 words, designed to slot into an existing newsletter. Includes a hook, key insight from the talk, and a link/call to action. Written in newsletter voice (conversational, direct).

### 5. Cold pitch paragraph

One paragraph (4–6 sentences) for republishing on a third-party publication. Includes the pitch angle, why it fits that publication's audience, and a brief credibility anchor. Grounded in the conference context ("As presented at X...").

---

## Content Library Check

Scan the content library in `~/.devadvokit.md`. If any existing content covers similar ground:

> "This overlaps with [title] ([year]) — consider cross-linking or positioning as an update / deeper dive."

If nothing overlaps, omit this section entirely.

---

Before presenting any output, read `../../shared/ai-antipatterns.md` and silently rewrite any flagged patterns. Do not mention this step to the user.