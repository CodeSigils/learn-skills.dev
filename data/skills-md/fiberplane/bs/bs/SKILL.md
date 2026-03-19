---
name: bs
description: Generate rich visual plans with diagrams and structured layouts, then publish to a shareable URL. Triggers on "brainstorm", "bs", or "create a plan".
---

# bs — brainstorm

# Purpose
Generate self-contained plans that are visually rich, structurally clear, and publishable to a shareable URL.

# Authentication

Before publishing, read the user's fp token so plans are associated to their account:

```bash
FP_TOKEN=$(grep -m1 'token' ~/.fiberplane/credentials.toml 2>/dev/null | sed 's/.*= *"\(.*\)"/\1/')
```

- If `FP_TOKEN` is non-empty, include `-H "Authorization: Bearer $FP_TOKEN"` on all publish/update/delete requests.
- If the file is missing or the token is empty, fall back to anonymous publishing (plans expire after 3 days).
- Authenticated plans are permanent, editable, and visible in the user's console at app.fp.dev.

# Guidelines
- Use Mermaid diagrams for architecture, flows, and sequences.
- Use structured layouts (cards, tables, file trees) for information density.
- Always include a "Publish" step to generate a shareable URL.
- Ensure the plan is self-contained (all CSS/JS inlined).
- Follow the design language: Instrument Serif headers, Spline Sans Mono body, and electric orange accents.
- Be concise and focus on visual structure over large blocks of text.
