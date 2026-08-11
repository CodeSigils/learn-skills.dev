---
name: harness-engineering
description: |
  Designing robust harnesses for long-running agent workflows, repository shaping, routing docs, and multi-agent orchestration.

  ALWAYS use this skill when the user discusses:
  - Multi-step agent tasks or long-running workflows (running longer than a few minutes)
  - Repository bootstrapping, scaffolding, or structural changes
  - AGENTS.md or docs/index.md routing and maintenance
  - Generator-evaluator patterns and quality control for autonomous agents
  - Planner/generator/evaluator role separation and handoffs
  - Sprint contracts and explicit work contracts for agent tasks
  - External verification strategies (browser automation, API checks, logs)
  - Context management and reset strategies for extended sessions

  Use for any task requiring durable artifacts, explicit contracts, or independent evaluation beyond simple unit tests.
  Do not use for routine feature work inside an already-stable repo with clear local verification.
---

# Harness Engineering

Use this skill when repository shape and agent continuity matter more than raw code generation.
Keep this file as the skill entrypoint. Keep bundled skill references under `./references/` and Codex-only agent files under `./codex/agents/`.

For multi-hour, multi-session, or failure-prone work, read `./references/long-running-harness-reference.md` before planning roles, handoffs, or reset strategy.

## Core Questions

- What must the next agent read, run, and verify?
- Does the repo need scaffold, runtime orchestration, or both?
- What is the smallest credible default scaffold for this request?
- Is an implementation dispatch gate required before code changes?
- Which agent should implement the next step?
- Which durable artifacts must exist before the task is done?

## Implicit Triggers

Trigger this skill even without explicit `$harness-engineering` when the task implies any of these:

- onboarding an agent to an existing repo
- bootstrapping a new repo, service, or module
- adding, moving, splitting, or renaming source roots or docs trees
- fixing stale `AGENTS.md`, stale `docs/index.md`, or missing deeper docs maps
- creating plans, contracts, handoffs, or QA artifacts for work that changes repo structure, routing docs, or long-lived task entrypoints

Do not trigger this skill for:

- routine feature or bugfix work inside an already-stable repo shape
- language-specific implementation work that does not change routing docs or orchestration
- isolated code review or test repair work with no repo-shaping consequence

## Routing Docs

- Require a root `AGENTS.md`. It is the fixed first entrypoint.
- Keep `AGENTS.md` short and routing-only.
- If the repo has durable docs, require `docs/index.md` as the deeper docs map.
- Prefer progressive disclosure: `AGENTS.md`, then `docs/index.md`, then child indexes only where needed.
- A stale path in `AGENTS.md` or `docs/index.md` is a defect.
- If structure, commands, entrypoints, or current work paths change, update the routing docs in the same pass.

## Interaction Modes

- Follow `./references/question-gate.md` as the shared user-question policy.
- `DEFAULT` is the normal mode. Do not ask the user about routine defaults, optional scope expansion, or whether to keep going. Record assumptions and proceed.
- `PLAN` is for explicit planning passes. Only hard blockers that change the identity of the first runnable artifact or implementation owner may become user questions.
- Child agents never ask the user directly. They return `NEEDS_CONTEXT` or `BLOCKED` to the parent agent with a blocker classification.
- The parent agent owns every user-facing question and should treat `NEEDS_CONTEXT` as a dispatch or context problem before considering a user question.

## Repo As Record

- Assume anything the agent cannot access locally does not exist.
- Move durable decisions out of chat and into versioned files.
- Keep active plans, handoffs, QA notes, references, and quality docs in the repo when the task actually needs them.
- Mark generated material clearly.

## Bootstrap Default

- When the user asks to initialize or bootstrap an empty or near-empty repo and the stack plus target are already clear enough to build, proceed without asking the user to pick from template menus.
- Default to the smallest credible baseline that satisfies the request and matches existing repo signals when they exist.
- Distinguish identity questions from expansion questions. Identity questions decide what the first runnable artifact is or who should own implementation. Expansion questions only widen scope.
- Do not stop for expansion questions during the first scaffold pass. Choose the narrowest runnable baseline, leave widening work out, and record the assumption.
- Do not turn the chosen baseline into a confirmation question. Avoid forms such as "先按...吗", "是否先...", or "第一版先...?" once the baseline is already clear enough to execute.
- Treat "should I proceed with the minimal baseline?" as a defect, not as cautious behavior, when the first runnable artifact is already clear.
- For bootstrap tasks with a clear identity, the first user-facing move should be an execution update that states the assumed baseline and starts the work.
- Record assumptions in the plan or handoff instead of turning them into avoidable questions.
- Ask only when the missing detail is an identity question that blocks implementation or would force a high-cost wrong turn.

## When To Simplify The Harness

As models improve, periodically re-test harness assumptions. Remove components that no longer add clear lift.

### Simplification Signals

Consider removing or collapsing roles when:

- **The model sustains longer coherent runs** without under-scoping or losing track
- **Sprint contracts become ceremonial** - the generator and evaluator agree immediately without meaningful negotiation
- **Evaluators find nothing meaningful** across multiple consecutive iterations
- **Context resets add more overhead than value** - the model stays coherent across the full task
- **Repair loops converge immediately** - the first pass is already correct

### Real Example: Opus 4.6 Transition

With Opus 4.6's improved planning and sustained agentic performance:

| Approach | Duration | Cost | Outcome |
|----------|----------|------|---------|
| Solo agent | 20 min | $9 | Broken core functionality |
| Full harness (3-agent + sprint contracts) | 6 hr | $200 | Working with AI features |
| Simplified harness (single-pass evaluation) | 4 hr | $124 | Same quality, faster |

**What changed:**
- Removed iterative sprint contracts (model plans more carefully upfront)
- Moved to single-pass evaluation with hard thresholds (model sustains longer tasks)
- Kept the evaluator for "last mile issues" like stubbed features

### Simplification Decision Tree

```
Is the task short and locally verifiable?
  → Yes: Stay single-agent
  → No: Continue

Does the model consistently complete similar tasks without drift?
  → Yes: Try single-agent with explicit contract
  → No: Add planner or evaluator

Does the evaluator consistently find real, actionable issues?
  → Yes: Keep evaluator
  → No: Remove or defer evaluator to final pass only

Do sprint contracts produce meaningful negotiation?
  → Yes: Keep contracts
  → No: Move to single-pass with post-hoc evaluation
```

### Maintaining Quality While Simplifying

When removing harness layers:

1. **Keep hard thresholds** - even without contracts, define explicit pass/fail criteria
2. **Keep external verification** - evaluators should still touch the real system
3. **Keep evidence requirements** - concrete artifacts over narration
4. **Add back quickly** - if quality drops, restore the removed layer

### Documentation

When simplifying:
- Record the simplification decision and date
- Note which model version justified it
- Define rollback triggers (quality regressions that would restore the layer)

See `./references/long-running-harness-reference.md` for the full simplification heuristics and article-backed rationale.

## Dispatch Gate

- Before stack-owned code-writing starts, run an implementation dispatch gate when the user request or repo signals make the stack clear enough to assign an implementation owner.
- The gate decides whether a matching domain-specific implementation agent must own the build step or whether a generic generator is allowed.
- Skip the gate for routing-doc-only, read-only, or clearly stack-neutral tasks.
- Record the gate result in the handoff before implementation starts.
- Keep dispatch in the parent agent. Do not have child agents open nested `codex exec`, `codex review`, or other Codex CLI sessions to delegate work.

## Agent Selection

### Codex Agents

- `planner`: prefer `harness-planner`, then `research-analyst`, then `product-manager`.
- `dispatch gate`: prefer `harness-dispatch-gate`, then the parent agent using `./references/subagent-dispatch-playbook.md`.
- `generator`: use the gate result. Prefer the matching language-specific implementation agent when required. Use `harness-generator` only when the gate explicitly allows a generic generator. Fall back to `worker` last.
- `evaluator`: prefer `harness-evaluator`, then `reviewer`, `qa-expert`, or `browser-debugger`.
- `doc-gardener`: use `harness-doc-gardener` after structure-heavy changes.

### Claude Code Agents

- `planner`: use `harness-planner` (see `./agents/harness-planner.md`)
- `dispatch gate`: use `harness-dispatch-gate` (see `./agents/harness-dispatch-gate.md`)
- `generator`: use `harness-generator` (see `./agents/harness-generator.md`)
- `evaluator`: use `harness-evaluator` (see `./agents/harness-evaluator.md`)
- `doc-gardener`: use `harness-doc-gardener` (see `./agents/harness-doc-gardener.md`)

See `./agents/README.md` for detailed usage instructions and platform differences.

### Cross-Platform Rules

- Do not silently stay single-agent after detecting an explicit language match.
- Record the gate result, chosen implementation agent, or dispatch limitation in the handoff.
- If another role is needed mid-task, the child agent must return `NEEDS_CONTEXT` or `BLOCKED` and ask the parent agent to dispatch it directly.
- Keep language and framework mappings in `./references/subagent-dispatch-playbook.md`.

## Handoffs

Every planner, generator, and evaluator handoff should state:

1. objective
2. artifacts read first
3. write or read-only scope
4. done criteria
5. evidence required on return
6. retry or escalate trigger
7. routing docs to update when the project surface changes

## Verification

- Prefer commands, tests, logs, traces, screenshots, and concrete failures over narration.
- Reproduce, repair, and re-verify instead of stopping at explanation.
- If review feedback repeats, turn it into a rule, test, or doc update when practical.

## Drift

After structure-heavy changes or merges, refresh routing docs against the current tree.

## Skill Maintenance

- After changing `SKILL.md` or `agents/openai.yaml`, verify that trigger wording, install paths, and referenced docs still match the current tree.
- Regenerate or manually trim UI metadata so `short_description` stays short and `default_prompt` stays copyable.
- Run the skill validator when the environment provides it. If it does not, do a manual frontmatter and path check before closing the update.

## References

- `./references/harness-principles.md`
- `./references/runtime-orchestration-principles.md`
- `./references/long-running-harness-reference.md` for article-backed long-running heuristics, role selection, contract shape, and reset or simplification decisions
- `./references/subagent-dispatch-playbook.md` (Codex-specific dispatch patterns)
- `./references/doc-index-maintenance.md`
- `./references/openai-docs-index-pattern.md`
- `./references/question-gate.md` for shared `DEFAULT` vs `PLAN` interaction rules and blocker taxonomy
- `./references/codex-to-claude-migration.md` for platform differences and agent migration guide
- `./agents/` for Claude Code-compatible agent definitions
- `./codex/agents/*.toml` for Codex-specific role behavior
