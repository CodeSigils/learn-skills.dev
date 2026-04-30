---
name: code-review
description: Personal code review guidelines that supplement official review behavior. Use when reviewing code, checking current changes, assessing code quality, or deciding whether a review finding is worth raising.
user-invocable: false
---

# Code Review Guidelines

Use this skill as a personal review lens alongside any official code review guidance. Focus on issues that materially affect correctness, security, architecture, maintainability, simplicity, or performance. Avoid nitpicks that do not meaningfully improve the code.

## Review Scope

- Ground findings in the code being reviewed.
- Do not rely on previous conversation history as evidence.
- Prefer concrete, actionable findings over broad style commentary.
- Preserve behavior unless the user explicitly asks for a behavior change.
- If a suggested change might alter business logic, ask before treating it as a fix.

## What To Flag

### Correctness And Behavior

Flag changes that can cause incorrect behavior, regressions, data loss, broken edge cases, or mismatches with the stated requirement.

All review suggestions must preserve original behavior unless the requested task is to change behavior.

```text
Original: if value >= 10
Wrong:    if value > 10
```

If existing behavior looks suspicious, raise it as a question or risk instead of silently changing it.

### Security And Privacy

Flag changes that weaken authentication, authorization, input handling, secret handling, sensitive data protection, or auditability.

Watch for:

- Trusting user input or external API responses without boundary validation.
- Missing authorization checks for user-, role-, or tenant-scoped data.
- Leaking tokens, credentials, personal data, or internal errors in logs or responses.
- Injection risks in SQL, shell commands, templates, URLs, dynamic imports, or code execution paths.
- Weakening existing security controls without a clear reason.

### Architecture Boundaries

Flag changes that blur ownership, bypass established layers, invert dependencies, or place logic in the wrong module.

Watch for:

- Business rules leaking into UI, controllers, route handlers, or persistence code when the project has a clearer layer for them.
- Direct cross-module access that bypasses existing public APIs or ownership boundaries.
- New dependencies that point against the intended dependency direction.
- Shared utilities becoming dumping grounds for domain-specific behavior.
- Changes that couple unrelated features or make future changes harder.

### Simplicity And Readability

Flag code that is harder to understand than the problem requires.

Watch for:

- Names that repeat obvious context, encode too many implementation details, or make simple code harder to scan.
- Abstractions created for one-time use, hiding simple code without reducing real complexity.
- Factories, strategies, managers, wrappers, or service layers that do not match an established project pattern or solve a real problem.
- Magic numbers, strings, status codes, limits, and time values that encode domain meaning without names.

```text
Bad:  userAuthenticationValidationResultStatus
Good: isValid

Bad:  isCurrentUserLoggedIntoTheSystem
Good: isLoggedIn
```

### Data Boundaries And Error Handling

Flag unclear or unsafe handling of data at boundaries, and errors that hide failure or remove useful context.

Watch for:

- Missing validation at system boundaries such as user input, external APIs, storage, network responses, and authentication boundaries.
- Paranoid internal checks that obscure logic inside trusted code paths.
- Errors swallowed silently or logged without giving callers a way to react.
- Broad catches that mask unrelated failures.
- Rethrowing errors without enough context to diagnose the failed operation.

### Performance And Resource Use

Flag performance issues when they are likely to matter in realistic usage.

Watch for:

- Avoidable O(n^2) behavior, repeated scans, or missing hash-based lookups in hot paths.
- N+1 database or API calls.
- Unbounded memory growth, caches, queues, subscriptions, listeners, or retained references.
- Expensive work repeated instead of batched, cached, memoized, or moved out of render/request loops.
- Large payloads, unnecessary serialization, or blocking I/O in latency-sensitive paths.

Do not flag theoretical performance concerns when the code path is small, cold, or clearly not performance-sensitive.

## What To Keep

- Meaningful error handling with useful context.
- Necessary validation at system boundaries.
- Direct code that is easier to read than an abstraction.
- Useful abstractions reused multiple times, reducing real complexity, or matching established architecture.
- Performance optimizations backed by realistic needs.
- Idiomatic language and framework patterns.
- Code that matches local conventions even if another style is also valid.

## Findings Quality

- Lead with bugs, regressions, security issues, and correctness risks.
- Include architecture, maintainability, and performance findings only when they have clear practical impact.
- Skip issues that a formatter, linter, typechecker, or compiler would trivially catch unless the user explicitly asks for that level of review.
- Do not over-fix; some patterns are acceptable in local context.
- Leave comment-specific writing guidance to the `comments` skill unless comments create a real review risk.

Raise a finding only when you can explain the concrete risk and a practical fix.

## Output Guidance

When presenting review findings:

1. List findings first, ordered by severity.
2. Include file and line references when possible.
3. Explain the concrete risk and a practical fix.
4. Add open questions only after findings.
5. Keep summary secondary and brief.

If no issues are found, say so clearly and mention any residual risk or test gap.