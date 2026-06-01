---
name: skill-audit
description: >
  SKILL.md SSL (Scheduling-Structural-Logical) auditor. Decomposes a target SKILL.md (or a directory of skills) into the 3-layer frame, surfaces missing / ambiguous / risky declarations, and emits a diagnostic report. Read-only — never modifies originals. Use for self-review before PR, refactor regression checks, or bulk repo audits.
  Triggers: "skill-audit", "skill audit", "ssl audit", "audit skill", "ssl 분해", "skill auditor", "audit-skill"
version: 0.1.0
ssl:
  scheduling:
    anti_triggers:
      - "Audit current session actions before commit — use galmuri:self-audit"
      - "Completion-claim gate (testid/branch/diff hygiene) — use galmuri:polish"
      - "Test-gap / coverage inspection — use galmuri:ralphi (or harnish:ralphi)"
      - "Decision forcing — use harnish:forki"
      - "Freeform text summarization — use distill / explain / doc"
      - "Auto-fixing SKILL.md content — this skill is read-only"
  structural:
    scenes: [Ingest, Decompose, Audit, Score, Report]
    resumable: true
    resume_marker: "tmp/audit-state-<n>.json"
    branches:
      - "single file path → single-mode (one scorecard)"
      - "directory path → batch-mode (per-file scorecards + collision matrix)"
      - "Logical score < 60 → emit suggested frontmatter patch alongside diagnosis"
      - "hard-limit hit (Read/Bash/sub-agents) → write tmp/audit-state-<n>.json and stop; next run resumes"
  logical:
    tools: [Read, Bash, Agent]
    side_effects:
      reads: ["{target_path}"]
      writes:
        - "{report_path} — default .galmuri/audit-{slug}.md, or stdout under --stdout"
        - "docs/reports/<YYYY-MM-DD>-audit-<slug>.md when batch report exceeds the chat budget"
        - "tmp/audit-state-<n>.json when a hard limit halts the cycle"
      deletes: []
      network: []
    idempotent: true
    rollback: null
---

# galmuri:skill-audit — SKILL.md SSL auditor

## Prerequisites
- `scripts/preflight.sh` passes (jq, bash, bats).
- Python 3 with PyYAML for frontmatter parsing.
- Read access to the target path.

## Step 1: Ingest

Receive a target path; if missing, ask: *"What should I audit? e.g. `skills/distill/SKILL.md` (single) or `skills/` (batch)."*

```bash
audit ./skills/distill/SKILL.md   # single-mode
audit ./skills                    # batch-mode → globs skills/*/SKILL.md (+ *.ko.md if present), each processed independently
```

Per-target validation: file readable · frontmatter present (between two `---`) · body ≤ 500 lines (warn if larger; do not abort).

## Step 2: Decompose

Parse the YAML frontmatter and the body separately, then construct an SSL representation. Use this prompt verbatim when delegating to an LLM helper:

```
Read the SKILL.md and emit JSON only — no markdown fences.

{
  "scheduling": {
    "triggers": [list of phrases from the description "Triggers:" line],
    "anti_triggers": [from frontmatter ssl.scheduling.anti_triggers, or null],
    "ambiguity_notes": "any trigger ≤ 4 chars, or generic adverb / conjunction"
  },
  "structural": {
    "scenes": [from frontmatter, or inferred from "## Step N:" body headings],
    "branches": [explicit branch conditions in body],
    "resumable": bool
  },
  "logical": {
    "tools": [from frontmatter ssl.logical.tools],
    "side_effects": {
      "reads": [], "writes": [], "deletes": [], "network": []
    },
    "idempotent": bool,
    "rollback": string | null
  }
}

Fields not justified by the body or frontmatter must be null or empty array. Do not infer.
```

Avoiding inference is the whole point. A plausible-looking guess hides the audit signal.

## Step 3: Audit (per-layer)

| Layer | Check | Failure |
|---|---|---|
| Scheduling | `triggers` non-empty | missing |
| Scheduling | no trigger ≤ 4 chars / stand-alone conjunction or adverb | ambiguous |
| Scheduling | `anti_triggers` declared | missing |
| Scheduling | (batch only) no verbatim trigger collision with peers | collision |
| Structural | `scenes` ≥ 2 entries (no monolith) | missing |
| Structural | every branch condition declared in `branches` (not in prose) | implicit |
| Structural | `resumable` matches body (counter / state-marker file ⇒ true) | mismatch |
| **Logical** ×1.5 | every body tool call reflected in `tools` | undeclared |
| **Logical** ×1.5 | destructive cmds (`rm` / `DROP` / `delete` / `--force`) in `side_effects.deletes` (or `writes` if overwrite) | undeclared |
| **Logical** ×1.5 | network calls (`curl` / `wget` / `fetch` / `http`) in `side_effects.network` | undeclared |
| **Logical** ×1.5 | non-idempotent body but `idempotent: true` | mismatch |
| **Logical** ×1.5 | `idempotent: false` requires `rollback` | missing |

Cross-check grep — undeclared destructive command ⇒ Logical ✗:

```bash
grep -E '(rm -rf?|DROP|delete|--force|--no-preserve)' "$target" | head -20
# diff vs. frontmatter ssl.logical.side_effects.deletes
```

## Step 4: Score

Per layer, out of 100. Missing field −15 · ambiguous −8 · Logical-layer deductions × 1.5.

Status: ≥ 80 ✓ · 60–79 ⚠ · < 60 ✗.

The score is a triage signal — Top-3 risks matter more than the absolute number. A skill at 80 with a real Logical ✗ is more dangerous than one at 60 with three ⚠ on Scheduling.

## Step 5: Report

CLI-friendly markdown with bar charts, Top-3 risks, and suggested frontmatter patches.

Single-mode shape:

```
┌─ <relative SKILL.md path> ─────────────┐
│ Scheduling   ████████░░  77  ⚠         │
│ Structural   ██████████ 100  ✓         │
│ Logical      ████░░░░░░  43  ✗         │
└────────────────────────────────────────┘

Top 3 Risks:
1. ✗ [Logical] body has `rm -rf {tmp}` but side_effects.deletes is empty
2. ✗ [Logical] idempotent flag missing
3. ⚠ [Structural] Step 2 branch condition is in prose only

[Suggested patch — frontmatter]
ssl:
  logical:
    side_effects:
      deletes: ["{tmp_dir} contents"]
    idempotent: false
    rollback: "Manual restore from .bak directory"
```

Batch-mode adds: **trigger collision matrix** (phrase × skill; ✗ verbatim / ⚠ substring or stem) and **tool dependency graph** (shared tools / scripts / hooks → SPOFs).

### Output destination

Default: `.galmuri/audit-{slug}.md` (slug from target name). `--stdout` prints to terminal. `--ci --threshold-logical=N` exits non-zero when any skill's Logical score < N.

## Token-Efficient Audit Discipline

Constraint layer over the canonical 5 scenes — **not** a replacement, and **no** fix step. The skill stays read-only; patch application is the caller's responsibility on a separate commit.

| Scene | Tool discipline |
|---|---|
| 1. Ingest | `fd` + `rg -l` only. Emit filename list, never contents. No `Read` here. |
| 2. Decompose | Targeted `rg -A 5 -B 5 'pattern'` over full `Read`. `Read` allowed only on highest-risk files surfaced in Ingest. |
| 3. Audit | Batch mode may spawn ≤ 4 parallel sub-agents, each scoped to ≤ 3 files. Each returns only `{file, line, layer, violation, suggested_patch}` — no function quoting, no prose recap. |
| 4. Score | Aggregate to a single table. Never re-quote diffs surfaced in scene 3. |
| 5. Report | Chat: ≤ 5-line summary + report path. Full report to `.galmuri/audit-{slug}.md` (or `docs/reports/<YYYY-MM-DD>-audit-<slug>.md` in batch overflow). |

### Hard limits per cycle
- `Read` calls: ≤ 10 files
- `Bash` calls: ≤ 20
- Chat output: ≤ 2000 tokens (overflow → report file)
- Parallel sub-agents: ≤ 4

If any limit is hit, write progress to `tmp/audit-state-<n>.json` and stop. Next invocation resumes from that state.

## Reference

SSL framework: arXiv:2604.24026 (Liang et al., 2026); Schank & Abelson, *Scripts, Plans, Goals and Understanding* (1977).
