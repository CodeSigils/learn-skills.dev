---
name: markdown-formatting
description: >-
  Use this skill whenever creating or editing any markdown file. Do not wait
  for an explicit request — if a markdown file is being created or edited,
  this skill applies.
---

## General

- No table of contents unless specifically requested.

## Code Blocks

All code blocks must include a language tag and a Torchlight flag.

| Flag           | Description                           |
| -------------- | ------------------------------------- |
| `+code`        | Source code only (syntax highlighted) |
| `+demo`        | Preview + code (always visible)       |
| `+demo-folded` | Preview + code + collapsible          |

Other flags (`+preview`, `+collapse`, `output`) exist but are less common — only use when requested.

### Language Tags

| Use For                         | Tag                     |
| ------------------------------- | ----------------------- |
| Directory trees, shell commands | ` ```bash +code `       |
| Blade templates                 | ` ```html +code-blade ` |

### Demo-Folded Attributes

When using `+demo-folded`, apply demo attributes intentionally:

- `class="..."` — outer demo wrapper styling
- `preview-class="..."` — preview-only layout or styling

Example opening tag:

```markdown
```html +demo-folded class="bx" preview-class="grid gap lg:cols-3"
<div class="example">Content here</div>
```

## Horizontal Rules

Use 80 hyphens as a visual section separator in long documents when a `---` thematic break is not appropriate:

`--------------------------------------------------------------------------------`

## Lists

- Use hyphens `-` for unordered lists
- Use `1.` `2.` for ordered steps
- 4-space indentation for nested items

## Tables

Standard GitHub Flavored Markdown. Keep column separators aligned.

| Column | Type         | Nullable | Default |
| ------ | ------------ | -------- | ------- |
| id     | bigint       | No       | AUTO    |
| name   | varchar(255) | No       | -       |

## Linting

- Blank line before and after headings, code blocks, and lists
- No trailing spaces
- Single blank line between sections — not double
