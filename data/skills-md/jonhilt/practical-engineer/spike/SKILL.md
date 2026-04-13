---
name: spike
description: Resolve technology unknowns from a spec's Requires field before slicing. Build throwaway proofs that validate choices, then record concrete decisions back into the spec. Use after /spec, before /slice.
argument-hint: "[optional: path to the Spec]"
---

Reduce uncertainty — prove technology choices work before committing to TDD. The spike code is throwaway. The decisions persist.

## Read the spec

Load it and parse the **Requires** field. Categorise each dependency:

- **Resolved** — the team already knows it. Skip.
- **Needs decision** — multiple viable options exist. Research, then prove.
- **Needs proof** — the choice is made but hasn't been validated. Just prove.

Present the list and confirm which items need spiking.

## Research

For each dependency that needs a decision, work through one at a time. Present:

- **What the spec needs** — the capability in user terms
- **Options** — 2–3 viable approaches with one-line trade-offs. Prefer options the user already has experience with (check the codebase). Prefer simplest.
- **Recommendation** — your pick and why. Be opinionated but defer to the user.

Don't research exhaustively. Good-enough, not optimal.

## Prove

For each dependency needing proof, build the **smallest possible throwaway code** that answers the open question.

A spike proof:

- **Answers one question** — *"Can we stream responses?"*, *"What does the response shape look like?"*
- **Is minimal** — a single script, no error handling, no edge cases
- **Uses real calls** — actual API, actual SDK. Mocks defeat the purpose.
- **Runs and produces output** — execute and show the user

Write spike code in `./spikes/` (create if needed, add to `.gitignore`). Name files by what they prove: `spike-anthropic-streaming.ts`, `spike-bento-draft-api.py`.

After each spike runs, report:

- **What we proved** — the specific question answered
- **What we learned** — surprises, constraints, gotchas (rate limits, response shapes, latency, auth quirks)
- **Decision** — the concrete choice, with enough detail for `/slice` and `/tdd` to act on

## Decide

Update the spec: resolve the `Requires` field from vague to specific, and append a Technology Decisions section.

<tech-decisions-template>
## Technology Decisions

### <Dependency name>
- **Choice:** <provider/library/approach>
- **Proved:** <what the spike confirmed>
- **Constraints:** <rate limits, response shapes, auth model, latency — anything slicing or TDD needs>
- **Integration detail:** <call pattern, response shape, config that matters for slicing and tests>
</tech-decisions-template>

Update spec status from `Spec ready, awaiting /spike` to `Spec ready, tech validated, awaiting /slice`.

## What a spike is NOT

- **Not a prototype.** Don't build a mini version of the feature. Build the smallest thing that answers the question.
- **Not architecture.** Module design emerges in `/slice`.
- **Not permanent.** Spike code lives in `./spikes/` and is gitignored.
- **Not exhaustive research.** Two or three options, quick decision, proof, move on.

## Loop-backs

Go back to `/spec` if a spike reveals the headline interaction isn't feasible with available technology, or a supporting job needs redesigning.

Go back to `/theories` if the required technology is prohibitively complex or expensive, making the theory not worth pursuing.
