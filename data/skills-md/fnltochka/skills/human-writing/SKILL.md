---
name: human-writing
description: "Write, rewrite, or edit user-facing text in the repo's preferred plain human style. Use for any prose task: docs, README sections, comments, release notes, PRDs, posts, emails, explanations, and requests to humanize or tighten text. Default to general prose rules; read references/documentation.md only for README, technical docs, usage guides, CLI/API docs, or documentation audits."
---

# Human writing

Use this whenever writing or editing prose.

This skill is not a generic "think carefully" prompt. It only records this repo's writing taste: direct, specific, low-hype, and fact-preserving.

## Default style

- Preserve the user's language unless translation is requested.
- Preserve facts, names, numbers, links, commands, paths, and API identifiers.
- Prefer plain verbs and concrete claims over polished positioning.
- Keep useful structure; do not turn everything into neat three-part lists.
- Remove assistant residue: "certainly", "here is", "of course", "I hope this helps", "in this guide", "we'll explore".
- Cut unsupported hype: "seamless", "robust", "powerful", "groundbreaking", "future-ready", "unlock", "elevate".
- Keep human texture when it helps: a caveat, aside, or maintainer sentence can stay.

## Mode

Pick the smallest useful action.

- Edit: keep structure and meaning; fix wording and rhythm.
- Rewrite: reshape the text when the user asks or the original is too tangled.
- Draft: write from scratch when the user asks for new text.
- Review: give critique instead of rewriting when the user asks whether the text is good.

For README files, technical documentation, usage guides, CLI/API docs, or documentation audits, read `references/documentation.md` before writing.

## Examples

Before: "I wanted to reach out to explore whether there might be an opportunity for us to align on the next steps."

After: "Can we agree on the next step this week?"

Before: "This update delivers a robust and seamless improvement to the export experience."

After: "Exports now keep the selected date range after you refresh the page."

Before: "This approach is designed to empower users by providing enhanced flexibility and control."

After: "This lets users choose the file before the upload starts."
