---
name: html
description: Create self-contained HTML visual explanations, reports, comparisons, proposals, audits, and previews when layout and visual structure can communicate the result better than chat alone. Use when requested or when this format clearly improves the answer; once chosen, create the artifact without asking first.
---

# HTML

Create a visual explanation, not a text answer placed inside a web page. Use layout, hierarchy, typography, color, diagrams, data displays, and interaction to make the subject easier to understand, compare, inspect, or decide on.

## Shape the explanation

Before building, identify:

- the intended reader and the decision or understanding the page should support;
- the main conclusion, recommendation, or useful takeaway;
- the evidence and source material that support it;
- the visual relationships that prose would communicate poorly.

Choose an information structure that fits the material. For example, comparisons may use aligned criteria and side-by-side options; feature proposals may combine current and proposed flows, integration points, scope, and sequencing; audits may organize findings by severity, affected area, evidence, impact, and remediation; previews may center the proposed experience and annotate its states. These are examples, not templates.

Lead with what matters, then support deeper reading. Keep facts, inferences, recommendations, and unknowns distinct. Never invent metrics, findings, source support, or certainty to complete a visual.

## Design for the subject

Adapt the visual language to the content and audience. Let the subject guide typography, density, color, composition, and tone rather than imposing a house style or default dashboard.

Use visual hierarchy to make the first view useful on its own. Prefer meaningful groupings and relationships over repetitive card grids. Use diagrams, timelines, matrices, annotated screenshots, charts, tables, code excerpts, or other forms when they clarify the material. Every prominent visual element should help explain something.

Make the page responsive and accessible in a modern Chromium-based browser. Use semantic HTML, visible focus states, keyboard-operable controls, sufficient contrast, reduced-motion support where motion appears, and text alternatives for meaningful visuals. Do not encode essential meaning through color alone.

## Use interaction to improve understanding

The default artifact may be mostly static, but interaction is useful whenever it lets the reader explore, compare, navigate, or reach an appropriate level of detail. Choose the interaction from the communication need. Examples include:

- tabs for switching among a small set of parallel views without losing context;
- filters, search, and severity controls for finding relevant items in a large audit or dataset;
- sortable tables for comparing options under different priorities;
- toggles for current-versus-proposed states, alternate scenarios, or layers of a diagram;
- sliders or adjustable inputs for showing how assumptions change costs, outcomes, or trade-offs;
- hover and focus tooltips for definitions or exact chart values where inline labels would crowd the view;
- clickable diagram nodes, callouts, or hotspots for connecting a visual overview to supporting evidence;
- `<details>` and `<summary>` blocks or accordions for optional evidence, methods, code, edge cases, and other deeper reading;
- anchor navigation, a table of contents, or a section tracker for moving through a long report;
- expand, zoom, or modal views for inspecting dense diagrams, images, and code excerpts;
- copy buttons for commands, snippets, identifiers, or recommendations the reader may need to reuse;
- charts with selectable series or time ranges for examining patterns that a single static view would hide;
- animation, step controls, or state transitions for explaining sequence, causality, or how an interface changes.

Label controls by the result they produce. Keep the main conclusion and anything needed for the primary decision available without interaction. Ensure interactive states work with keyboards as well as pointers and remain understandable when motion is reduced.

## Build the artifact

Create one self-contained `.html` file by default. Embed CSS, JavaScript, inline SVG, icons, and small data directly so the file works when opened locally. Use multiple files only when the artifact genuinely needs large assets, substantial reusable code, or an existing project structure.

Prefer native browser capabilities and small amounts of purpose-built JavaScript. Add a library only when it is absolutely neccesary and dramatically improves the explanation and can fit the artifact's delivery constraints. Never require a development server for the final output.

Keep source material traceable. Cite URLs when web sources inform the page and point to relevant local files or code locations when the explanation concerns a codebase. A polished design must not obscure gaps in the evidence.

## Inspect before delivery

When preview, browser, or screenshot tools are available, render and inspect the finished page before handing it back. Check at a normal desktop width and a narrow viewport. Fix visible overflow, clipping, broken wrapping, weak hierarchy, unreadable density, poor contrast, and controls that do not work as intended. Exercise each interaction at least once.

If visual inspection is not possible, still check the markup and scripts for obvious errors and state plainly that the page was not visually verified.

Deliver the artifact with a direct link to the file and a short summary of what it contains. Do not duplicate the full explanation in chat.
