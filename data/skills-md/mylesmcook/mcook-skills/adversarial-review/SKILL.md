---
name: adversarial-review
description: Adversarial code review using a cross-model workflow. Use when you want an opposing model to challenge a diff, implementation, or plan from distinct reviewer lenses and produce a synthesized verdict.
---

# Adversarial Review

Use this skill to run review passes on the opposite model, not on your own model family.

## Workflow

1. Define the review intent from the user request, recent diff, or plan.
2. If the repo has `brain/principles.md`, read it and use that as the review frame.
3. Choose reviewer count from change size:
   - small: 1 reviewer
   - medium: 2 reviewers
   - large: 3 reviewers
4. Open these reference files before spawning reviewers:
   - `references/reviewer-lenses.md`
   - `references/reviewer-prompt.md`
   - `references/verdict-format.md`
5. If you are Claude, run Codex reviewers with `codex exec`.
6. If you are Codex, run the bundled helper in `scripts/run_claude_reviewer.sh` so Claude runs in repo-tool mode and writes structured output.
7. Verify every reviewer output file exists and is non-empty before synthesizing.
8. Produce one verdict plus a lead judgment that accepts or rejects findings explicitly.

## Guardrails

- Do not use same-model subagents as reviewers.
- Do not make code changes as part of this skill.
- Do not silently drop a failed reviewer; report the failure in the verdict.
