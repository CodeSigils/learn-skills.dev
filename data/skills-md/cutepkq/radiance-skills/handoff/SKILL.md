---
name: handoff
description: Compact this session into handoff.md, and append what was tried to CHANGELOG.md.
argument-hint: "What will the next session focus on?"
disable-model-invocation: true
---

# Handoff

Two documents at the project root (unless `CLAUDE.md` says otherwise), with opposite lifetimes:

- **`handoff.md`** — current state, rewritten from scratch every time.
- **`CHANGELOG.md`** — history, appended to and never rewritten. It keeps what `handoff.md` throws away.

For both: cite paths and commit hashes instead of copying content; label anything not actually run as an assumption; record failures, dead ends and skips with their reason; redact secrets; get the date from `date +%F`.

## `handoff.md` — overwrite

Read the existing file only to see which of its open items closed this session, then rewrite end to end.

1. **Done / resolved** — what changed, what ran, what came out. Every claim carries its evidence: a metric, an error that stopped firing, a diff path.
2. **Open / in progress** — running, stuck (symptom, what's ruled out, next thing to try), and untested hypotheses. Tag each `in progress` / `blocked` / `needs verification` / `parked (reason)`.
3. **Reference** — files touched, one line each; **copy-pasteable** commands with config paths, checkpoints, overrides and env vars, never "run the training script"; links to tracking runs, issues, arXiv, commits.

Arguments say what the next session is for — compress everything unrelated.

## `CHANGELOG.md` — append

One entry per experiment or method exploration, **not per session**. Nothing tried, nothing written. Newest first, directly below the `# Changelog` header. Never edit an existing entry — a failed experiment stays on the record; only factual corrections, marked as such.

```markdown
## YYYY-MM-DD — <what was tried>

- **Hypothesis** — what this settles.
- **Done** — the change or config; cite the commit or config path.
- **Result** — numbers, against a named baseline. Say so if it didn't finish.
- **Verdict** — `works` / `doesn't work` / `inconclusive`, and why.
- **Follow-up** — what it opens up or rules out.
```

If the method itself changed, run `design`.
