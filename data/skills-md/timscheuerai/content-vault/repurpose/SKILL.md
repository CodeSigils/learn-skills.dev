---
name: repurpose
description: Take one master content piece (Notion row, transcript, video, paragraph, URL) and spin off variants across channels. Hub-and-spoke repurposing engine. Reads the source, identifies key insights / hooks / quotable moments, then creates child rows in the Notion Content DB with drafts already written by calling sub-skills (linkedin-copywriter, x-copywriter, lead-magnet-creator, etc.). Use when asked to "repurpose this", "spin off variants", "turn this into LinkedIn + X + ...", "make derivatives of this webinar / video / post", or "/repurpose".
---

# repurpose

The marketing repurposing engine. One master → N channel variants in
the Notion Content database. Hub-and-spoke, anchored on big-rock
content (webinars, talking-head videos, long-form articles).

## When to use

Trigger on:
- "Repurpose this [post / video / webinar / transcript]"
- "Turn this into LinkedIn + X variants"
- "Make derivatives of <source>"
- "Spin off variants of this"
- User explicitly types `/repurpose [source]`

Skip for:
- One-off content generation (call `/linkedin-copywriter`,
  `/x-copywriter`, `/launch-video`, `/video-use` directly)
- Editing an already-published piece (no derivative work needed)

## Inputs

The source can be:
1. **Notion row URL or ID** in the Content DB. Read its title, body,
   pillar, drive assets. The row is the master.
2. **Transcript file** (`.txt`, `.md`, `.srt`, `.vtt`). Often produced
   by `/video-use`.
3. **Video file** (`.mp4`). Run `/video-use` to transcribe first, then
   repurpose from the transcript.
4. **Pasted text** in the prompt.
5. **External URL** (web article, YouTube, etc.). Fetch + parse.

Plus targets (default: LinkedIn + X). Optional: YouTube short clip,
Newsletter, Lead Magnet, Blog (Website).

## Workflow

### 1. Read the source

If Notion row URL → `mcp__claude_ai_Notion__notion-fetch` with the row
ID. Capture: Title, Pillar, Format, page body, Drive Assets, master
URL.

If transcript / pasted text → read directly.

If video file → call `/video-use` to transcribe first, then continue
with the transcript.

If external URL → `WebFetch` to pull the content.

### 2. Extract key moments

From the source, identify:
- 3 to 5 **hooks** (sentences or punchy moments that could anchor a
  post)
- 2 to 3 **frameworks** or numbered lists (good for carousels +
  threads)
- 1 to 2 **quotable one-liners**
- The **core insight** / argument

These are inputs for the sub-skills. Stay in your voice (refer to the
corpora in `/linkedin-copywriter` and `/x-copywriter`).

### 3. Plan the cluster

Tell the user what variants you intend to create and let them prune.
Default suggestions by source type are below ("Repurposing patterns").

If the user already specified channels, skip the prompt and proceed.

### 4. Generate each variant

For each target, call the right sub-skill via the Skill tool, passing
the source context:

| Target                  | Sub-skill                |
| ----------------------- | ------------------------ |
| LinkedIn text post      | `/linkedin-copywriter`   |
| X tweet or thread       | `/x-copywriter`          |
| Lead magnet PDF         | `/lead-magnet-creator`   |
| YouTube short clip      | `/video-use` (cut from source video) |
| Synthetic motion graphic | `/launch-video`         |
| Long-form article       | manual draft (no skill yet) |

Pass each sub-skill the source context (Notion row URL or transcript
excerpt + the specific hook / framework / insight to anchor on).
Capture the draft.

### 5. Create Notion rows

For each variant, call
`mcp__claude_ai_Notion__notion-create-pages` with the Content DB data
source ID `<YOUR_NOTION_CONTENT_DB_ID>` and a page body
starting with the source link.

Per-row properties:

- **Title**: `<topic> · <Channel>` (e.g., `Outbound stack 3 Wochen · LinkedIn`)
- **Status**: `Scripting`
- **Pillar**: same multi-select as master
- **Format**: per variant (`Text` / `Video` / `Lead Magnet` /
  `Long-form Article`)
- **Channel**: per variant
- **Page body**: first line = `Source: <master row URL or external URL>`
  · then the draft

If a variant has assets (clipped video, generated PDF), upload to the
right Drive folder (e.g. `<YOUR_DRIVE_VIDEOS_FOLDER>`,
`<YOUR_DRIVE_GRAPHICS_FOLDER>`, `<YOUR_DRIVE_LEAD_MAGNETS_FOLDER>`)
and paste the Drive `viewUrl` into `Drive Assets`.

### 6. Report back

One-line summary plus the list of created rows with their Notion URLs.
Example:

```
Created 5 variants from "Outbound stack · webinar". Open the Pipeline
view (Status=Scripting):
- Outbound stack 3 Wochen · LinkedIn      → notion.so/...
- Outbound stack 3 Wochen · LinkedIn (recap) → notion.so/...
- Outbound stack · X thread               → notion.so/...
- Outbound stack · YouTube short          → notion.so/...
- Outbound stack framework · Lead Magnet  → notion.so/...
```

## Repurposing patterns (defaults)

### Webinar → cluster

| Variant               | Format             | Channel    | Source content                       |
| --------------------- | ------------------ | ---------- | ------------------------------------ |
| Pre-event promo       | Text               | LinkedIn   | Title + hook + date + registration link |
| Post-event recap      | Text               | LinkedIn   | Top 3 takeaways                      |
| Quote post            | Text               | LinkedIn   | Best one-liner from transcript       |
| Thread breakdown      | Text               | X          | Numbered list of tactics             |
| Single hot take       | Text               | X          | Most provocative one-liner           |
| Short clip            | Video              | YouTube    | 60s highlight (use /video-use)       |
| Recap article         | Long-form Article  | Website    | Full prose summary                   |
| Framework PDF         | Lead Magnet        | Website    | Distill the framework                |

### LinkedIn post → cluster

| Variant              | Format | Channel    | Notes                                |
| -------------------- | ------ | ---------- | ------------------------------------ |
| X variant            | Text   | X          | Same insight, X register             |
| X thread (if rich)   | Text   | X          | Break LI post into numbered points   |
| Newsletter blurb     | Text   | Newsletter | Same insight, more context           |

### Long-form article → cluster

| Variant              | Format | Channel    | Notes                                |
| -------------------- | ------ | ---------- | ------------------------------------ |
| 3 LinkedIn pulls     | Text   | LinkedIn   | One per key section                  |
| X thread             | Text   | X          | TL;DR breakdown                      |
| Newsletter issue     | Text   | Newsletter | Re-cut for the list                  |

### Lead magnet → cluster

| Variant              | Format        | Channel    | Notes                            |
| -------------------- | ------------- | ---------- | -------------------------------- |
| Lead magnet PDF      | Lead Magnet   | Website    | Master · use /lead-magnet-creator |
| LinkedIn promo       | Text          | LinkedIn   | "We just shipped this · grab it" |
| X promo              | Text          | X          | Same                             |
| Webinar tease        | Text          | LinkedIn   | "Live walkthrough on <date>"     |

## Cluster traceability

No Notion relation between master and derivatives (intentional ·
dumb-simple by design). Link via convention:

- First line of every derivative's page body: `Source: <master URL>`
- Pillars match the master (multi-select copied verbatim)

To find a cluster later: search Notion for the master URL string. Or
filter rows where Pillar matches and Created Date is within a few days
of the master.

If clusters become hard to track, you can add a self-relation on the
Content DB later.

## Don'ts

- **Don't auto-fan to every channel.** Suggest the defaults from the
  patterns table; let the user prune before generation.
- **Don't lose the source.** Always inject `Source: <URL>` as the first
  line of each variant's page body.
- **Don't translate verbatim across channels.** Each channel has its own
  register · the sub-skills handle that. Pass them the raw insight, not
  pre-formatted copy.
- **Don't override an existing draft.** If the master Notion row
  already has body content, surface it; don't regenerate from scratch
  unless the user asks.
- **Don't create variants without setting Status = Scripting.** They
  start in review, not scheduled.
- **Don't skip the asset upload step.** If a variant has a Drive-bound
  asset (PDF, video clip), upload it before creating the Notion row so
  the URL goes into `Drive Assets` at creation time.

## See also

- Notion Content DB data source ID: `<YOUR_NOTION_CONTENT_DB_ID>`
- Sub-skills: `/linkedin-copywriter`, `/x-copywriter`, `/launch-video`,
  `/video-use`, `/lead-magnet-creator`
