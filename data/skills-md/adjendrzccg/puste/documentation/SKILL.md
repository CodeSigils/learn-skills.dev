---
name: documentation
description: "Generate and update project documentation under docs/. Uses Mermaid for diagrams. Invoked explicitly when the user requests documentation work."
---

# Documentation Generation Skill

## Purpose

Generate, update, and maintain documentation files under `docs/`. This skill ensures consistency with existing project conventions, structure, and formatting patterns.

## Audience

The documentation targets **developers and engineers working on the project**. It serves as a reference and knowledge source for understanding the codebase, architecture, flows, and conventions. Write with the assumption that the reader has development experience but may be new to this project.

## When to Use

- User explicitly asks to create, update, or review documentation
- User asks to document a new feature, flow, model, or architectural decision

## Documentation Structure

All documentation lives under `docs/`, organized by domain subfolders. The folder structure evolves over time — always check the current state of `docs/` before creating or updating files. `docs/README.md` serves as the main index and must be updated when adding new documentation areas.

## Conventions

### Formatting Rules

- **Headings**: `#` for title (H1), `##` for sections, `###` for subsections
- **Tables**: Use markdown tables for comparisons, feature matrices, config layers
- **Code blocks**: Triple backticks with language tag (`python`, `json`, `bash`, `mermaid`)
- **Inline code**: Backticks for variable names, file paths, CLI commands
- **Links**: Relative markdown links — `[Display Text](relative/path.md)`
- **Lists**: Bullet points for descriptions, numbered lists for sequential steps
- **No emojis** in documentation content
- **Short and concise** — keep docs brief, avoid verbose explanations and filler words

### Structure of a Documentation File

Every doc file should follow this pattern:

1. **H1 title** — short, clear name
2. **Overview section** — 1–3 sentences explaining the purpose
3. **Detail sections** — organized with H2/H3 headings
4. **Tables** — for structured comparisons or reference data
5. **Last updated** — every doc file must end with a "Last Updated" line at the bottom, formatted as: `*Last updated: YYYY-MM-DD*`
   - When creating a new doc, add the current date
   - When updating an existing doc, update the date to the current date

### Diagrams

- Use **Mermaid** for all diagrams — flowcharts, sequence diagrams, C4, etc. (embed in fenced code blocks with `mermaid` tag)
- Use **ASCII text diagrams** for simple layered architectures
- **Do not use PlantUML** for new diagrams

### Code Examples

- **Avoid specific code examples from the codebase** — code changes frequently and concrete examples become outdated quickly
- Prefer describing patterns and conventions in prose or pseudocode
- Only include code snippets when they illustrate a stable API or convention unlikely to change

## Workflow

1. **Read existing docs** in the target domain folder before writing — match tone and depth
2. **Check `docs/README.md`** — if adding a new documentation area, update the index
3. **Place the file** in the correct domain subfolder
4. **Follow the conventions** listed above
5. **Cross-reference** related docs with relative links where helpful
