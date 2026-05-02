---
name: citation-audit
description: Run a pre-submission citation and reference audit for LaTeX academic papers. Use this skill whenever the user wants to verify that BibTeX entries are correct, every citation key in TeX resolves, every figure/table/equation/section reference is valid, DOI/arXiv/OpenReview/proceedings metadata matches the cited work, citation claims are supported by the cited paper, or a paper is ready for submission with clean references.
argument-hint: "[paper-dir] [--main main.tex] [--bib refs.bib] [--metadata] [--claims]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Citation Audit

Run a pre-submission audit of citations, BibTeX entries, and LaTeX cross-references. This skill is for checking correctness before submission, not for broad literature discovery.

Use this skill when a paper already has draft citations and the user wants confidence that:

- every `\cite{...}` key in TeX exists in BibTeX
- every BibTeX entry is syntactically valid and not duplicated
- every `\ref{...}`, `\cref{...}`, `\eqref{...}`, `\autoref{...}` target exists
- every `\label{...}` is unique and follows the local naming convention
- DOI, arXiv, OpenReview, URL, title, author, year, and venue metadata match the real paper
- citation claims in nearby prose are actually supported by the cited work
- bibliography style is submission-ready

Pair this with `submit-paper` for the broader submission checklist. Pair it with `research-project-memory` when citation correctness issues should become blocking paper risks or actions.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
├── scripts/
│   └── audit_latex_refs.py
└── references/
    ├── citation-claim-audit.md
    ├── metadata-verification.md
    └── report-template.md
```

## Progressive Loading

- Always run `scripts/audit_latex_refs.py` for deterministic TeX/BibTeX/reference checks.
- Read `references/metadata-verification.md` when checking DOI, arXiv, OpenReview, proceedings, or publisher metadata.
- Read `references/citation-claim-audit.md` when the user asks whether citations support the claims made in the paper, or when doing a full pre-submission audit.
- Use `references/report-template.md` for the final audit report.

## Step 1 - Locate Paper Sources

Determine:

- paper root
- main TeX file
- all included TeX files
- BibTeX files referenced by `\bibliography{...}` or `\addbibresource{...}`
- target venue and submission mode if obvious

Useful local checks:

```bash
find . -maxdepth 4 -name "*.tex" -o -name "*.bib"
find . -maxdepth 3 -name "main.tex" -o -name "paper.tex"
```

If the user provides a paper directory, use it. If no main file is provided, prefer `main.tex`, then `paper.tex`, then the TeX file containing `\begin{document}`.

## Step 2 - Run Deterministic Local Audit

Run:

```bash
python3 <citation-audit-skill-dir>/scripts/audit_latex_refs.py --paper-dir "$PAPER_DIR" --main "$MAIN_TEX"
```

Use an absolute path to the installed skill script. Do not assume a Claude-specific install path.

The script checks:

- included TeX file discovery
- citation keys in `\cite`, `\citet`, `\citep`, `\citealp`, `\citeauthor`, `\citeyear`, `\textcite`, `\parencite`
- BibTeX keys and basic syntax
- missing citation keys
- unused BibTeX entries
- duplicate BibTeX keys
- missing bibliography files
- duplicate labels
- undefined references
- labels that are never referenced
- unresolved LaTeX placeholders such as `??` and citation placeholders such as `[?]`

If the script reports blocking issues, fix or report those before doing web metadata checks. Metadata validation is much less useful if the TeX/BibTeX graph is broken.

## Step 3 - Classify Findings

Use this severity model:

- `blocking`: missing cited key, duplicate BibTeX key, undefined ref, duplicate label, invalid BibTeX structure, broken DOI for a cited work
- `important`: metadata mismatch, wrong venue/year, likely duplicate entry, citation claim not supported, arXiv cited when peer-reviewed version should be cited
- `warning`: unused BibTeX entry, unreferenced label, inconsistent key naming, missing optional DOI/URL
- `note`: style cleanup, capitalization, field normalization, BibTeX key rename suggestion

Do not treat unused BibTeX entries as blocking unless the target venue or user requires a minimal bibliography.

## Step 4 - Verify Metadata

Read `references/metadata-verification.md`.

For every cited key, verify the best available identifier:

- DOI through publisher/CrossRef/doi.org
- arXiv ID through arXiv
- OpenReview URL or forum ID through OpenReview
- proceedings URL for NeurIPS, ICML, ICLR, ACL Anthology, CVF, ACM, IEEE, Springer, or PMLR

Check:

- title
- author list or first author + author count
- year
- venue or publication status
- DOI/arXiv/OpenReview/proceedings URL
- whether a peer-reviewed version exists

When metadata cannot be verified, mark it explicitly instead of guessing.

## Step 5 - Audit Citation Claims

Read `references/citation-claim-audit.md` for full guidance.

For each citation context, classify what the prose asks the citation to support:

- background fact
- prior method existence
- closest related work
- empirical result
- theoretical result
- dataset or benchmark
- negative claim or limitation
- comparison or state-of-the-art claim

Then check whether the cited paper actually supports that role. For high-risk claims, inspect the abstract, introduction, method/result section, and if needed the PDF.

High-risk contexts:

- "first", "only", "state-of-the-art", "significantly", "provably", "guarantees"
- claims about a paper's results or limitations
- citations used to justify a baseline choice
- citations used for theory assumptions
- citations in contribution bullets or problem motivation

Do not silently rewrite scientific claims. If a citation does not support a claim, propose one of:

- replace citation
- weaken claim
- add a more specific citation
- move the claim to related work
- mark as needing author confirmation

## Step 6 - Fix Safe Issues

Safe auto-fixes:

- add missing `.bib` extension resolution in the report
- remove obvious duplicate BibTeX entries only after confirming they are truly identical
- normalize capitalization braces in titles
- add missing DOI/arXiv/URL fields when verified
- fix BibTeX field spelling
- rename labels or citation keys only if all TeX call sites are updated consistently

Never auto-fix:

- citation claims whose support is ambiguous
- substitution of one cited paper for another without explaining the scientific difference
- venue status when multiple versions exist
- author order if sources disagree

For any edit, keep the smallest possible diff.

## Step 7 - Write the Audit Report

Use `references/report-template.md`.

The final report should include:

- files checked
- local TeX/BibTeX graph status
- metadata verification status
- citation-claim support status
- blocking fixes required before submission
- recommended non-blocking cleanup
- unresolved items requiring author judgment

If the user asks for a saved report and gives no path, use:

```text
docs/reports/citation_audit_YYYY-MM-DD.md
```

## Step 8 - Final Sanity Check

Before finalizing:

- all cited keys resolve to exactly one BibTeX entry
- all required TeX references resolve to exactly one label
- blocking citation/reference problems are tracked as actions when project memory exists

## Step 9 - Write Back to Project Memory

If the project uses `research-project-memory`, update:

- `memory/risk-board.md`: blocking or important citation, metadata, label, reference, or citation-claim risks
- `memory/action-board.md`: concrete fixes for missing keys, metadata corrections, unsupported claims, or broken refs
- `memory/claim-board.md`: claims that must be weakened because citations do not support them
- `paper/.agent/paper-status.md`: citation-audit status and unresolved author decisions

Use `observed` for deterministic TeX/BibTeX graph findings and `needs-verification` for metadata or claim-support issues not fully checked.
- every blocking metadata issue is fixed or explicitly listed
- high-risk citation claims have been audited
- unresolved citation correctness questions are not hidden
- the final answer distinguishes deterministic script findings from web/semantic verification findings
