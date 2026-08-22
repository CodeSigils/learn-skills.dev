---
name: structured-data
description: Designs and validates JSON-LD structured data for rich result eligibility. Use when adding schema, fixing rich result errors, or combining entities with @graph.
---

# Structured Data

## Overview

Emit valid JSON-LD that matches visible content and Google’s guidelines.

## When to Use

- Adding/fixing schema; rich result eligibility work

**Not for:** Guaranteeing rich results (eligibility ≠ serving).

## Official sources

- https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
- https://developers.google.com/search/docs/appearance/structured-data/sd-policies

## Process

1. Pick types that match the page (Article, Product, BreadcrumbList, Organization, etc.).
2. Prefer JSON-LD; use `@graph` for multiple entities.
3. Ensure every claimed property is visible/accurate on the page.
4. Run `python skills/structured-data/scripts/schema_audit.py <url-or-file>`.
5. Validate with Rich Results Test when possible.
6. See skill `references/` for common type notes and `references/structured-data-checklist.md`.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Any schema type boosts rankings." | Markup enables eligibility; it does not guarantee rich results or rankings. |
| "Invisible claims in JSON-LD are fine." | Markup must match visible content per Google guidelines. |
| "I will validate later." | Broken JSON-LD ships silent failures — parse and test before publish. |

## Red Flags

- Inventing ranking factors not documented by Google
- Skipping verification ("looks fine")
- Advising spammy shortcuts (cloaking, doorways, link schemes)

## Verification

- [ ] JSON-LD parses
- [ ] Types appropriate; required properties present
- [ ] Markup matches visible content
- [ ] Checklist reviewed
