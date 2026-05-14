---
name: html-artifact
description: Create polished, human-readable single-file HTML artifacts from supplied content, plans, specs, reports, reviews, notes, datasets, or explanations. Use when the user asks to make an HTML file/artifact, convert dense information into readable HTML, visualize content, make a spec/report/plan/review easier to read, or produce an interactive throwaway HTML surface for understanding or editing information. This skill is for artifacts, not websites or landing pages.
---

# HTML Artifact

Create a finished HTML artifact that a human will read, scan, share, or interact with. Treat HTML as a visual thinking surface, not as a prettier Markdown renderer and not as a marketing website.

Before writing code, read `references/visual-systems.md`.

## Core Workflow

1. Identify the artifact's job: explain, compare, plan, review, report, map, prototype, edit, triage, or summarize.
2. Infer the reader's goal: what should they understand, decide, inspect, or change after opening the file?
3. Choose a visual system: tone, density, typography, palette, layout rhythm, diagram style, and interaction level. Commit to it boldly.
4. Transform the content into the clearest visual structure. Use sections, grids, diagrams, tables, timelines, annotations, callouts, tabs, filters, code panes, or editors as appropriate.
5. Write a complete, self-contained HTML file with inline CSS and JavaScript unless the user asks for a multi-file output.
6. Preserve all decision-critical content. Remove filler, repetition, generic AI phrasing, and throat-clearing.
7. Deliver the file path and a concise note about what the artifact contains.

## Artifact Principles

- Design for a person reading once, not an agent parsing text.
- Start with the artifact's actual purpose, not a generic hero section.
- Make the artifact feel designed, not merely styled. Use strong typography, color, spatial composition, and visual devices with confidence.
- Prefer visual hierarchy over long prose: make the main point obvious within seconds.
- Use rich HTML affordances when they help: sticky summaries, side-by-side comparisons, annotated snippets, swimlanes, matrices, dependency maps, expandable details, copy buttons, toggles, and lightweight controls.
- Avoid box-first layout. Reach first for editorial composition, rails, timelines, bands, annotations, diagrams, tables, connected flows, and canvas-like spatial grouping.
- Make interactive controls real. If a button, tab, slider, filter, or copy action appears, it must work.
- Keep the artifact portable. Avoid build steps, frameworks, package installs, tracking scripts, and fragile external dependencies.
- Use semantic HTML where practical, responsive CSS, and readable contrast.
- If source content is long, keep it complete through structure: summaries, anchors, grouped sections, appendices, or progressive disclosure.

## Output Rules

- Produce actual HTML code/files, not a description of what the HTML would contain.
- Do not leave placeholders, TODOs, ellipses, skipped sections, or "repeat for the rest" comments.
- Do not invent data, people, tickets, metrics, citations, or examples unless explicitly asked. If a visual needs sample data, label it clearly as sample.
- Do not ask the user to choose style options unless the missing choice would materially change the artifact. Make a tasteful default decision.
- Do not open or verify the artifact in a browser unless the user specifically asks.
