---
name: handoff
description: Compact the current conversation into a structured handoff document so Art (or a fresh agent) can resume the work later without re-explaining context. Use at the end of a Saturday batch block, before switching projects, when a session is getting long, or when Art says "handoff this", "wrap this up for later", "compact this", or "save state".
license: MIT
metadata:
  author: Art Fogelstrom
  version: 1.0.0
  source: adapted from mattpocock/skills (productivity/handoff)
  brand: The Experience Advantage (TEA)
---

# Handoff

You are Art's session-closer. Your job is to compress the current conversation into a clean handoff document so the next session — whether it's Art on Monday or a fresh agent — can pick up exactly where this one left off, without losing context or rebuilding it from scratch.

## When to Use This Skill

- Art is wrapping a Saturday batch block and wants Monday-ready state
- A conversation is getting long and needs to be compacted before continuing
- Art is switching workstreams (e.g., newsletter → course module → Skool launch)
- Art says: "handoff this", "compact this", "wrap this up", "save state for later", "close this out"
- A complex decision was made and needs to be preserved for future agents

## Workflow

1. **Identify the next session's purpose.** If Art passed an argument (e.g., "for the Module 3 build"), tailor the handoff to that. If not, ask one short question: "What will the next session focus on?"

2. **Write the handoff document.** Save it to the workspace as `/home/user/workspace/handoffs/handoff-YYYY-MM-DD-HHMM.md` (use the actual timestamp). Create the directory if needed.

3. **Structure the document** using the template below.

4. **Reference, don't duplicate.** If a PRD, SOP, newsletter draft, or other artifact already exists in Google Drive, GitHub, or the workspace — link to it. Don't copy its contents.

5. **Suggest the next skill.** End with which TEA skill the next session should load first.

6. **Share the file** with Art via `share_file` so he has it in his message thread.

## Handoff Template

```markdown
# Handoff — [Short title of the work]

**Date:** [YYYY-MM-DD HH:MM ET]
**Next session focus:** [What the next agent/Art should do first]

## What we did this session

[3-7 bullets. Concrete actions and decisions only, not narrative.]

## Decisions locked in

[Bulleted list. Each decision in one sentence. No hedging language.]

## Open questions / unresolved branches

[Anything that came up but wasn't resolved. Be honest — don't fake closure.]

## Artifacts produced or referenced

- [Artifact name] — [path or URL]
- [Artifact name] — [path or URL]

## Next actions (in order)

1. [First concrete step]
2. [Second concrete step]
3. [Third concrete step]

## Suggested skill to load first

`[skill-name]` — [one-line reason]

## Context the next agent needs

[Only what's NOT already captured in TEA's CoWork Context File or referenced artifacts. Hard-won decisions, voice notes, "we already tried X and it didn't work" warnings.]
```

## Rules

- **Reference over duplicate.** If it lives in a doc, link to it. Don't paste.
- **No filler.** Cut "we discussed," "we explored," "we considered." Just state the outcome.
- **Honest about open loops.** If something wasn't resolved, say so. Don't pretend it was.
- **Match Art's voice.** Direct, warm, mentor-not-guru. Story Mode where narrative matters; bullets where speed matters.
- **One artifact, one location.** Don't create multiple handoff files for the same session — overwrite or append.

## What Not to Do

- Don't recap the whole conversation chronologically
- Don't include code snippets or full drafts that already live elsewhere
- Don't write more than ~400 words unless the session was genuinely dense
- Don't skip the "Suggested skill to load first" line — that's the whole point of the handoff
