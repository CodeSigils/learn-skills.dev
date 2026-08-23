---
name: scope

description: Assess whether a task is appropriately sized for the current session. Use when a task feels large, vague, or potentially too broad, and you need to determine whether to proceed, narrow the scope, or split the work into smaller sessions.

metadata:

  disable-model-invocation: true

---

# Scope

Is this too big for one session?

This skill evaluates the size and complexity of the current task against the context, dependencies, uncertainty, and likely amount of work involved.

Its job is to determine whether the task should be:

- **Kept** — reasonable to complete in the current session.
- **Narrowed** — possible, but the scope should be reduced.
- **Split** — too large or complex to handle effectively as one session.

It is not a project planner. It does not create a complete roadmap or break the entire project into tasks unless that is necessary to define a practical session boundary.

## Assess the current scope

Before answering, inspect the available context:

- The user's actual goal
- The expected deliverable or outcome
- Work already completed
- Remaining work
- Number of distinct areas involved
- Dependencies between steps
- Unknowns or decisions that could significantly change the work
- Existing constraints, requirements, or acceptance criteria
- Whether the task contains multiple independently meaningful outcomes

Use the current context as the source of truth.

Do not estimate from assumptions that are not supported by the context.

## Scope signals

Treat these as signals that a task may be too large for one session:

- Multiple major deliverables
- Several unrelated areas of work
- Significant implementation plus significant research
- Many dependent steps before anything can be considered complete
- Unclear requirements that need substantial discovery first
- Work that spans multiple systems, repositories, or environments
- A task that contains several independently completable objectives
- A request whose "done" state is difficult to define

Do not treat length alone as proof that something is too large.

A technically complex task may still be appropriately scoped when the goal and boundary are clear.

## Decide

Choose exactly one:

### Keep

Use when the goal is clear, the boundary is reasonable, and the work can be completed or meaningfully concluded in the current session.

### Narrow

Use when the core goal is reasonable but the request contains optional, secondary, or distracting work.

Recommend the smallest useful reduction that preserves the primary outcome.

### Split

Use when the work contains multiple substantial objectives, large dependencies, or a broad enough scope that trying to complete everything in one session would reduce quality or make progress difficult to evaluate.

Recommend practical session-sized boundaries.

Do not split work merely for the sake of producing smaller tasks.

## Prefer a meaningful boundary

When narrowing or splitting:

- Preserve the user's primary objective.
- Keep each boundary independently meaningful.
- Put prerequisites before dependent work.
- Avoid creating artificial micro-tasks.
- Prefer a clear definition of "done" for each session.

A good session boundary should answer:

> "What meaningful outcome will exist when this session ends?"

## How to answer

Format every reply as:

1. **Verdict** — `Keep`, `Narrow`, or `Split`.
2. **Why** — one short explanation of the scope assessment.
3. **Boundary** — the recommended session boundary.

When the verdict is `Keep`, describe the intended outcome for this session.

When the verdict is `Narrow`, state what should be removed or deferred.

When the verdict is `Split`, give the smallest number of meaningful session boundaries needed.

Stop after that.

## Principles

- Scope the **session**, not the entire project.
- Optimize for meaningful progress, not maximum task count.
- Prefer one clear outcome over many partial outcomes.
- Do not confuse complexity with excessive scope.
- Do not invent requirements or dependencies.
- Do not turn this into a full project plan.
- When uncertain, preserve the user's primary objective and reduce secondary work first.

## Maintenance

This skill should remain focused on evaluating session size and defining practical boundaries.

Only update this file when its scope criteria or output format need to change.