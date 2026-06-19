---
name: wiki-lint
description: Health-check and improve a repo-local wiki/ vault. Use to find stale claims, duplicate concepts or entities, orphan pages, broken Markdown links, missing routes, and pages that were consulted but did not help.
---

# Wiki Lint

Use this skill to maintain wiki quality.

## Checks

- Broken Markdown links in `wiki/`.
- `[[WikiLinks]]`, which are not allowed.
- Pages missing required frontmatter fields.
- Orphan pages with no meaningful inbound links.
- Duplicate or near-duplicate concepts/entities.
- Stale claims contradicted by newer docs, issues, code, or official sources.
- Pages that were consulted but marked unhelpful in `wiki/log.md`.
- `wiki/index.md` routes that are too broad, stale, or acting like a catalog.

## Workflow

1. Read `wiki/README.md`, `wiki/index.md`, and recent entries in `wiki/log.md`.
2. Run targeted searches, starting with:

   ```sh
   rg -n "\\[\\[" wiki
   rg -n "deprecated|stale|misleading|did not help|not useful" wiki
   rg -n "title:|created_at:|updated_at:|status:|kind:" wiki/pages
   ```

3. Inspect likely broken links and orphaned pages.
4. Propose or make focused improvements: link fixes, status changes, page merges,
   page splits, route edits, or short reflections.
5. Append a `lint` or `maintenance` entry to `wiki/log.md`.

## External Facts

For entity pages or external specifications, verify important claims against
official sources before marking a page stable.

## Quality Bar

Do not aim for a perfect graph. Aim for a wiki that makes future engineering
work faster and prevents repeated mistakes.
