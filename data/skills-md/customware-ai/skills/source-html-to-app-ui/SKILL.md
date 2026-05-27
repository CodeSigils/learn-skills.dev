---
name: source-html-to-app-ui
description: >
  This skill is strict implementation instruction, not advisory
  reference text. The skill treats the HTML as discovery-only input, forces
  interactive Playwright route/state capture, then moves through scored gates
  for source acceptance, implementation planning, authored UI reproduction,
  implementation integrity, visual verification, and adversarial proof before
  signoff.
---

# Source HTML To App UI

## Strict Instruction Contract

This file is strict implementation instruction, not loose guidance and not optional reference material.

If the Agent reads this skill, it must execute it exactly as written, in order, to the letter.

Do not reinterpret the steps.
Do not reorder the steps.
Do not skip the steps.
Do not replace the steps with a simpler approach.
Do not make assumptions that override this file.
Do not treat broad similarity, intuition, or prior habits as permission to deviate.

If the Agent is uncertain, it must resolve that uncertainty inside the workflow defined here and not invent its own workflow.
If the skill says to perform a step, gate, checklist, review, or loop, that step is mandatory.
If the skill says a later phase is blocked, the Agent must treat it as blocked.
If the Agent cannot prove a phase passed in the required artifact, it must treat that phase as failed.

## Core Idea

Re-read this `SKILL.md` after every compaction before continuing work. Re-load the phase references too. Do not rely on conversational memory.

This skill is a gated execution protocol, not a loose set of suggestions. The source HTML file exists only to produce a complete visual and behavioral reference corpus through interactive Playwright browser scripts. The finished app must then be authored in the target repo from that accepted corpus plus the supplied design-system JSON.
If the Agent has read this skill, it must follow it strictly to a T and must not deviate from its required workflow, gates, artifacts, order, or blocking rules.

Assume this skill may run fully autonomously. No human is expected to watch the run line by line. The artifact files are therefore the enforcement system. A phase is not complete because the Agent feels confident. A phase is complete only when its required artifact shows a real passing score and all critical items pass.

Never promote work from one phase to the next on optimism, partial evidence, or broad visual similarity.

When this skill says `Playwright`, it means standalone interactive Node.js Playwright scripts that directly open the source HTML app or the built target app, drive the browser, and save screenshot artifacts. It does not mean the repo's normal Playwright end-to-end test suite.

## Mandatory Process Shape

This workflow shape is not optional:

1. Launch the provided HTML app with standalone interactive Playwright scripts.
2. Discover every route, state, desktop view, mobile view, and important page section through real interaction.
3. Capture that discovery as a screenshot-backed source corpus plus written inventory and source-quality score.
4. Build the target UI as authored repo code from the accepted corpus and the design-system JSON.
5. Run a separate implementation-integrity gate on the authored code before any screenshot-based target verification begins.
6. Capture target screenshots, grade them against the source corpus, fix mismatches, and loop until the gates pass.
7. Run adversarial and functional proof before signoff.

If the work skips one of those phase boundaries, the run is off track.

## Autonomous Run Contract

Treat these rules as always active:

- Every phase must end with an objective gate.
- Every gate must be recorded in the phase-owned artifact file.
- Every gate must have both a numeric threshold and critical-item pass requirement.
- If a gate fails, remain in that phase and keep iterating.
- If later work reveals missing evidence from an earlier phase, return to that earlier phase, repair it, and re-pass the gate.
- Every phase gate is an internal control point, not a user confirmation checkpoint.
- If a phase gate passes, continue directly into the next phase without asking whether to continue.
- If a phase gate fails, rework the phase, rerun the gate, and keep looping without asking the user for permission to continue.
- The purpose of the gate, redo, verification, and rework loop is to remove the need for user confirmation during execution and let the Agent complete the run autonomously.
- If a dependency, launch detail, or local setup issue blocks progress, resolve it with the most direct logical solution that preserves the workflow and continue; for example, if the interactive Playwright method is required and its dependency is missing, install it and keep going.
- Do not lower the skill's strictness, skip gates, or change direction because of an environment issue that can be solved inside the sandbox.
- Do not stop to ask the user to choose an alternate environment or manual setup path when the sandbox can solve the blocker directly.
- Do not stop after any phase to summarize progress and ask whether to continue.
- Do not assume the user will catch a shortcut. The Agent must prevent the shortcut itself.

## Critical Output Invariant

These are hard constraints:

- The target app must be a real interactive app, not a static visual copy.
- The target app must be authored in the target repo as real routes, layouts, components, state, styling, and interactions.
- The target app must be a near one-to-one reproduction of the accepted source corpus.
- The target repo's design-system foundation must be updated before route or page implementation begins: shared CSS variables in `app/app.css` first, theme mapping in `tailwind.config.ts` second, shared UI primitives next.
- If the accepted source corpus shows a sidebar shell, the target must update and use the repo's shared sidebar component or equivalent shared shell layer instead of inventing a separate page-local sidebar system.
- Layout fidelity and style fidelity are separate hard gates.
- Route coverage and state coverage are separate hard gates.
- Visible controls in the source must become real target controls with matching states.
- The target app must own the viewport as the real product UI.
- If the target UI has a sidebar shell of any kind, vertical overflow must belong only to the content pane and not to the full page. The sidebar stays stable while the content beside it scrolls.
- The provided source HTML file is discovery input only. The finished app must not depend on it at runtime.
- Reusable component styling belongs in the corresponding shared primitive or component-local styling path, not in fake global component classes such as `.btn` or `.input` inside `app/app.css`.
- Tailwind is preferred but not mandatory. Custom CSS is allowed when needed for fidelity, but reusable design-system concerns must flow through the shared CSS variables defined in `app/app.css`.
- Primary pages or views must be implemented as real router routes or repo-native route modules, not as an in-memory page-state switch inside one large component.
- If a visible nav item exists in the shell but no accepted source route/state exists for it, the target should disable that item instead of inventing a fake destination.
- Ordinary UI structure must be exact across the screen: navigation, headers, controls, filters, tables, panels, spacing, and section order.
- Ordinary UI styling must also be exact: typography weight, surface tone, border strength, radii, shadows, density, and control treatment.
- The Agent must review the app part by part, route by route, state by state, and section by section.
- If ordinary visible drift remains, the run has not passed.

## Required References

Load only the phase-relevant references, but use all four during a full delivery run:

- `references/playwright-interactive.md`
- `references/phase-1-source-discovery.md`
- `references/phase-2-5-target-implementation.md`
- `references/phase-6-7-visual-verification.md`

## Operating Modes

### Validation Mode

Use this when improving or testing the skill itself.

- Use a throwaway target app copy.
- Preserve all source, target, and grading artifacts.
- Judge repeatability across fresh runs.
- If the same failure repeats, improve the reusable skill before running again.

### Delivery Mode

Use this when the user wants the real target app built.

- Work inside the provided target repo.
- Treat the accepted source corpus as the design authority.
- Do not sign off until every gate in this file has passed in writing.

## Required Artifacts

These are mandatory in delivery mode:

- `mocks/source/`
- `mocks/verification/`
- `design/spec.json`
- `design/source-inventory.md`
- `design/source-quality-review.md`
- `design/implementation-reading.md`
- `design/implementation-review.md`
- `design/implementation-open-gaps.md`
- `mocks/verification/final-desktop.png`
- `mocks/verification/final-mobile.png`

The templates in `assets/templates/` are enforcement artifacts. Copy their structure directly. If a required table is replaced by prose or stripped down until rows are no longer auditable, the run fails.

## Multi-Phase Protocol

### Phase 0: Start-Up And Artifact Scaffolding

1. Determine mode: validation or delivery.
2. Read the target repo `AGENTS.md`.
3. Confirm the task includes:
   - path to the self-contained source HTML app file
   - path to the design-system JSON
4. Copy or normalize the design-system JSON into `design/spec.json`.
5. Create the required artifacts from templates.
6. Read:
   - `references/playwright-interactive.md`
   - `references/phase-1-source-discovery.md`
7. Inspect the target repo's real route, layout, theme, and test structure.
8. Decide how the source HTML app will be launched with interactive Playwright.
9. Do not edit target app UI files yet.
10. Do not treat HTML reading as a substitute for the discovery run.

### Phase 0 Gate: Start-Up Gate

This gate is recorded in `design/source-quality-review.md`.

Score this phase as `10/10`.

Pass rule:

- all `10/10` items above are complete
- no target UI implementation files have been edited yet

If the phase scores below `10/10`, remain in Phase 0.

### Phase 1: Source Discovery And Acceptance Loop

1. Read `references/playwright-interactive.md` again before writing the discovery scripts.
2. Write dedicated interactive Playwright discovery scripts for the source app.
3. Open the source HTML app with those scripts.
4. Capture the default desktop and mobile views.
5. Discover every route and meaningful state through real UI interaction.
6. Capture desktop and mobile screenshots for every discovered route/state.
7. Capture mobile screenshots not only for the default mobile shell, but for every accepted primary route/state and major interaction state that exists in the mobile UI.
8. Capture focused section crops for shell, navigation, header, dense workflow surfaces, dialogs, drawers, and any section that later needs section-level grading.
9. Fill `design/source-inventory.md`.
10. Fill `design/source-quality-review.md`.
11. If coverage is incomplete, rerun the interactive scripts from clean Node.js processes and capture more evidence.
12. Keep looping until the written source-quality gate passes.

HTML reading, DOM inspection, and script inspection may clarify behavior, but they do not replace interactive Playwright discovery and cannot satisfy this phase on their own.

### Phase 1 Gate: Source Promotion Gate

This gate is owned by `design/source-quality-review.md`.

Pass rule:

- score is at least `48/50`
- every critical discovery item passes
- every discovered route/state has desktop evidence
- every discovered route/state has mobile evidence unless a real source limitation is recorded
- every accepted primary route/state and major interaction state has dedicated mobile evidence, not just one default mobile-shell capture
- every visible page section has screenshot evidence and a written contract
- every route/state row in `design/source-inventory.md` cites actual screenshot paths

If this gate fails, implementation is blocked. Stay in Phase 1.

### Phase 2: Implementation Reading And Build Plan

1. Read:
   - `design/spec.json`
   - `design/source-inventory.md`
   - `design/source-quality-review.md`
   - `references/phase-2-5-target-implementation.md`
2. Write `design/implementation-reading.md` before coding.
3. Map the accepted source corpus into target files, routes, sections, and interaction families.
4. Map the design-system foundation work into the repo's real theme entry points, starting with `app/app.css`, then `tailwind.config.ts`, then the shared `app/components/ui/*` primitives.
5. Cite the exact source screenshots the implementation will build from.
6. List the visual and behavioral risks most likely to drift.
7. Fill the ordered implementation checklist in `design/implementation-reading.md` and keep the steps in strict execution order.
8. If the corpus is ambiguous, return to Phase 1, rerun the source interactive Playwright scripts, capture more evidence, and re-pass the source gate.

### Phase 2 Gate: Planning Gate

This gate is owned by `design/implementation-reading.md`.

Pass rule:

- score is at least `19/20`
- every planned route/state cites source evidence
- every planned build region maps to concrete target files or extension points
- the design-system foundation plan maps token work to `app/app.css`, theme mapping to `tailwind.config.ts`, and shared reusable control work to concrete `app/components/ui/*` files or equivalent repo-native extension points
- the ordered implementation checklist is filled and shows the intended build order through shell, routes, sections, states, and mobile
- no source-critical ambiguity remains unresolved

If this gate fails, implementation is blocked. Stay in Phase 2 or return to Phase 1 if evidence is missing.

### Phase 3: Theme And Shell Reproduction Loop

1. Translate `design/spec.json` into the target repo's real theme entry points.
2. Update `app/app.css` first so the shared CSS variables and global design tokens become the styling source of truth.
3. Update `tailwind.config.ts` after that so Tailwind theme values consume those shared CSS variables.
4. Inspect the repo's component demo or reference surface and existing `app/components/ui/*` primitives before changing route or page files.
5. Update shared component wrappers or primitives where the source app requires custom treatment.
6. Do not create fake global reusable component classes such as `.btn`, `.btn-primary`, `.input`, or `.badge` in `app/app.css`; put reusable component styling in the corresponding shared primitive instead.
7. Rebuild the shell so the target owns the viewport as the actual product UI.
8. Mark the Phase 3 ordered-checklist rows as `Done`, `Failed`, or `Blocked` in `design/implementation-review.md` and cite exact file evidence.
9. Capture `mocks/verification/01-theme-shell-desktop.png`.
10. Update `design/implementation-review.md`.
11. Update `design/implementation-open-gaps.md`.
12. Fix shell, theme, shared-component, or checklist-order drift before moving on.
13. Do not implement route or page UI until this phase passes in writing.

### Phase 3 Gate: Theme And Shell Gate

This gate is owned by `design/implementation-review.md`.

Pass rule:

- score is at least `19/20`
- the design-system foundation is visibly established in `app/app.css` and `tailwind.config.ts`
- shared reusable controls are adapted in `app/components/ui/*` or the repo's equivalent primitive layer before route/page implementation begins
- reusable component styling is not being introduced through fake global component classes in `app/app.css`
- every Phase 3 ordered checklist row is marked `Done` with evidence and none are marked `Failed`
- no critical shell-ownership issue remains
- `mocks/verification/01-theme-shell-desktop.png` exists
- open gaps for shell/theme are explicitly recorded or resolved

If this gate fails, route and page implementation is blocked. Stay in Phase 3.

### Phase 4: Route, State, And Section Reproduction Loop

1. Implement every accepted primary page or view from `design/source-inventory.md` as a real router route or repo-native route module, not as an in-memory page-state switch.
2. Build route and page UI from the adapted shared primitives as the default path.
3. Implement every listed page section, not just the outer page layout.
4. Use real local state and real interactions for tabs, filters, dialogs, drawers, menus, row selection, and mobile navigation.
5. If the source shell exposes nav items that do not have accepted source pages or states behind them, render them as disabled or unavailable rather than inventing fake destinations.
6. If the target UI has a sidebar shell, keep the sidebar stable and scope vertical overflow only to the content region beside it. Do not make the whole page scroll.
7. Custom CSS is allowed where needed for fidelity, but reusable design-system concerns must flow through the shared CSS variables and primitive layer instead of one-off global component classes.
8. Update `app/routes.ts` or the repo's equivalent route registration entrypoint and create the required route files before adding page-state logic inside route modules.
9. Mark the Phase 4 ordered-checklist rows as `Done`, `Failed`, or `Blocked` in `design/implementation-review.md` and cite exact route-file evidence.
10. After each meaningful pass, capture matching target screenshots.
11. Update `design/implementation-review.md`.
12. Update `design/implementation-open-gaps.md`.
13. If a source route, state, or section is still missing, generic, fake, or out of order in the checklist, keep iterating.

### Phase 4 Gate: Route And State Gate

This gate is owned by `design/implementation-review.md`.

Pass rule:

- score is at least `28/30`
- every critical route/state item passes
- every primary route exists as real target route UI
- no primary route is implemented as a page-state machine inside one large component
- every source interaction family exists as real target interaction
- every source-listed page section has a target counterpart and review row
- shell nav items without accepted source destinations are disabled instead of routing to invented pages
- when a sidebar shell exists, vertical overflow is scoped only to the content region instead of the whole page
- reusable controls are implemented through shared primitives or component-local styling, not fake global component classes
- mobile route/state coverage exists for the accepted mobile corpus
- every Phase 4 ordered checklist row is marked `Done` with evidence and none are marked `Failed`

If this gate fails, stay in Phase 4.

### Phase 5: Implementation Integrity Gate Loop

1. Read `references/phase-2-5-target-implementation.md` again before running the gate.
2. Review the authored target code and confirm the design-system foundation is actually in place:
   - `app/app.css` is the shared CSS-variable source of truth
   - `tailwind.config.ts` maps theme values to those variables
   - shared `app/components/ui/*` primitives or repo-native equivalents own reusable control styling
3. Review route architecture and confirm primary pages or views are implemented as real route modules or repo-native route boundaries.
4. Review interaction truth and confirm visible controls are implemented as real behavior rather than static markup or decorative state.
5. Review state distinction and confirm distinct source states are still distinct in the target implementation.
6. Review shell ownership and confirm sidebar usage, scroll ownership, and disabled-nav behavior match the accepted source shell.
7. Run the dedicated Phase 5 implementation-integrity checklist in `design/implementation-review.md` and mark every row `Done`, `Failed`, or `Blocked` with evidence.
8. Run the required non-visual repo checks for the implementation, including code checks, build checks, and targeted tests needed for the changed behavior.
9. Update `design/implementation-review.md`.
10. Update `design/implementation-open-gaps.md`.
11. Fix implementation-architecture, primitive-ownership, route, state, interaction, shell, or test-integrity failures.
12. Rerun the implementation gate until it passes in writing.

### Phase 5 Gate: Implementation Integrity Gate

This gate is owned by `design/implementation-review.md`.

Pass rule:

- score is at least `28/30`
- every critical implementation-integrity item passes
- the design-system foundation is visibly established in `app/app.css` and `tailwind.config.ts`
- shared reusable controls are adapted in `app/components/ui/*` or the repo's equivalent primitive layer before page-level styling takes over
- no reusable component styling is being introduced through fake global component classes
- every primary page or view exists as a real route boundary
- no major page architecture is implemented as a single in-memory page-state machine
- source interaction families are implemented as real target interactions
- distinct source states are not collapsed into one generic target state
- if the source shell has a sidebar, the repo's shared sidebar component or equivalent shared shell layer is actually used
- shell nav items without accepted source destinations are disabled instead of linking to invented pages
- vertical overflow belongs only to the content pane rather than the full page whenever a sidebar shell exists
- required implementation artifacts are filled with real content, not template placeholders
- required repo checks for the changed implementation have passed
- every Phase 5 integrity checklist row is marked `Done` with evidence and none are marked `Failed`

If this gate fails, visual verification is blocked. Stay in Phase 5.

### Phase 6: Visual Verification Loop

1. Read:
   - `references/playwright-interactive.md`
   - `references/phase-6-7-visual-verification.md`
2. Start the target app using the repo's normal command.
3. Write dedicated interactive Playwright verification scripts for the target app.
4. Capture target screenshots that mirror the accepted source inventory.
5. Capture focused section evidence where full-page screenshots are not enough.
6. Compare source and target route by route, state by state, and section by section.
7. Update `design/implementation-review.md`.
8. Update `design/implementation-open-gaps.md`.
9. Fix mismatches.
10. Rerun the interactive Playwright verification scripts from clean Node.js processes.
11. Keep looping until the written verification gate passes.

### Phase 6 Gate: Visual Fidelity Gate

This gate is owned by `design/implementation-review.md`.

Pass rule:

- score is at least `49/50`
- desktop fidelity score is at least `48/50`
- mobile fidelity score is at least `48/50`
- every critical verification item passes
- every source route/state row has target evidence
- every source-listed page section has target evidence and a passing section-review row
- `design/implementation-open-gaps.md` contains no unresolved ordinary drift
- final desktop and mobile screenshots exist

If this gate fails, stay in Phase 6. If either desktop or mobile fidelity is below `48/50`, fix the weaker viewport, rerun the interactive verification scripts, rescore, and keep looping until both pass.

### Phase 7: Adversarial And Functional Proof Loop

1. Assume the implementation is still wrong.
2. Find at least five serious possible mismatches.
3. Check each against the accepted source corpus.
4. Fix true mismatches.
5. Record defended non-blocking differences with concrete reasoning.
6. Exercise each visible interaction family with real user input.
7. Capture at least one proof screenshot per interaction family.
8. Update the adversarial and functional sections of `design/implementation-review.md`.

### Phase 7 Gate: Adversarial Proof Gate

This gate is owned by `design/implementation-review.md`.

Pass rule:

- score is at least `19/20`
- at least five serious suspected mismatches were checked
- every checked mismatch was either fixed or explicitly defended
- every visible interaction family has functional proof
- mobile is included in the adversarial pass

If this gate fails, stay in Phase 7 and keep iterating.

### Phase 8: Final Signoff

Before signoff:

1. Re-check that every earlier phase gate passed in writing.
2. Re-check that required artifacts still use their required tables.
3. Re-check that the app is authored repo code rather than source-file reuse.
4. Re-check that final screenshots exist.
5. Run the target repo's required checks when code changed.
6. If any ordinary mismatch remains, return to the failing phase.

### Phase 8 Gate: Signoff Gate

This gate is owned by `design/implementation-review.md`.

Score this phase as `12/12`.

Pass rule:

- all earlier gates passed and remain current
- all required artifacts exist
- final desktop and mobile screenshots exist
- open gaps contain no unresolved ordinary drift
- required review tables remain intact
- repo checks required for code changes have been run
- the app is interactive
- the app does not depend on the provided source HTML file at runtime
- the app owns the viewport as the product UI
- no placeholder or generic route remains
- no ordinary section remains unreviewed
- no critical item remains failing

If the phase scores below `12/12`, signoff is blocked.

## Disallowed Shortcuts And Automatic Fails

These shortcuts automatically fail the run:

- moving to implementation before the source gate passes
- moving past planning before the planning gate passes
- moving past theme/shell before the theme gate passes
- moving past route/state build before the route/state gate passes
- moving to visual verification before the implementation-integrity gate passes
- signing off before the implementation-integrity, visual, and adversarial gates pass
- stopping after any phase to ask the user whether to continue
- treating any passed phase gate as a user handoff point instead of an automatic promotion into the next phase
- filling the implementation checklist out of order and then treating the later steps as valid
- skipping the checklist evidence columns or leaving checklist rows in placeholder state while claiming the phase passed
- reading the HTML file and inferring the app without interactive Playwright discovery
- using repo Playwright E2E tests as a substitute for the interactive Playwright discovery or verification scripts
- embedding, fetching, or rendering the provided source HTML file at runtime
- using `iframe`, `srcDoc`, `object`, `embed`, `webview`, or injected raw HTML as the product UI
- building a screenshot viewer, design board, gallery shell, poster shell, or device frame around the app
- treating route existence as proof of route fidelity
- treating a green test suite or a successful build as proof of visual fidelity
- replacing required audit tables with prose
- leaving ordinary mismatches undocumented in the open-gaps ledger
- treating visible interactive controls as static markup
- skipping mobile discovery, mobile implementation, or mobile grading
- approving work from overall vibe rather than row-by-row evidence

## Reference Map

- `references/phase-1-source-discovery.md`: Phase 1 discovery and source acceptance.
- `references/phase-2-5-target-implementation.md`: Phase 2 planning plus Phase 3, Phase 4, and Phase 5 implementation integrity.
- `references/phase-6-7-visual-verification.md`: Phase 6 visual QA plus Phase 7 adversarial and functional proof.
- `references/playwright-interactive.md`: how this skill uses interactive Playwright scripts for discovery and verification.
- `assets/templates/phase-1-source-inventory.md`
- `assets/templates/phase-0-1-source-quality-review.md`
- `assets/templates/phase-2-implementation-reading.md`
- `assets/templates/phase-3-8-implementation-review.md`
- `assets/templates/phase-3-8-implementation-open-gaps.md`

## Non-Negotiables

- Use the phase gates exactly.
- Keep the artifacts auditable.
- Return to earlier phases when evidence is weak.
- Do not let the provided source HTML leak into the finished runtime.
