---
name: youtube-title-generator
description: "Generate 3–5 strong, A/B-testable YouTube video titles for videos in ANY niche — tech, business, fitness, food, finance, lifestyle, education, entertainment, story/personal, or 'cool thing I found' roundups. Use this whenever the user wants titles or a name for a YouTube video — including phrases like 'title for my video', 'YouTube titles', 'title ideas', 'help me name this video', 'what should I call this', or when they hand over a topic, script, bullet points, or a draft title and want title options. Trigger even if the user doesn't say the word 'title' explicitly (e.g. 'what should I call this video about my marathon training')."
---

# YouTube Title Generator

Generate a small set of high-CTR, A/B-testable YouTube titles. Each option pulls a **different psychological lever** so the user learns which *idea* wins, not just which wording.

Works for **any niche** — tech, business, fitness, food, finance, lifestyle, education, entertainment, and beyond. Also handles **story/personal** videos and **"cool thing I found"** roundup videos.

## Workflow

1. **Read the input and classify it.** The user will give you one of:
   - **A topic / one-liner** — e.g. "video about the new Claude model." Thin input. Make reasonable assumptions; ask **at most one** quick clarifying question only if the video's angle is genuinely unclear (e.g. is this a review, a tutorial, or a reaction?). Prefer proceeding over interrogating.
   - **A rough or finished script / bullet points** (may come from the shortform-script skill). Rich input. **Mine it** for the single sharpest hook, surprising claim, number, or emotional beat — the titles should reflect what's actually in the video.
   - **A draft title they already have.** Riff around it: keep what works, generate stronger variants across different strategies. Don't just reword it.
   - **A competitor's title to beat** (if offered). Identify why it works, then out-angle it.

2. **Identify the video type** (tech, story/personal, or app-roundup). This constrains which strategies fit — see below.

3. **Generate 3–5 titles, each on a DIFFERENT strategy.** Spread across levers; never cluster 4 titles on the same angle. Pick the strategies that fit *this* video.

4. **Apply the hard rules** (length, honesty, formatting) to every title.

5. **Output** the table + ranked shortlist (format below).

## The strategy levers

Label each title with the lever it pulls. Choose the ones that fit the video:

| Label | What it does | Example |
|---|---|---|
| **Curiosity** | Opens a gap the viewer needs closed | "Nobody's talking about what GPT-5 just did" |
| **Bold Claim** | High-stakes assertion / consequence | "This AI tool makes Photoshop obsolete" |
| **How-To** | Concrete value / outcome | "How I automate my whole week with 3 AI tools" |
| **Listicle** | Numbered, scannable, collectible | "7 free AI sites that feel illegal to know" |
| **Contrarian** | Skeptic / myth-buster / "so you don't have to" | "I tried the viral AI app so you don't have to" |
| **Story** | Personal narrative, tension, stakes | "The night my side project almost broke me" |

Guidance by video type:

- **Informational / how-to / review (any niche):** Curiosity, Bold Claim, How-To, Listicle, Contrarian all fair game. Lean on the niche's native patterns — "X just killed Y," benchmark/"vs" framings, "the [thing] nobody's using yet," or whatever the audience already recognizes.
- **Roundup / recommendations:** Favor Listicle, Curiosity, and Bold Claim ("value" framings like "free," "underrated," "feels illegal to know").
- **Story / personal:** Lead with Story and Curiosity. Do **not** force a Listicle or a spammy Bold Claim onto a narrative video — it reads fake.

## Hard rules (apply to every title)

- **Length ~60 characters.** YouTube truncates around 60 chars on desktop and even earlier (~40) on mobile/sidebar. **Front-load the hook** so it survives truncation. Show the character count for each title.
- **Honesty check — no clickbait the video can't cash.** Every promise must be delivered by the actual content. A title that overpromises tanks retention and hurts the channel. If the input doesn't support a bold claim, don't manufacture one.
- **Formatting norms:**
  - Title Case.
  - Brackets/parens for context tags are good: `(free)`, `[2026]`, `(no code)`, `(honest review)`.
  - Emoji only when it fits the creator's style — sparing, never more than one, never required.
  - No ALL-CAPS words except at most one single-word emphasis, used rarely.
  - Avoid vague filler ("Amazing new thing you must see").

## Thumbnail pairing

For each title, suggest **2–4 punchy words of thumbnail text** that *complement* the title without repeating it. Title + thumbnail work as a combo: if the title asks a question, the thumbnail can tease the stakes; if the title is a claim, the thumbnail can name the subject. Example — title "This AI Tool Makes Photoshop Obsolete" → thumbnail text "RIP Photoshop?"

## Output format

First, a scannable table:

```
| # | Title | Strategy | Chars | Thumbnail text |
|---|-------|----------|-------|----------------|
| 1 | ...   | Curiosity| 52    | ...            |
```

Then a short **ranked shortlist**:

> **Test these first:**
>
> 1. **[Title]** — one line on why it's the strongest bet for this audience/video.
> 2. **[Title]** — one line.
> 3. *(optional third)* — one line.

Rank on: hook strength, clarity within the char limit, and fit with the video's actual content. Recommend the top **2–3** to A/B test — that's the deliverable. Keep the reasoning to one line each; don't write a paragraph per title.

## Notes

- Default to **5 options** when the video supports varied angles; drop to 3 if the video is narrow (a simple tutorial doesn't need a contrarian and a story angle forced on).
- Keep the whole response tight and copy-paste friendly. The user is choosing fast and shipping.
