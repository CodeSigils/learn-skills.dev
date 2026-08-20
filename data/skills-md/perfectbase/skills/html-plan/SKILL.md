---
name: html-plan
description: Create or adapt implementation plans as polished, self-contained interactive HTML documents. Use when a user invokes html-plan or asks for an HTML visual plan, reviewable implementation plan, architecture plan, UI plan, storyboard, wireframe plan, or clickable planning artifact before code changes.
disable-model-invocation: true
---

# HTML Plan

Create the implementation plan normally written in chat as one standalone HTML document. Combine serious technical prose with the visual surfaces that materially improve review: diagrams, file maps, annotated code, tables, UI states, wireframes, lightweight prototypes, decisions, and open questions.

The HTML document is the approval gate. Do not implement the planned source changes until the user approves the direction.

## Plan discipline

- Gate thoughtfully. Use an HTML plan when the user needs to see, compare, operate, or approve a direction. Skip only truly trivial, unambiguous work. Never pad a plan and never produce a single-step plan.
- Research before drafting. Inspect the real repository, schemas, actions, components, helpers, tests, and conventions. Name actual files, symbols, commands, and data shapes. Do not invent codebase facts.
- Lead with reuse. For every implementation step, identify existing pieces to reuse before describing the new delta.
- Decide hard-to-reverse bets first: public identifiers, wire formats, schema shape, authentication, authorization, ownership, migration boundaries, and external contracts.
- Preserve the user's level of abstraction. Separate a reusable core from motivating examples, provider adapters, or launch-specific work.
- Make the plan standalone. A reader without the chat history must understand the objective, constraints, decisions, scope, and execution path. Do not write a revision memo or refer to a previous draft.
- Ask only questions whose answers materially change the design and cannot be resolved from the code. Otherwise state a reasonable assumption. Put all unresolved decisions in one Open Questions section at the bottom.
- Keep planning read-only. Reading, searching, and rendering the plan are allowed; modifying the product source is not.

## Workflow

1. **Ground the plan.** Read the relevant code and any source plan supplied by the user. Identify objective, current behavior, constraints, reusable primitives, affected files, irreversible decisions, risks, and verification. Completion criterion: every load-bearing claim is tied to repository evidence or explicitly labeled as an assumption.

2. **Choose the review surface.**
   - Use document-first for backend, architecture, data, API, migration, refactor, copy-only, and other non-visual work.
   - Use UI-first for static screens, before/after comparisons, component states, responsive behavior, popovers, panels, and visual direction.
   - Use prototype-first when navigation, onboarding, wizards, review flows, or interaction behavior is the main decision.
   - Use design-first only when the user asks for polished, production-like, branded, high-fidelity screens.

   Completion criterion: the surface matches the decision the reviewer must make; decorative visuals are excluded.

3. **Read the quality references.**
   - Always read [references/document-quality.md](references/document-quality.md) before authoring.
   - Read [references/visual-quality.md](references/visual-quality.md) before creating any wireframe, prototype, storyboard, or diagram.
   - Read [references/exemplar.md](references/exemplar.md) for the good/bad bar.

4. **Compose one self-contained HTML document.** Use semantic HTML, embedded CSS, inline SVG where useful, and small vanilla JavaScript only for interactions that improve review. Include no build step and no external runtime dependency. The document must remain useful with JavaScript disabled except for explicitly interactive prototypes.

5. **Make the technical plan executable.** Include outcome and done criteria, scope and non-goals, the chosen approach and rationale, affected files and symbols, ordered implementation steps, contracts or data shapes where relevant, risks and mitigations, rollout/migration when relevant, and verification that exercises the real workflow.

6. **Audit decisions.** For each unresolved architecture, scope, UX, data, rollout, provider, or ownership choice, either commit to a recommendation with rationale or add one question at the bottom with a recommended default. Never ask the same question twice.

7. **Validate the artifact.** When browser tooling is available, open or render the HTML and check desktop and narrow widths, keyboard navigation, contrast, overflow, clipping, broken anchors, inactive-looking controls, diagrams, prototype transitions, print output, and console errors. Otherwise validate the document structure, local links, and scripts statically and disclose the visual-validation limitation. Fix every defect found. Completion criterion: all intended controls and links pass the strongest validation available in the environment.

8. **Hand off for approval.** Provide a clickable link to the HTML artifact, summarize the direction in one or two sentences, name the principal files/areas affected, and ask the user to review and approve before implementation.

## HTML contract

- Emit exactly one complete HTML document with `<!doctype html>`, `html`, `head`, and `body`.
- Keep CSS and JavaScript inside the document. Prefer native browser APIs, semantic elements, CSS Grid/Flexbox, `<details>`, and inline SVG.
- Do not require a server, package installation, framework, CDN, remote font, or network request to render the plan.
- Use CSS custom properties for color, spacing, type, borders, and state. Support light and dark color schemes with legible contrast.
- Make the document responsive and printable. Avoid fixed page heights, coordinate-heavy layout, and horizontal page overflow.
- Treat buttons as real controls. Every visible interactive control must work; otherwise render it as text.
- Use stable section IDs and a compact table of contents for substantial plans.
- Escape repository content before placing it in HTML. Never embed secrets, credentials, personal data, or executable repository content.
- Keep scripts local to review behavior. Do not submit forms, call external services, run repository code, or mutate project files.
- If open questions exist, use native form controls near the bottom and include a simple client-side way to copy the selected answers for return in chat.

## Visual surface rules

- UI/product plans begin with the meaningful screens or prototype, followed by the technical document. Architecture-only plans begin with the recommendation and keep diagrams next to the claims they explain.
- Product screens show only what a user would see. Keep file paths, data flow, and implementation annotations outside the screen.
- Reproduce an existing product shell before changing it. Show only the planned delta; do not redesign unrelated areas.
- For multiple states, use labeled adjacent panels or functional tabs. Connect only genuinely sequential states.
- Keep static reference screens and functional prototypes aligned: identical labels, states, and screen IDs.
- Prefer grouped regions, layers, swimlanes, matrices, and before/after panels for architecture. Use a one-dimensional arrow chain only for a true sequence.
- Do not duplicate the same information across a top visual, body diagram, and prose. Each surface should carry information the others cannot.

## Revision behavior

When the user gives feedback, edit the existing HTML plan instead of creating a parallel plan unless they explicitly request a new alternative. Re-read the current artifact first, preserve unaffected content and interactions, make the document standalone, rerun visual validation, and return the updated artifact.

For irreversible migrations, security-sensitive work, or an explicit request for extra rigor, run one skeptical self-review of the finished plan. Look only for implicit irreversible decisions, unsupported codebase claims, uncommitted option menus, missing failure behavior, weak verification, and filler. Apply clear fixes; return genuine judgment calls to Open Questions.
