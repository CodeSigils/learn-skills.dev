---
name: create-spec
description: Write the settled requirements into a spec a fresh window can build from alone. Only invoke when the user has just chosen it.
---

If you are on main/master, first ask whether to open a new branch for this work — the spec and the build that follows will land on it.

Write the spec to `docs/specs/YYYY-MM-DD-<topic>.md` from the current conversation context and codebase understanding, using [assets/spec-template.md](assets/spec-template.md). Do not re-interview your human partner — synthesize what the interview settled. The only questions still allowed are the product-level gaps defined below.

## The handoff contract

The approved spec is the sole requirements source: a fresh context holding only this document and the repository must be able to implement and verify the work. Conversation history is not authoritative — anything the build needs must be in the spec. The spec carries no status field; its lifecycle lives in git: **uncommitted is draft, committed is approved**. `Baseline:` records the commit the spec was written against — it is not a version lock, `/implement` cuts its tasks against the code as it stands and only escalates when the code moved in a way that contradicts the spec.

No open product question survives to review — one gets asked now, in this window, never shipped as a TBD.

**Committed means frozen.** The commit that adds the spec is the approval, and from that moment the file is read-only for every process, this one included: no amendments, no clarifications, no bookkeeping written back at the end of a build. `/implement` never writes to it — it records what it built in a `build(<basename>): complete` commit instead; committed-with-no-build-commit is how a later window tells a pending spec from a finished one, and a tracked spec with local modifications is a freeze violation the build's validator flags.

A requirements change after approval is therefore a **new spec file**, written through this skill with the full review gate, carrying one extra metadata line:

```
Supersedes: docs/specs/<old-basename>.md
```

The old file is never edited — not to point at its replacement, not to mark it dead. Its history is the record, and the new file names it. A build already running against the superseded spec is abandoned by `/implement`, not quietly re-aimed.

## Traceability

Requirements are numbered `R1..Rn`, each independently testable, with exact values and observable behavior. Acceptance criteria are numbered `A1..An`, each naming the requirement(s) it verifies and the verification method — the exact command where one exists. Every requirement is verified by at least one acceptance criterion. The implement run maps every task to these IDs and its validator checks the coverage in both directions before any review — an unnumbered requirement is invisible to that net.

## Length discipline

A spec is a list of exact values, not prose. No narrative filler, no restating what the code already shows. Prefer lists and tables over paragraphs. YAGNI ruthlessly. And no execution task list — the spec says *what*; how to build it on the current code is the implement run's plan, made fresh at build time.

## Gaps found while writing

Three kinds, three responses:

- A codebase fact → look it up, never ask.
- A reversible implementation detail → decide it, record it under Decisions as `(author's choice)`.
- Anything that changes user-visible behavior, scope, or acceptance → ask your human partner now, in this window. Never invent a requirement to kill a TBD.

## Design for isolation and clarity

- Break the system into smaller units that each have one clear purpose, communicate through well-defined interfaces, and can be understood and tested independently
- For each unit, you should be able to answer: what does it do, how do you use it, and what does it depend on?
- Can someone understand what a unit does without reading its internals? Can you change the internals without breaking consumers? If not, the boundaries need work.
- Smaller, well-bounded units are also easier for you to work with - you reason better about code you can hold in context at once, and your edits are more reliable when files are focused. When a file grows large, that's often a signal that it's doing too much.

## Working in existing codebases

- Explore the current structure before proposing changes. Follow existing patterns.
- Where existing code has problems that affect the work (e.g., a file that's grown too large, unclear boundaries, tangled responsibilities), include targeted improvements as part of the design - the way a good developer improves code they're working in.
- Don't propose unrelated refactoring. Stay focused on what serves the current goal.

## Spec self-review

After writing, re-read the spec with fresh eyes — as the build window will read it, holding only this document and the repository — then run the checklist in [references/self-review.md](references/self-review.md). Fix any issues inline — no need to re-review, just fix and move on.

## User review gate

After the self-review, ask your human partner to review the written spec before proceeding:

> "Spec written to `<path>`. Decisions I made while writing: <the `(author's choice)` list, or 'none'>. Please review it and let me know if you want to make any changes before we move on."

Wait for your human partner's response. If they request changes, make them and re-run the self-review. Once they approve, commit the spec — the commit is the approval and the freeze; there is no status line to flip. When the spec grew out of a `docs/roadmap/` queue entry, `git rm` that entry in the same commit — the entry's durable carrier is now the spec; nothing else rides along. Then ask what happens next (AskUserQuestion), two options:

| Choice | Then |
|---|---|
| Build now | invoke the `implement` skill with the spec path — no command for your human partner to type |
| Later | stop — and say how to come back: `/implement docs/specs/<filename>.md` from any window (bare `/implement` finds it while this is the branch's only committed spec with no `build(<basename>): complete` commit behind it); an interrupted build resumes with the same command |
