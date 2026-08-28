---
name: design
description: Create or update Design.md — how the pipeline is built, stage by stage.
argument-hint: "What changed in the design?"
disable-model-invocation: true
---

# Design

Maintain **`Design.md`** at the project root (unless `CLAUDE.md` says otherwise): the pipeline as it stands now, in enough detail to reimplement from the document alone.

- **Current state only.** No history section — superseded designs live in `CHANGELOG.md`.
- **Patch, never regenerate.** Regenerating drops detail nobody thought to restate.
- **Describe the mechanism, don't paste code.** "Handles the encoding" is a failed description — say *how*.
- **Cite code** as `path/file.py:Symbol`. Where document and code disagree, the code wins. Can't find the code? Say so rather than documenting it as real.
- Tag anything unbuilt `planned`. Arguments are the change to fold in.

## Structure

**1. Overview** — what the method does, what counts as success (metric, benchmark, baseline), and a diagram of the flow.

**2. Global conventions** — axis order, coordinate system, normalization, frame indexing, padding/masking, dtype and device. Cross-stage bugs come from here; a convention that lives only in someone's head is the one that breaks.

**3. Pipeline** — the body. One subsection per stage, data → model → training → inference/eval, split further where a sub-part has its own non-obvious mechanism. Per stage:

- **Purpose** — one line.
- **In → out** — every tensor with shape, dtype, value range.
- **How it works** — steps in order, formulas and losses, learned vs fixed, branching and special cases. Give this the most room.
- **Where** — `file.py:Symbol` plus the config driving it.
- **Hyperparameters** — tagged `paper default` / `empirical` / `arbitrary`.
- **Why this way** — what was rejected, what would overturn it, linked to its `CHANGELOG.md` entry or paper. Skip for unremarkable stages; don't manufacture rationale.
- **Assumptions** — what it requires of its input, what downstream may rely on.

**4. Known limitations / unverified** — known broken, assumed but unmeasured, out of scope. Anything tested later graduates into `CHANGELOG.md`.
