---
name: subagent-driven-development
description: "Use after an implementation plan is approved to execute mostly independent tasks through fresh subagents with scoped context, harness-aware model routing, proportional review gates, and mandatory controller verification."
---

# Subagent-Driven Development

Use this skill after the plan is written and approved. Keep the controller session as the manager: detect the harness, extract tasks, route models, decide what to delegate, keep context narrow, review the work, verify outcomes, and close agents that are no longer needed.

## Use When

- The plan already exists and is approved.
- Most tasks are bounded and can be owned by one worker at a time.
- The controller can keep integration, review, and final verification centralized.

## Workflow

1. Confirm the plan is approved and the workspace is safe to edit.
2. Capture a routing profile before dispatching work:
   - harness name or family
   - whether fresh workers can be spawned
   - whether model or reasoning can be set per worker
   - whether browser sessions can be isolated
   - whether parallel execution is safe
3. Load routing references only when they matter:
   - read `references/harness-routing.md` when the harness is unclear or model and reasoning choices materially affect cost, latency, or correctness
   - read `references/preferred-openai-codex-preset.md` when the harness is `codex` or `openai-chatgpt` and no stronger user, repo, or org policy overrides it
4. Extract the task list up front: acceptance criteria, dependencies, risks, shared contracts, and likely write surfaces.
5. Stay in manager posture. Delegate bounded work aggressively. Keep blocking, tightly coupled, or controller-only work local.
6. Route by role and task risk:
   - controller = strongest available reasoning and coding setup
   - implementer = fastest setup that should still pass review for the task class
   - reviewer = smallest setup that can read the diff precisely enough for the risk level
   - explorer = cheapest fast read-only worker
7. In Codex or OpenAI harnesses, default to `gpt-5.4` for the controller, `gpt-5.4-mini` for most implementers, `gpt-5.4-mini` for targeted low-risk review, `gpt-5.4` for risky or full review, and `gpt-5.3-codex-spark` only as an optional shallow read-only explorer when available.
8. Bootstrap worker context narrowly. If the repo has a canonical entrypoint such as `AGENTS.md`, `CLAUDE.md`, `WORKFLOW.md`, `README.md`, or a memory index, point the worker there first and add only the extra context it still needs.
9. Check coupling before dispatching. Merge or serialize tasks that touch the same files, APIs, migrations, selectors, browser state, schemas, or shared contracts.
10. Give each implementation task one fresh worker with the exact task text, acceptance criteria, owned write scope, working directory, canonical entrypoint, necessary repo context, and model or reasoning hint when the harness supports it.
11. If browser work is needed, give that worker its own isolated browser session. Never share live browser state across workers.
12. Run review gates proportionally:
    - controller verification is always required
    - use both spec review and code-quality review for risky, user-visible, cross-cutting, shared-contract, or ambiguous changes
    - use targeted review only for tiny doc-only or tightly scoped mechanical edits when the risk is truly low
13. Verify each task in the controller session with the relevant tests, checks, or manual validation. Do not rely on the worker report alone.
14. Record reusable learnings, then close finished agents once their output is fully reviewed and no longer needed.
15. After all tasks finish, run fresh whole-branch verification and a whole-diff review when the overall change is large or cross-cutting.

## Review Depth

Use the full two-stage review loop when the change affects external behavior, APIs, schemas, migrations, auth, permissions, billing, security-sensitive paths, browser flows, shared UI components, shared contracts, concurrency, caching, or performance-critical code.

Targeted review is acceptable only for clearly low-risk work such as docs, non-semantic renames, isolated fixture updates, mechanical import moves, or formatting refreshes with no behavior change.

When unsure, use the full loop.

## References

- `references/harness-routing.md`
- `references/preferred-openai-codex-preset.md`
- `references/implementer-prompt.md`
- `references/spec-reviewer-prompt.md`
- `references/code-quality-reviewer-prompt.md`

## Guardrails

- Use this only when the plan is already approved and the tasks are mostly independent.
- Do not make workers read the plan file directly. Paste only the relevant task text and context.
- Do not flood workers with broad context when a canonical repo entrypoint exists.
- Do not dispatch conflicting tasks in parallel or give two workers the same write surface.
- Do not share browser sessions, refs, or mutable browser state across workers.
- Do not skip controller verification, and do not relax review depth for risky or shared-behavior changes.
- Do not trust an implementation success report without fresh verification evidence.
- Do not let workers invent acceptance criteria or silently make broad architectural decisions.
- Do not route every task to the strongest model by reflex.
- Do not claim a vendor-specific model is available unless the harness actually exposes it.
- Do not let a local preset override an explicit user choice, repo policy, org policy, or clear task-risk signal.
- Do not pretend model pinning or reasoning controls exist when the harness does not support them.
- If your environment cannot dispatch fresh subagents, run the same loop inline instead of pretending delegation exists.
