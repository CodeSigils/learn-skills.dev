---
name: visualize
description: >
  Create beautiful, self-contained HTML visualizations from any content or idea.
  Use for: slide decks, presentations, infographics, dashboards, flowcharts, diagrams,
  timelines, comparison tables, data visualizations, landing pages, one-pagers, org charts,
  mind maps, process flows, kanban boards, report summaries, codebase maps, software
  architecture diagrams, module dependency graphs, runtime/data-flow diagrams, or any visual
  that helps humans digest information faster. Trigger on requests like "visualize this,"
  "make a deck," "create a slide," "build an infographic," "show me a dashboard,"
  "make this visual," "map this codebase," "draw the architecture," "make layered SVG diagrams,"
  or any request to present information in a visual HTML format.
license: MIT
metadata:
  author: sting8k
  version: 1.0.0
  category: document-creation
  tags: [visualization, html, slides, dashboard, infographic, svg, codebase, architecture]
---

# Visualize

Turn an idea, text, dataset, report, plan, or explanation into a polished single-file HTML visualization.

The main file should stay lean. Put implementation details in references and read only what the task needs.

## Output contract

- Create exactly one self-contained `.html` file unless the user asks otherwise.
- Save it to `/tmp/` by default, or to the user-specified path if provided.
- Use a descriptive kebab-case filename, for example `/tmp/q4-revenue-dashboard.html`.
- Keep CSS and JavaScript inline in the HTML file. Do not create separate `.css`, `.js`, image, or asset files unless explicitly requested.
- After writing the file, open it in the browser:
  - macOS: `open <file>.html`
  - Linux: `xdg-open <file>.html`
- In the final response, include the absolute path and a clickable `file://` URL.

Example final response:

```text
Created your visualization and opened it in the browser.
Path: /tmp/team-roadmap-deck.html
URL: file:///tmp/team-roadmap-deck.html
```

## Required workflow

1. Identify the best visualization type from the user's intent.
2. Read the minimum relevant reference files from the map below.
3. Start from `references/skeleton.md`; copy the full skeleton and replace only the content placeholder.
4. For large or multi-diagram output, apply `references/generation-protocol.md`: write in chunks, with `Chunk N = Diagram N` for diagram-heavy files.
5. Apply the design system, type pattern, semantic-first diagram rules, and any needed library rules.
6. Add at least one meaningful interaction beyond theme toggle and menu when it improves comprehension.
7. Verify the output against the quality gates before responding.
8. Open the file and return its path/URL.

## Reference map

Read these files as needed:

- `references/skeleton.md` — mandatory base HTML. Start every output from this file.
- `references/design-system.md` — theming, typography, spacing, accessibility, cards, chart styling, visual polish.
- `references/types.md` — layout patterns for slide decks, dashboards, timelines, flowcharts, comparisons, data visualizations, one-pagers, mind maps, and infographics.
- `references/libraries.md` — CDN usage and integration patterns for Chart.js, D3, Reveal.js, Three.js, Leaflet, and Motion. For diagrams, prefer inline SVG/CSS; do not use Mermaid unless the user explicitly requests it.
- `references/codebase-svg.md` — high-level codebase/repository diagrams using inline SVG/CSS layered views: system context, architecture layers, module dependencies, runtime flow, and data flow.
- `references/generation-protocol.md` — chunked HTML writing protocol and semantic-first diagram generation rules. Use for large outputs, codebase visualizations, or any file with 2+ diagrams.
- `references/diagram-quality.md` — mandatory review gates for diagrams, flowcharts, architecture maps, dependency graphs, runtime flows, data flows, and decision trees.
- `references/menu.md` — hamburger menu, theme toggle, PNG download, print/PDF support.
- `references/animations.md` — CSS-first animation patterns and restrained JS helpers.
- `references/css-techniques.md` — advanced CSS/SVG techniques; use only when the task benefits from them.
- `references/eval.md` — final quality rubric and common deductions.

## Non-negotiable requirements

These are duplicated here because missing them usually breaks the generated visualization or its reviewability:

- Use `references/skeleton.md` as the starting point for every HTML file.
- Preserve the menu system from the skeleton/menu reference, including theme toggle, PNG download, and print support.
- Use class-based themes with both `.theme-light` and `.theme-dark`; do not rely only on `prefers-color-scheme`.
- Preserve these CSS custom property names: `--bg`, `--surface`, `--surface-hover`, `--border`, `--text`, `--text-secondary`, `--accent`, `--accent-secondary`, `--positive`, `--negative`, `--warning`.
- Use semantic HTML: include the skip link, `<main id="main-content">`, and multiple `<section>` elements for major content blocks.
- Keep text readable in both themes; verify contrast for all cards, charts, labels, and overlays.
- If using Chart.js, follow `references/libraries.md` and the skeleton rules: include Chart.js in `<head>`, disable default animation, keep tooltips enabled, make charts responsive, and give every canvas `role="img"` plus a descriptive `aria-label`.
- Avoid module syntax (`import`/`export`) inside generated HTML. Use browser-safe global scripts.
- For architecture/codebase diagrams, use semantic-first inline SVG/CSS instead of Mermaid so rendering is deterministic and does not depend on a graph parser.
- For any diagram, flowchart, architecture map, dependency graph, runtime flow, data flow, or decision tree, define the diagram purpose, nodes, edges, layout, visual grammar, and confidence before drawing.
- For any diagram, flowchart, architecture map, dependency graph, runtime flow, data flow, or decision tree, apply `references/diagram-quality.md` before finalizing.
- For generated HTML larger than about 15 KB or containing 2+ diagrams, write the file in chunks according to `references/generation-protocol.md`; do not write the entire file in one tool call.

## Choosing the visualization type

Use the user's goal, not only their wording:

- Presentation, pitch, lesson, narrative → slide deck.
- Metrics, KPIs, operational status → dashboard.
- Sequence over time → timeline.
- Process, architecture, decision logic → flowchart or diagram.
- Codebase, repository, software architecture, modules, packages, services → layered inline SVG/CSS graph set; read `references/codebase-svg.md`.
- Options, tradeoffs, before/after → comparison.
- Dense report or concept summary → infographic or one-pager.
- Relationships between ideas → mind map.
- Numeric trends/distribution/composition → data visualization.

If the user gives ambiguous input, pick the format that best helps a human understand it quickly. Ask only when a wrong choice would materially change the result.

## Quality bar

Before finalizing, check:

- The file opens without console-breaking syntax errors.
- The page has a clear visual hierarchy and one dominant focal point.
- The layout is responsive and does not clip important content on common laptop widths.
- Charts, labels, and legends are readable in both light and dark themes.
- Interactions are useful rather than decorative.
- The result feels specifically designed for the user's content, not like a generic template.
- Explanatory text is pedagogical and easy to follow: avoid terse fragments; use clear, complete sentences that teach the reader how to interpret the visual.
- Diagrams pass the diagram quality gates: clear purpose, readable labels, understandable arrows, consistent visual grammar, legend when needed, responsive SVG, accessibility metadata, and confidence notes for inferred content.
- Large or multi-diagram HTML files were generated incrementally and validated after chunks, so interruption can be recovered without rewriting the whole file.

Use `references/eval.md` for the full scoring rubric when doing a careful review.

## Codebase visualization defaults

When the input is a codebase or repository, do not make a single giant graph and do not use Mermaid. Produce a layered HTML visualization with 3-6 focused semantic-first inline SVG/CSS diagrams. For these outputs, use chunked writing where `Chunk N = Diagram N`. Good default views are:

1. System context.
2. Layered architecture.
3. Module/package dependency map.
4. Runtime request or command flow.
5. Data flow across storage, queues, and external APIs.
6. Build/deploy/tooling flow when relevant.

Inspect the repo enough to support the diagrams, then state confidence and open questions for anything inferred. Use a pedagogical explanation style: clear headings, short teaching notes, plain language, and complete sentences that explain why each layer matters.
