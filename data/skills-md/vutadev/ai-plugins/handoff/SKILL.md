---
name: handoff
description: Compact the current conversation into a project-local or global handoff document for another agent to pick up. Use when the user asks to create a handoff, preserve session context, or prepare the next agent; supports --project and --global destination flags.
---

# Handoff

Write a handoff document summarizing the current conversation so a fresh agent can continue the work.

## Destination

Default to project mode.

- `--project`: Save the document under `.agents/handoff/` in the current project.
- `--global`: Save the document under `~/.agents/handoff/`.
- No flag: Use project mode.

If both `--project` and `--global` are present, ask the user which destination to use before writing.

Create the destination directory if it does not exist. Name the file with a stable, readable Markdown filename such as `handoff-YYYYMMDD-HHMMSS.md`, adding a short slug from the user's focus argument when helpful.

Include a "suggested skills" section in the document, which suggests skills that the agent should invoke.

Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments other than `--project` or `--global`, treat them as a description of what the next session will focus on and tailor the doc accordingly.
