---
name: document-writer
description: Use whenever substantial evidence-led documents need to be orchestrated from atomic consulting workpacks into a semantically structured report, board paper, write-up, or other executive-ready output. Trigger this for serious document production with tracked materials, citation control, themeable rendering, and output adapters, especially when the reasoning should stay explicit instead of being hidden inside drafting.
---

# Document Writer

Use this skill when the task needs disciplined document workflow ownership and semantic document composition, not just a final packaged file.

## When to use

- substantial reports, board papers, strategy documents, workshop write-ups, and assessment documents
- semantically structured documents with explicit roles, boundaries, and citation objects
- themeable output where hierarchy, spacing, colour, and emphasis are rendering concerns
- Word template or style-aware output, plus other target-specific adapters
- document flows that should consume explicit upstream consulting workpacks rather than hide the reasoning inside one monolithic skill

## Bundled materials (progressive disclosure order)

1. Read this `SKILL.md` for orchestrator boundaries and required handoffs.
2. Read `references/composition-architecture.md` for the target semantic model, theme layer, semantic roles, and output adapters.
3. Read `references/graph-contract.md` for the canonical evidence graph, story graph, soft graph rules, and double-diamond convergence model.
4. Read `references/skill-routines.md` for runtime composition routines, fallback behavior, and transitional support when named upstream skills are unavailable.
5. Read `references/template-strategy.md` for Microsoft Word templates and styles, reference-doc extraction, and helper-style backfill rules.
6. Read `references/workflow.md` for the full operating method.
7. Read `references/validation-checklist.md` before handoff.
8. Read `references/quality-standard.md` before drafting and before release.
9. Use `references/repo-map.md`, `references/term-sheet.md`, and `references/tracking-readme.md` as needed.
10. Use `assets/theme-template.json`, `assets/tracking-templates/`, and `scripts/` only when the workflow calls for them.

## Upstream atomic consulting skills

Use these atomic consulting skills as named upstream subroutines when they are available in the runtime:

- `decision-framing`
- `issue-structuring-hypothesis-design`
- `evidence-discipline-synthesis`
- `narrative-synthesis-executive-writing`
- `traceability-knowledge-control`
- `challenge-quality-assurance`

Use these additional atomic skills when the document type needs them:

- `current-state-diagnosis`
- `option-architecture-trade-off-analysis`
- `prioritisation-sequencing`
- `stakeholder-power-incentive-mapping`
- `change-adoption-planning`

`references/skill-routines.md` remains the fallback path when atomic skills are unavailable. Transitional wrapper skills may still exist in the repo, but they are not the preferred runtime composition surface.

## Required upstream handoff artefacts

Minimum handoff artefacts before dense drafting:

- `tracking/decision-canvas.md`
- `tracking/issue-hypothesis-register.md`
- `tracking/source-register.md`
- `tracking/claim-ledger.md`
- `tracking/message-map.md`
- `tracking/document-development-pack.md`
- `tracking/decision-log.md`
- `tracking/qa-red-team-log.md`

Required graph artefacts for evidence and story shaping:

- `tracking/story-graph.json`
- `inputs/processed/evidence-graph.json`

Runtime document packs should still carry the established release-tracking files:

- `tracking/document-brief.md`
- `tracking/source-register.md`
- `tracking/review-notebook.md`
- `tracking/findings-workbook.md`
- `tracking/open-questions.md`

## Retained document-writer responsibilities

`document-writer` retains ownership of:

- semantic document assembly
- citation synchronization and bibliography support through Citation.js and CSL-JSON
- DOCX, PDF, and HTML composition through output adapters
- reference-doc and theme extraction, previewing, and template/style alignment
- document scaffolding
- document export and packaging
- document-specific validation and format checks

This is the runtime surface for semantic roles, theme handling, output adapters, and Microsoft Word template compatibility. It is not the place to hide generic consulting reasoning.

## Extracted consulting logic

The following consulting logic belongs upstream in atomic skills and should arrive as workpacks rather than being recreated implicitly inside drafting:

- framing the document decision, audience, scope, criteria, and constraints
- building issue structures and hypotheses
- evidence synthesis, confidence handling, and contradiction management
- narrative synthesis and message-map construction
- traceability pack management
- QA and red-team logic beyond format correctness

`document-writer` should consume those artefacts and translate them into a semantic document model. It should not rebuild them from scratch unless the user explicitly asks for a degraded fallback path.

## Working materials discipline

- keep canonical document meaning in tracked working files; markdown may be a surface, but it is not the abstraction
- keep observations, findings, decisions, and open items in tracking files
- keep intake and review state in `inputs/processed/evidence-graph.json`; markdown registers are readable projections
- keep narrative logic in `tracking/story-graph.json`; message maps and storyline notes are readable projections, not the canonical structure
- keep semantic roles, citation intent, and section boundaries explicit
- keep the citation store in CSL-JSON where possible, with Citation.js handling normalization from compatibility inputs such as BibTeX or RIS
- keep styling in themes and output adapters, not in prose rewrites or formatting tricks
- keep per-document theme intent in `full/document-theme.json` or an equivalent tracked file when the visual treatment differs from a built-in theme
- use a soft graph for insights extrapolation and story shaping; do not collapse multiple plausible paths too early
- use a double-diamond workflow across evidence and narrative shaping, but treat upstream handoff artefacts as the primary reasoning trace
- run `humanizer` near release when the prose needs cleanup, but only after the argument and evidence pack are stable

## Review gates before drafting and export

- stop if the decision frame is unclear, politically sensitive, or missing scope/owner constraints
- stop if evidence synthesis has unresolved contradictions or an unacceptably thin source base
- stop if the message map and document-development pack do not align with the intended audience and ask
- stop if traceability from source to claim to recommendation is missing
- stop if QA workpacks show material unresolved risks before export

## Minimum workflow

1. Scaffold files:
   - `uv run scripts/scaffold_document.py`
   - scaffold now seeds `report-body/references.csl.json`, `full/document-theme.json`, `assets/reference.docx`, `inputs/processed/evidence-graph.json`, and `tracking/story-graph.json`
2. Replace title and subtitle placeholders immediately.
3. Confirm or create the upstream handoff artefacts:
   - `tracking/decision-canvas.md`
   - `tracking/issue-hypothesis-register.md`
   - `tracking/source-register.md`
   - `tracking/claim-ledger.md`
   - `tracking/message-map.md`
   - `tracking/document-development-pack.md`
   - `tracking/decision-log.md`
   - `tracking/qa-red-team-log.md`
4. Build or refresh the evidence graph in `inputs/processed/evidence-graph.json`.
5. Build or refresh the story graph in `tracking/story-graph.json`.
6. Declare document structure and semantic roles before dense drafting.
7. Lock the citation path before drafting:
   - use first-class citation objects and Citation.js-managed CSL-JSON
   - keep compatibility syntax such as `[@smith2024]` at the markdown surface only
   - set citation presentation through `full/document-theme.json` or semantic metadata, not prose rewrites
8. Choose theme and target adapters separately from prose decisions.
9. Build the semantic model from markdown working files:
   - script: `scripts/build_semantic_model.mjs`
10. Assemble compatibility markdown when needed:

- `uv run scripts/assemble_report.py`

11. Validate the semantic composition model before rendering:

- script: `scripts/validate_composition.mjs`

12. Compose packaged output only after structure is stable:

- script: `scripts/compose_document.mjs`

13. Use `uv run scripts/export_docx.py --assemble --reference-doc assets/reference.docx` only for compatibility markdown paths that have not moved to the semantic adapter flow yet.
14. Run `humanizer` near release if the prose needs cleanup.
15. Share working files, graph files, theme intent, citation store, and packaged output together.

## Composition contract

- the document must declare roles such as heading, callout, caption, evidence note, reference, and appendix item
- the evidence baseline should be graph-backed, with observations, insights, contradictions, and gaps represented in `inputs/processed/evidence-graph.json`
- the narrative baseline should be graph-backed, with a soft graph in `tracking/story-graph.json`
- the story graph should support double-diamond flow with multiple paths converging as the argument sharpens
- the theme layer controls hierarchy, spacing, colour, and emphasis consistently
- renderer-independent styles should support different visual treatments from the same source
- page breaks, section boundaries, captions, lists, and references must be explicit composition concerns
- tables may also declare width, alignment, and span intent rather than relying on renderer defaults
- citations are first-class content objects, not only inline text substitutions
- Citation.js-backed CSL-JSON should be the maintained bibliography structure when the document has non-trivial references
- citation presentation should remain renderer-driven, including inline and endnote-style output, without rewriting source prose
- output is produced through adapters for Word, PDF, or other targets
- Microsoft Word templates and styles, plus native note objects where supported, are handled through the relevant adapter rather than by making the prose carry styling work

## Authoring boundary

- helper tools may inspect or extract, but the semantic document model remains canonical
- graph projections are allowed in markdown, but the evidence graph and story graph remain canonical for intake and story shaping
- styling is a theme concern and export is an adapter concern, not the authoring surface
- current Python and Pandoc helpers are compatibility tooling, not the target architecture
- if the user explicitly requires direct binary editing from the start, treat this skill as supporting context, not primary authoring

## Runtime dependency

- current compatibility helpers use PEP 723 Python scripts and the repo-root `package.json`
- composition adapters prefer JavaScript libraries that compose the document model directly
- Citation.js is the preferred library for citation normalization and CSL-JSON maintenance
- current semantic adapter runtime lives in repo-root `package.json`

## Bundled resources

- `scripts/` for scaffold, citation sync, build, validate, render, preview, Mermaid, and compatibility export tooling
- `assets/reference.docx`, `assets/reference-style-showcase.semantic.json`, `assets/reference-style-showcase.docx`, `assets/theme-template.json`, `assets/csl/`, `assets/mermaid/`, and `assets/tracking-templates/`
- `references/graph-contract.md`, `references/skill-routines.md`, `references/composition-architecture.md`, `references/template-strategy.md`, `references/workflow.md`, `references/quality-standard.md`, `references/validation-checklist.md`, `references/term-sheet.md`, `references/tracking-readme.md`, and `references/repo-map.md`

## Do not

- draft substantial prose only in chat
- bypass tracking artifacts
- hide upstream consulting reasoning inside `document-writer`
- treat `source-register.md`, `review-notebook.md`, or message-map projections as the only canonical structure when the graph files exist
- use prose rewrites to solve what should be theme problems
- hand-maintain author, year, and title fragments when Citation.js can keep the citation store normalized
- treat export tooling as the main abstraction
- treat packaged output as the only deliverable
- hide canonical document prose, citation intent, or style rules inside scripts
