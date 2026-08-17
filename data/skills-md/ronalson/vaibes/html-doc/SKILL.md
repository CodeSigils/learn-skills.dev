---
name: html-doc
description: Create a polished, single-file HTML document for specs, write-ups, findings, summaries, reports, comparisons, and explanatory visualizations. Use whenever the user explicitly requests an HTML document, an HTML report, or a deliverable saved as .html. Do not use for websites, web apps, landing pages, reusable UI components, HTML snippets, DOCX, PDFs, or slide decks.
---

# HTML document

Create exactly one `.html` file. Save it to the user-specified location or choose a descriptive filename in the workspace. Deliver the file itself, not only an HTML code block, and provide its path when finished.

The document is a single-file artifact that loads Tailwind from a CDN. It therefore requires a network connection for full styling. Every document includes the light/dark theme toggle in the scaffold. Load Mermaid from its CDN only when the document contains a diagram that benefits from it. Do not describe the output as fully self-contained or available offline.

## Workflow

1. Identify the document's purpose, audience, language, source material, and requested style. Explicit user requirements override the defaults in this skill.
2. Choose a structure appropriate to the requested document type. Do not force every report or summary into a specification format.
3. Outline the content before choosing visuals. Preserve supplied facts and citations, and do not invent findings or sources.
4. Add a diagram, comparison, table, or other visual only when it communicates the material more clearly than prose.
5. Build the document from the scaffold below and keep every requested variant in the same `.html` file.
6. Render and inspect the result at desktop and mobile widths. Fix overflow, clipping, broken links, Mermaid errors, and browser console errors before delivery.

## Scaffold

Start with this base and adapt its semantic sections to the content. Set `lang` to the document's language.

```html
<!doctype html>
<html lang="{{document-language}}">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{{Document Title}}</title>
    <script>
      (() => {
        let savedTheme = null;
        try {
          savedTheme = localStorage.getItem("theme");
        } catch (_) {
          savedTheme = null;
        }

        document.documentElement.classList.toggle("dark", savedTheme === "dark");
      })();
    </script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
      html {
        --status-danger-bg: rgb(254 242 242);
        --status-danger-border: rgb(254 202 202);
        --status-danger-text: rgb(185 28 28);
        --status-success-bg: rgb(240 253 244);
        --status-success-border: rgb(187 247 208);
        --status-success-text: rgb(21 128 61);
        --status-warning-bg: rgb(255 251 235);
        --status-warning-border: rgb(253 230 138);
        --status-warning-text: rgb(146 64 14);
        color-scheme: light;
        scroll-behavior: smooth;
      }
      html.dark {
        --theme-page: rgb(2 6 23);
        --theme-surface: rgb(15 23 42);
        --theme-muted-surface: rgb(30 41 59);
        --theme-heading: rgb(248 250 252);
        --theme-text: rgb(226 232 240);
        --theme-secondary: rgb(203 213 225);
        --theme-muted: rgb(148 163 184);
        --theme-border: rgb(51 65 85);
        --theme-strong-border: rgb(100 116 139);
        --status-danger-bg: rgb(69 10 10);
        --status-danger-border: rgb(153 27 27);
        --status-danger-text: rgb(252 165 165);
        --status-success-bg: rgb(5 46 22);
        --status-success-border: rgb(22 101 52);
        --status-success-text: rgb(134 239 172);
        --status-warning-bg: rgb(69 26 3);
        --status-warning-border: rgb(146 64 14);
        --status-warning-text: rgb(252 211 77);
        color-scheme: dark;
      }
      body { text-wrap: pretty; }
      .dark body { background-color: var(--theme-page); color: var(--theme-text); }
      .dark .bg-white { background-color: var(--theme-surface); }
      .dark .bg-slate-50,
      .dark .bg-slate-100 { background-color: var(--theme-muted-surface); }
      .dark .text-slate-950,
      .dark .text-slate-900 { color: var(--theme-heading); }
      .dark .text-slate-700,
      .dark .text-slate-600 { color: var(--theme-secondary); }
      .dark .text-slate-500 { color: var(--theme-muted); }
      .dark .border-slate-200,
      .dark .border-slate-300 { border-color: var(--theme-border); }
      .dark .border-slate-400,
      .dark .border-slate-900,
      .dark .border-slate-950 { border-color: var(--theme-strong-border); }
      .dark .divide-slate-200 > :not([hidden]) ~ :not([hidden]) {
        border-color: var(--theme-border);
      }
      .dark .hover\:text-slate-950:hover { color: var(--theme-heading); }
      .status-danger {
        background-color: var(--status-danger-bg);
        border-color: var(--status-danger-border);
      }
      .status-danger .status-label { color: var(--status-danger-text); }
      .status-success {
        background-color: var(--status-success-bg);
        border-color: var(--status-success-border);
      }
      .status-success .status-label { color: var(--status-success-text); }
      .status-warning {
        background-color: var(--status-warning-bg);
        border-color: var(--status-warning-border);
      }
      .status-warning .status-label { color: var(--status-warning-text); }

      /* Add only the small document-specific layer that Tailwind does not cover cleanly. */
      @media print {
        html.dark {
          --theme-page: rgb(255 255 255);
          --theme-surface: rgb(255 255 255);
          --theme-muted-surface: rgb(241 245 249);
          --theme-heading: rgb(2 6 23);
          --theme-text: rgb(15 23 42);
          --theme-secondary: rgb(71 85 105);
          --theme-muted: rgb(100 116 139);
          --theme-border: rgb(226 232 240);
          --theme-strong-border: rgb(148 163 184);
          --status-danger-bg: rgb(254 242 242);
          --status-danger-border: rgb(254 202 202);
          --status-danger-text: rgb(185 28 28);
          --status-success-bg: rgb(240 253 244);
          --status-success-border: rgb(187 247 208);
          --status-success-text: rgb(21 128 61);
          --status-warning-bg: rgb(255 251 235);
          --status-warning-border: rgb(253 230 138);
          --status-warning-text: rgb(146 64 14);
          color-scheme: light;
        }
        body { background: #fff !important; }
        main { max-width: none !important; padding: 0 !important; }
        #theme-toggle { display: none !important; }
        section, figure, table { break-inside: avoid; }
      }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans antialiased">
    <main class="mx-auto w-full max-w-5xl space-y-12 px-5 py-10 sm:px-8 sm:py-12">
      <header>...</header>
      <section id="section-01">...</section>
      <section id="section-02">...</section>
    </main>
    <button
      id="theme-toggle"
      type="button"
      class="fixed bottom-5 right-5 z-50 inline-flex h-10 w-10 items-center justify-center rounded-lg border border-slate-300 bg-white text-slate-700 shadow-sm hover:border-slate-400 hover:text-slate-950 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-500 focus-visible:ring-offset-2"
      aria-pressed="false"
      aria-label="Switch to dark mode"
    >
      <svg id="theme-icon-moon" class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
        <path stroke-linecap="round" stroke-linejoin="round" d="M21 12.8A8.5 8.5 0 1 1 11.2 3 6.5 6.5 0 0 0 21 12.8Z" />
      </svg>
      <svg id="theme-icon-sun" class="hidden h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
        <circle cx="12" cy="12" r="3.5" />
        <path stroke-linecap="round" d="M12 2v2M12 20v2M4.93 4.93l1.42 1.42M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.42-1.42M17.66 6.34l1.41-1.41" />
      </svg>
    </button>
    <script>
      (() => {
        const root = document.documentElement;
        const toggle = document.querySelector("#theme-toggle");
        const moonIcon = document.querySelector("#theme-icon-moon");
        const sunIcon = document.querySelector("#theme-icon-sun");

        function updateToggle() {
          const isDark = root.classList.contains("dark");
          toggle.setAttribute("aria-pressed", String(isDark));
          toggle.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
          moonIcon.classList.toggle("hidden", isDark);
          sunIcon.classList.toggle("hidden", !isDark);
        }

        toggle.addEventListener("click", () => {
          const isDark = root.classList.toggle("dark");
          try {
            localStorage.setItem("theme", isDark ? "dark" : "light");
          } catch (_) {
            // The selected theme still applies for the current page view.
          }
          updateToggle();
        });

        updateToggle();
      })();
    </script>
  </body>
</html>
```

The theme toggle is required, not an optional enhancement. Keep the initialization script before Tailwind so a saved theme applies before the page renders. Light mode is the default when no preference has been saved. Keep the accessible toggle button and its behavior script at the end of `<body>`. The selected theme must persist through `localStorage`, and the document must print with the light palette.

## Document rules

- Write in a lean editorial style appropriate to the requested document type. Make it information-dense without cramped spacing.
- Avoid landing-page conventions such as hero sections, decorative chrome, marketing language, and excessive card grids.
- Do not use em dashes in generated prose unless the user requests them.
- Use semantic HTML and a logical heading hierarchy. Use real tables for tabular data rather than simulated tables made from generic `div` elements.
- Keep the layout fluid with a readable maximum width. Wide tables and diagrams must remain usable on narrow screens.
- Use inline CSS only for behavior or styling that Tailwind does not express cleanly. Use inline SVG for custom vector visuals.
- Embed important images as data URLs when portability matters. Otherwise use HTTPS image sources. Do not reference machine-local image paths in the finished document.
- Give external links `target="_blank"` and `rel="noopener noreferrer"`.
- Beyond the required theme-toggle scripts, keep the document static by default. Add another small inline classic script only when the user explicitly requests interactivity or when it is essential to understanding the document.
- Do not load external or module scripts other than the Tailwind CDN and, when needed, the Mermaid ESM import.

## Visual system

Use a grayscale palette unless the user supplies another style:

- Page background: `stone-50`
- Surfaces: `white`
- Primary text: `slate-900`
- Secondary text: `slate-600`
- Borders and rules: `slate-200`
- Strong emphasis: `slate-950`

The required dark theme maps these classes to a `slate-950` page, `slate-900` surfaces, `slate-800` muted surfaces, `slate-50` headings, `slate-200` body text, `slate-300` secondary text, and `slate-700` borders. Prefer the mapped grayscale classes already covered by the scaffold. If the document introduces another color utility, add its corresponding dark-mode override. Use `currentColor` or theme variables in custom SVGs where practical.

Outside semantic statuses, avoid saturated accent colors. Communicate distinctions with labels, line styles, borders, spacing, and font weight rather than relying on color alone. Maintain readable contrast throughout.

### Semantic status colors

Reserve color for three meanings:

- Red means danger, failure, error, bad, or a destructive consequence.
- Green means success, completion, approval, good, or a passing result.
- Amber means warning, caution, risk, or something that needs attention.

Use these colors sparingly in small status elements such as labels, icons, borders, badges, or lightly tinted callouts. Do not use them as decorative accents, section themes, or arbitrary chart-series colors. Keep the surrounding page and typography grayscale.

Never communicate status through color alone. Pair each color with an explicit word such as `Danger`, `Success`, or `Warning` and, when useful, an icon or distinct border style. Use the scaffold's `status-danger`, `status-success`, and `status-warning` classes so the treatment remains muted and readable in both themes.

```html
<aside class="status-warning rounded-lg border p-4">
  <p class="status-label text-xs font-semibold uppercase tracking-wider">Warning</p>
  <p class="mt-2 text-sm text-slate-700">Explain the risk and the action required.</p>
</aside>
```

Use serif headings only when they suit the subject. Use `text-xs uppercase tracking-wider` for schematic labels inside diagrams, not for ordinary interface text.

Choose the visual form based on the content:

- Use Mermaid for relationships, processes, sequences, hierarchies, and state changes.
- Use semantic HTML and CSS for comparisons, matrices, callouts, and annotated text.
- Use inline SVG for spatial, proportional, or editorial visuals that need precise composition.

Aim for compact diagrams around 320px tall when the material permits. Readability takes precedence over a fixed height. Do not force different visual techniques into the same document merely for variety.

## Mermaid

When Mermaid materially improves the document, add this module script to the document's `<head>`:

```html
<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
  mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "strict" });
</script>
```

Wrap each diagram in a restrained container:

```html
<figure class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    flowchart LR
      A[Source] --> B[Transform]
      B --> C[Result]
  </pre>
  <figcaption class="mt-3 text-sm text-slate-600">
    A concise explanation of what the diagram shows.
  </figcaption>
</figure>
```

Prefer simple Mermaid syntax. If a complex diagram becomes difficult to read, simplify the information or use another visual form.

## Variants and options

When the user asks for variants, render actual alternatives rather than describing hypothetical ones. Label them `A`, `B`, `C`, and so on. Choose the comparison scope from the task:

- For visual styles, render representative styled sections.
- For complete document alternatives, render the full variants when practical.
- For content, architecture, or process options, render the relevant sections, diagrams, and supporting explanation.

Place variants side by side on wide screens and stack them on narrow screens. Keep all variants in the same `.html` file.

## Acceptance checklist

Before delivery, confirm that:

- Exactly one `.html` file was created.
- The title, language, content, and visual treatment match the request.
- The document works at desktop and mobile widths without horizontal page overflow.
- Headings, tables, links, images, and diagrams are accessible and readable.
- Images have useful alt text, and meaningful inline SVGs include a `<title>` and `<desc>`.
- Visual distinctions remain understandable without color.
- The theme initializes from the saved preference, defaults to light mode when none exists, toggles correctly, updates its accessible label and icon, persists the selection, and prints in the light palette.
- Red, green, and amber appear only for danger, success, and warning states, and every colored status also has a text label or other non-color cue.
- Mermaid renders successfully when used.
- There are no broken links, clipped visuals, or browser console errors.
- The final response links to the generated `.html` file instead of returning only its source.
