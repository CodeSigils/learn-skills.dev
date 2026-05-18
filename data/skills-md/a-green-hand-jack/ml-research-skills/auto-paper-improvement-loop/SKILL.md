---
name: auto-paper-improvement-loop
description: Run multi-round review-implement-recompile improvement cycles on a paper draft. Use when a draft needs iterative writing quality passes with reviewer independence (fresh context per review round), edit-whitelist gating, and crash-resumable state. Distinct from paper-reviewer-simulator (report only) and paper-draft-consistency-editor (single pass).
argument-hint: "[paper-dir] [--rounds <N>] [--edit-whitelist <ops>] [--mode writing|theory|format]"
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Auto Paper Improvement Loop

Run controlled, multi-round review → implement → recompile cycles on a paper draft. Each review round uses a fresh context to prevent confirmation bias; an edit-whitelist gates what may be changed; state is checkpointed after each round so sessions can resume.

Use this skill when:

- a paper draft needs iterative writing quality improvement beyond a single-pass consistency edit
- reviewer independence matters: prior-context reviews inflate scores and miss real problems
- certain parts of the paper (theorems, numerics, citations) should be frozen during a writing pass
- a long improvement session may span multiple agent sessions and needs crash recovery
- you want a logged diff of what changed between draft versions

Do not use this skill as a substitute for real reviewer feedback — use `paper-reviewer-simulator` first to identify structural risks. Do not use this skill to make decisions about experimental results — use `result-diagnosis` or `research-results-auditor` before running improvement loops.

Pair this skill with:

- `paper-reviewer-simulator` before the first loop round to identify high-priority issues
- `paper-draft-consistency-editor` for a single targeted pass when full multi-round iteration is not needed
- `paper-writing-assistant` when a round's review flags sections that need substantial rewriting
- `submit-paper` after the final round to verify submission readiness

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── templates/
    └── improvement-log.md
```

## Progressive Loading

- Read `templates/improvement-log.md` before starting a new loop.
- Read `paper-writing-assistant/references/edit-whitelist-contract.md` to select or customize the edit whitelist preset for this loop.
- Read `paper/.agent/writing-contract.md` when it exists to understand protected invariants.
- Read `paper/.agent/PAPER_IMPROVEMENT_STATE.json` when resuming an interrupted loop.

## Core Principles

**Reviewer independence is non-negotiable.** A reviewer that continues from the writer's session context produces inflated scores. Each review sub-task must start with no memory of prior rounds or the author's intentions — only the paper text.

**Edit-whitelist prevents scope creep.** A writing-quality pass should not silently introduce new claims, new citations, or new numerical values. Declare what is frozen before the loop starts.

**Two rounds is usually enough.** Round 1 catches the most obvious issues. Round 2 catches what round 1's fixes introduced. A third round rarely finds genuinely new problems and risks over-polishing.

**Checkpoint after every round.** Multi-round loops over long documents take time. Write state after each completed round.

## Step 1 — Configure the Loop

Decide before starting:

```markdown
Rounds: 2 (default) | 1 (quick) | 3 (high-stakes submission)
Mode: writing | theory | format | full
Edit whitelist — FROZEN (may not be changed):
  - [ ] Theorem/lemma/proof bodies
  - [ ] Any numerical result values
  - [ ] Citation keys and reference list
  - [ ] Section structure and ordering
Edit whitelist — ALLOWED:
  - [ ] Prose rewording for clarity and flow
  - [ ] Paragraph restructuring within sections
  - [ ] Caption rewording
  - [ ] Transition sentences
  - [ ] Notation consistency fixes
```

Save the configuration and a snapshot of the current PDF (or `.tex` hash) as the baseline.

## Step 2 — Initialize State

Create `paper/.agent/PAPER_IMPROVEMENT_STATE.json`:

```json
{
  "loop_id": "<paper-dir>-<YYYY-MM-DD>",
  "rounds_planned": 2,
  "rounds_completed": 0,
  "mode": "writing",
  "edit_whitelist_frozen": ["theorems", "numerics", "citations"],
  "baseline_tex_hash": "<sha256>",
  "round_summaries": [],
  "status": "in-progress"
}
```

## Step 3 — Run a Review Round (Reviewer Independence Protocol)

For each round:

1. **Prepare a self-contained review prompt** that includes only the paper text — no prior review history, no author intent, no session context.

2. **Run the review as an isolated task** using `sidecar-task-runner` with a fresh Codex session (`codex exec --ephemeral`), or explicitly start a new Claude session with no continuity. Never continue from the current agent session to run the review.

3. The review prompt should ask for:
   - section-by-section clarity issues (confusing sentences, missing transitions)
   - argument flow problems (claims not supported by the evidence in that section)
   - presentation issues (figures/tables not mentioned in prose, undefined notation)
   - format violations against the writing contract
   - a ranked list of the 5 most impactful fixes

4. Save the review output to `paper/.agent/sidecars/improvement-round-<N>/output.md`.

## Step 4 — Implement Fixes (Edit-Whitelist Enforcement)

For each fix from the review:

1. Check whether the fix touches a frozen category. If yes, log the rejection:
   ```
   REJECTED: [fix description] — touches frozen category [category]
   ```
2. For allowed fixes, implement them in the `.tex` source.
3. Recompile to confirm the paper builds without errors.
4. Log the implemented changes in the round summary.

## Step 5 — Restatement Regression Check (Theory Mode)

When `mode` includes theory:

- For each theorem/lemma in the main paper, locate its corresponding restatement in the appendix.
- Confirm the statement body is byte-identical or semantically equivalent.
- Flag any drift between main-paper statement and appendix restatement.

This check catches accidental divergence introduced by prose edits near theorem environments.

## Step 6 — Update State and Log

After each round, update `PAPER_IMPROVEMENT_STATE.json`:

```json
{
  "rounds_completed": <N>,
  "round_summaries": [
    {
      "round": 1,
      "review_output": "paper/.agent/sidecars/improvement-round-1/output.md",
      "fixes_implemented": <count>,
      "fixes_rejected": <count>,
      "recompile_status": "success"
    }
  ]
}
```

Write a human-readable log using `templates/improvement-log.md`.

## Step 7 — Final Format Check

After all rounds:

- Page count is within venue limit
- No duplicate `\label{}` keys
- No `\ref{}` to undefined labels
- No obvious overfull hbox warnings in the compile log (check for `Overfull \hbox` lines > 10pt)
- Abstract word count is within venue limit if specified

## Step 8 — Route Next Steps

- `submit-paper`: run final submission preflight after the loop
- `paper-reviewer-simulator`: run a fresh simulation if structural issues were found during the loop
- `paper-writing-assistant`: draft new content for sections flagged as needing substantial work
- Mark `status: "complete"` in `PAPER_IMPROVEMENT_STATE.json`

## Crash Recovery

If the loop is interrupted:

1. Read `paper/.agent/PAPER_IMPROVEMENT_STATE.json` to find `rounds_completed`.
2. Resume from the next round. Do not re-run completed rounds.
3. If `recompile_status` is not `success` for the last completed round, fix the compile error before continuing.

## Final Sanity Check

Before marking the loop complete:

- all planned rounds are done
- each round's review used a fresh context (no continuation)
- edit-whitelist rejections are logged
- paper compiles cleanly
- improvement log is saved
- `PAPER_IMPROVEMENT_STATE.json` has `status: "complete"`
