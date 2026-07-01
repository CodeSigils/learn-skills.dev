---
name: design-system-extractor
description: Extract, audit, and document design systems from existing product UI, screenshots, Figma-like specs, codebases, component libraries, CSS, design tokens, mobile apps, web apps, dashboards, and marketing pages. Use when turning inconsistent UI into reusable tokens, components, patterns, spacing, typography, color, motion, accessibility, and product craft rules.
---

# Design System Extractor

Use this skill to turn scattered UI into a coherent design system an agent can reuse.

## Workflow

1. Identify source surfaces, product type, platforms, brand constraints, and target consumers of the system.
2. Read `references/design-system-extraction-systems.md`.
3. Inventory tokens, components, states, layout patterns, content patterns, motion, accessibility, and exceptions.
4. Normalize into canonical names and separate primitives from product-specific components.
5. Produce a design-system map with gaps, duplicates, migration plan, and validation checks.

## Guardrails

- Do not invent a new system when the task is to extract the existing one.
- Do not collapse meaningful product variants into one generic component.
- Do not ignore accessibility states, error states, density, responsive behavior, or motion.

## Output format

```text
Source surfaces:
System shape:

Tokens:
- color / type / spacing / radius / elevation / motion

Components:
- <component> -> variants, states, usage, gaps

Inconsistencies:
- <issue> -> recommended canonical pattern

Migration plan:
- quick wins / systematic fixes / open questions
```
