---
name: skill-orchestrator
description: Discover HeyEddi skills, load the catalog, and suggest which @skills to invoke for the current task. Use at session start, ambiguous requests, multi-skill pipelines, or when the user asks what skills are available. Reads skill-routing.json from @product-translator when present.
version: 1.1.0
---

# Skill Orchestrator

Routes work to the right HeyEddi skill — without loading every SKILL.md at once.

## When to use

- Session start on a HeyEddi project (`.heyeddi/` present or greenfield app request)
- User asks "what skills do we have?" or "which skill should handle this?"
- Before a multi-step pipeline (intake → scaffold → design → handoff → QA)
- After `@product-translator` — confirm `skill-routing.json` before downstream work

## Limits (Cursor)

Cursor **cannot** inject all skill bodies automatically. This skill:

1. **`write_skills_index`** — scan once → `.heyeddi/skills-index.json` + `skills-index.md`
2. **`load_catalog`** — read the cached index (rescan with `--refresh` after skill installs)
3. **`suggest_skills`** — ranked matches from index entries (+ `skill-routing.json` when present)
4. **You** — read **one** chosen skill's `SKILL.md`, then invoke it

## Pipeline

```
write_skills_index        → .heyeddi/skills-index.{json,md}  (session start / after installs)
read skills-index.md      → quick catalog without opening every SKILL.md
suggest_skills            → ranked @skills for this task
read one SKILL.md         → follow that skill's pipeline
```

If `.heyeddi/docs/intake/skill-routing.json` exists (from `@product-translator`), **follow route order** — suggestions surface it at score 100.

## Instructions

1. **Session start:** `write_skills_index --project-root <root>` (or `load_catalog --refresh` — same effect)
2. **Quick lookup:** read `.heyeddi/skills-index.md` — no need to open every SKILL.md
3. `suggest_skills --project-root <root> --user-prompt "<request>"`  
   Or `--prompt-file USER_PROMPT.md`
4. Read **one** chosen skill's `SKILL.md` (path in index JSON), then invoke `@skill-name`
5. Re-run `write_skills_index` after `npx skills add` or hub skill updates
6. Greenfield with no `.heyeddi/product.md` → top suggestion often `@product-translator`

## Tools

| Script | Purpose |
|--------|---------|
| `write_skills_index.py` | Scan → `.heyeddi/skills-index.*` |
| `load_catalog.py` | Read index (or scan+write if missing) |
| `suggest_skills.py` | Rank skills from cached index |

## Related

- `@product-translator` — writes `skill-routing.json`
- `reference/skill-triggers.md` — how per-skill `reference/triggers.md` works (fully agnostic scoring)
