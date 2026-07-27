---
name: explain-diff-html
description: Create a rich, self-contained interactive HTML explanation of a code change, diff, branch, or pull request. Use this whenever the user wants to understand, teach, document, or walk through a software change — its background, intuition, implementation, data flow, diagrams, or quiz-based reinforcement — even if they don't explicitly say "HTML". Trigger on requests like "explain this PR", "write up what this diff does", "make a teaching page for this change", or "help someone understand this branch". The result is saved as a dated, standalone HTML file outside the repository.
---

# Explain Diff HTML

Produce a single long-form HTML page that teaches a reader how a specified code change works. Investigate the surrounding system before explaining the diff: the page should make sense to a beginner while still giving an experienced engineer a concise path to the changed behavior.

## Workflow

1. Identify the change and its scope. Use the current checkout, diff, branch, PR metadata, or user-supplied files as the source of truth. If the target is ambiguous, infer the most likely change from the available context and state the assumption in the page.
2. Explore relevant surrounding code, tests, configuration, callers, data models, and documentation. Trace the old and new paths far enough to explain behavior, not merely file-by-file edits. Prefer checked-in examples and tests over speculation.
3. Build a narrative before writing HTML:
   - what problem or constraint motivated the change;
   - how the old system behaved;
   - the smallest useful mental model of the new behavior;
   - how the implementation realizes that model;
   - edge cases, trade-offs, and observable consequences.
4. Write the output as one self-contained HTML file with inline CSS and JavaScript. Do not depend on external fonts, CDNs, images, JavaScript packages, or network access. Save it outside the repository, preferably at `/tmp/YYYY-MM-DD-explanation-<slug>.html`, using the current date in `YYYY-MM-DD` format.
5. Validate the artifact before handing it off: confirm it exists, is a complete HTML document, contains no external asset dependencies, has working quiz interactions, and satisfies the code-block and quiz checks below. If practical, open it in a browser or use a local HTML inspection tool to catch layout or JavaScript errors.

## Required page structure

Include a clear title, a short summary, and a table of contents linking to these sections in this order:

1. **Background** — Explain only the system needed for the change. Start with an optional beginner-friendly mental model, then narrow to the exact components, contracts, and prior behavior involved.
2. **Intuition** — Explain the core idea before implementation detail. Use small concrete toy inputs and outputs. Show the old and new behavior when comparison makes the change clearer.
3. **Code** — Walk through the changes in conceptual groups, ordered by execution or dependency flow rather than arbitrary file order. Include precise file and line references when available, but do not dump the whole diff.
4. **Quiz** — Include exactly five medium-difficulty, interactive multiple-choice questions. Clicking an option must immediately show whether it is correct and explain why, including the relevant behavior or code path.

Use smooth transitions, plain language, and precise systems-oriented prose. Explain jargon on first use. Use callouts for definitions, invariants, important edge cases, and practical consequences. Keep the page readable on phones with responsive CSS. Do not use top-level page tabs; make it one continuous page (in-diagram toggles are fine — see Interactive visuals).

## Visual design (editorial / literary print)

The page must use a single warm, editorial print theme — no dark mode, no alternate palettes, no theme toggle. Think of a well-set essay or a book's title page: a warm paper background, elegant serif typography, generous whitespace, and a small number of muted, printerly accent colors that carry meaning. The mood is calm and confident; the *typography and spacing* do the work, not heavy borders or shadows. Declare these exact values as CSS custom properties on `:root` and build every color in the page from them, so nothing drifts off-palette:

```css
:root {
  /* paper & ink — a warm, printed editorial base */
  --paper:    #eae7d9; /* page background — warm cream / oatmeal */
  --panel:    #f2f0e6; /* cards, callouts, code blocks — a shade lighter than paper */
  --panel-2:  #e1ddcd; /* table stripes, insets, subtle fills */
  --ink:      #1c1d18; /* display type & headings — warm near-black */
  --body:     #3a3c34; /* body text — soft charcoal on paper */
  --muted:    #6d7168; /* secondary text, captions, small-caps labels — muted sage-gray */
  --rule:     #cfcaba; /* hairline borders and connector lines */

  /* accents — muted and print-like; used sparingly and semantically */
  --green:      #234c38; /* PRIMARY brand accent: links, dots, italic display, active states */
  --green-soft: #3d6b52; /* lighter green for tints and hovers */
  --rust:       #a24b2f; /* removed / errors / warnings */
  --gold:       #9a7b1f; /* highlights / emphasis */
  --blue:       #2f5d78; /* data-flow arrows / informational */
  --plum:       #6d3a52; /* alternate highlight */

  /* editorial tokens */
  --radius: 4px;
  --serif:  Georgia, "Iowan Old Style", "Palatino Linotype", Palatino, "Times New Roman", serif;
  --hair:   1px solid var(--rule);
}
```

Apply them consistently so color carries information rather than decoration:

- Background is `--paper`; cards, panels, and `pre` blocks sit on `--panel` (a shade lighter), with `--panel-2` for table stripes and insets. Body text is `--body`, headings and display type are `--ink`, and labels, captions, and secondary text are `--muted`. Hairlines and connector lines are `--rule`.
- `--green` is the one brand accent — hold it everywhere: links, the leading italic word of the title, section markers, diagram dots, and active states. The other accents are the "some colors": use them sparingly and semantically, keeping the mapping fixed across the whole page — `--rust` for removed/errors/warnings, `--gold` for highlights/emphasis, `--blue` for data-flow arrows/informational, `--plum` for an alternate highlight. For before/after panels, keep the old-vs-new colors identical everywhere they appear — e.g. `--rust` for old/removed and `--green` for new/added. A reader should learn the mapping once and trust it everywhere.
- Respect contrast: `--body` on `--paper` is the intended reading pair. Reserve `--muted` for genuinely secondary text — never put important content in `--muted`, and never in `--rule`.
- Because correctness must never depend on color alone (quiz feedback, added/removed lines, etc.), always pair an accent with a label, icon, or shape.

### Visual style — editorial serif

Render the whole page like a printed essay or title page, built entirely from the palette above. The look comes from a few moves applied consistently to every surface — cards, callouts, code blocks, before/after panels, tables, the table of contents, quiz cards, and diagram frames:

- **Serif everything, typography-led.** Set the whole page in `--serif`. The page title is large, tight, and mixes an *italic* leading phrase in `--green` with the rest in roman `--ink` (as in "*Rethinking* the Render Pipeline"). Headings are serif and confident (600–700); body text is `--body` at a comfortable measure (~66ch) with generous line-height (~1.7) and ample vertical rhythm between sections.
- **Quiet structure, hairlines not boxes.** Surfaces are flat: a warm `--panel` fill with a single `--hair` (1px `--rule`) border and `--radius` around 4px, and at most a whisper of shadow (`0 1px 2px rgba(20,20,15,.06)`) — never a hard, offset, or heavy shadow. Separate sections with whitespace and short, centered hairline rules rather than thick dividers.
- **Small-caps labels.** Section kickers, the TOC heading, nav-like labels, table headers, chips, badges, and the footer are UPPERCASE with wide letter-spacing (~0.16em), small, and set in `--muted` or `--green`; a middot `·` makes a nice separator for label runs (e.g. a footer breadcrumb like `BACKGROUND · INTUITION · CODE · QUIZ`).
- **Dot-and-hairline diagram motif.** Echo the title-page stepper: small filled `--green` circles connected by thin `--rule` lines with small triangle arrowheads, and an uppercase small-caps label beneath each node. Reuse this vocabulary for flow and sequence diagrams so the whole page reads as one piece; a dashed `--rule` return arc (labeled, e.g. "next week") is a good way to show a loop.

Interactive controls carry the style too but stay understated: links are `--green` with a thin underline that deepens on hover; primary and selected/active states use a soft `--green` tint fill (or a green underline / left-border) rather than a hard block fill; chips fill softly with `--green` and `--paper` text when active. Keep focus rings visible and motion gentle and quick — the typography and spacing, not animation or heavy chrome, carry the design.

## Interactive visuals

Make the visuals genuinely interactive — the reader should be able to poke at the change and watch it respond, not just read a static picture. Interaction is what turns a diagram into understanding, so beyond the quiz, include at least a few interactive elements chosen to fit the change:

- before/after panels the reader can toggle or slide between, so the old and new behavior occupy the same space and the difference pops;
- clickable flow or sequence diagrams that advance step by step, highlighting the active stage and revealing what data is passed at each hop;
- in-diagram toggles or segmented controls that switch a single diagram between states (e.g. success vs. error path) so the reader compares without losing their place;
- expandable panels that reveal detail on demand (a fuller code excerpt, an edge case) so the default view stays uncluttered;
- hover/focus reveals that surface definitions, types, or concrete example values inline;
- small "trace it yourself" widgets — pick an input, then watch which branch the old vs. new code takes.

Keep every interaction discoverable and honest: visible affordances (cursor changes, buttons that look like buttons), clear focus states, and full keyboard operability. All state lives in inline JavaScript with no network access. Use smooth CSS transitions so state changes are legible rather than jarring. Never signal state through color alone — pair it with text, an icon, or motion.

## Diagrams and examples

Use a small, reusable set of HTML/CSS diagram patterns rather than ornamental graphics:

- flow diagrams for requests, data, or control flow;
- before/after panels for changed behavior;
- labeled component cards for system boundaries;
- compact tables for mappings, invariants, and toy data.

Never use ASCII diagrams. Build diagrams with semantic HTML elements and CSS. Label arrows and include example values whenever the diagram describes data movement. Add accessible text or a caption so the explanation does not depend on visual inspection alone.

## Quiz quality rules

Treat quiz design as part of the explanation, not decoration. Before emitting the page, inspect all five questions as a set.

- Randomize the option order independently for each question. Do not always place the correct answer first, second, or in any fixed position. A deterministic shuffle with a per-page seed is acceptable; the visible order must vary across questions.
- Balance correct-answer positions across the five questions as evenly as possible. Never let position, letter, punctuation, or a repeated pattern reveal the answer.
- Keep options comparable in length, grammar, specificity, and confidence. Do not make the correct option conspicuously longer, more qualified, or more technically precise than distractors. Shorten or enrich distractors as needed.
- Make every distractor plausible and tied to a real misunderstanding of the change. Avoid joke answers, obviously impossible claims, “all/none of the above,” and trivia that cannot be inferred from the page.
- Ask about behavior, causality, contracts, edge cases, or trade-offs. Avoid questions whose answer can be guessed from a single copied phrase.
- Keep the correct answer and explanation in the page’s JavaScript data or DOM so the interaction works offline. Reveal feedback only after selection. Mark the selected option and explain both the right reasoning and, when useful, the misconception behind the distractors.
- Ensure the UI does not expose the answer through styling before selection, DOM labels, `title` attributes, source ordering, or accessibility text. Accessibility labels should describe the option, not its correctness.

## HTML and code-block constraints

- Begin the file with `<!doctype html>` and `<meta charset="utf-8">`. The page is opened as a standalone local file, so without an explicit charset a browser mis-decodes the UTF-8 and em-dashes, arrows, and math symbols (— → ≤ ∅ τ) render as mojibake like `â€"`.
- Escape user/code-derived text for HTML and JavaScript contexts. Preserve meaningful whitespace in code examples.
- Use `<pre><code>...</code></pre>` for code blocks. The CSS for `pre` must explicitly include `white-space: pre` or `white-space: pre-wrap`; verify every code block in the saved source before delivery.
- Keep JavaScript small, namespaced, and dependency-free. Use event listeners rather than inline handlers when convenient, and handle repeated quiz cards without relying on fragile global selectors.
- Include visible focus states and sufficient color contrast. Do not make correctness depend on color alone.
- Avoid claiming behavior that the inspected source does not support. Distinguish observed facts from reasonable interpretation.

## Final handoff

Return the exact absolute path to the generated HTML file as a clickable local-file link. Briefly state what was inspected and any assumptions or validation limitations. Do not place the deliverable inside the code repository unless the user explicitly requests that.
