---
name: pr-review
description: >-
  Standalone only — hardcore teacher: dock points / fail imperfect work on an
  open GitHub PR with strict taste/architecture/design. Pass B: five-axis Wave 1
  (Standards + Spec + Routes + BigPicture + Risk) then always-on adversarial
  Wave 2. On Nth pass, triage ALL prior finding comments (not just last pass),
  then rescan. One finding per PR comment; never summary/announcement comments;
  never repo helper scripts (use gh only). Show drafts in chat before publish.
  No em dashes. Never under /goal. For local fix loops use /code-review.
disable-model-invocation: true
---

# PR Review

**Stance:** hardcore teacher — hunt Blocking defects; mercy low, fairness stays (see [doctrine.md](doctrine.md) Stance). Operational intensity, not chat roleplay.

**Variants:** [../variants.md](../variants.md) — this skill is **standalone-only** (no `flow.md`). If flow is requested, use the **no flow** missing-variant message.

**Standalone only.** Never call from `/goal`, never ship a `pr-review-flow`. Posts on the **Pull Request**. Linked Linear is **read-only** Spec.

**Read:** [doctrine.md](doctrine.md) · [reference.md](reference.md) · **Ask style:** [../asking.md](../asking.md) · **Axes:** [../code-review/doctrine.md](../code-review/doctrine.md) (posting owned here)

**Hard:**

- **One finding = one PR comment** (never bundle)
- **Severity: Blocking or Nit only** (no non-blocking)
- **No summary / announcement comments** on the PR (chat-only status)
- **No helper scripts** in the repo (`build-review.cjs`, etc.) — **`gh` / `gh api` only**
- **Nth pass:** Pass A covers **all** prior finding comments across every pass, not only the last one
- **Pass B:** Wave 1 five axes + always Wave 2 adversarial; show drafts (severity already set), then **one** question: publish as shown? yes / no
- **No findings cap** — every real defect is its own comment

**Subagent model:** omit Task `model` unless the user asked for one.

## Process

1. **Resolve PR** — URL, number, or `gh pr view`. Fail if none / `gh` missing.
2. **Load context** — body, commits, **all** inline review comments + threads (every review, every page, resolved included). Linear/GitHub issue → Spec only.
3. **Pin base** — `gh pr diff` or `git diff <base>...HEAD`.

### Pass A (if any prior finding comments exist)

4. Check **all** prior findings. List **No action needed** (e.g. already correctly resolved) without Questions.
5. **Questions only for actionable priors** (open needing resolve/reply, or closed wrongly). `Reply like:` = one row of recommended codes (`1a 2b`). Wait if any questions.
6. Apply approved actions only (**one reply or resolve per thread**). **Do not** post a Pass A summary on the PR. If nothing actionable, skip Questions and go to Pass B.

### Pass B (always: first review or after Pass A)

7. **Fresh rescan Wave 1** — Standards + Spec + Routes + BigPicture + Risk (fill-or-fail artifacts; no findings cap). Skip issues already on an open prior finding thread. Label each new finding **Blocking** or **Nit** only.
8. **Wave 2 adversarial (always)** — launch fresh Task(s) with Wave 1 summaries; merge unique hits only (see code-review doctrine).
9. **Needs /create-test** — if the diff touches a complex architectural part with no durable behavior lock, list subjects in chat (`## Needs /create-test`) and/or as **Nit** drafts telling the author to run `/create-test`. **Tell the user**; do **not** invoke `/create-test` or write test files. Only `/code-review` and `/pr-review` may recommend locks.
10. **Show new drafts in chat** — **one full draft per finding** with severity already on it. Nothing on the PR yet. **No em dashes.**
11. **One question only** — Publish all drafts as shown? `a) yes` ← recommended / `b) no — say what to change`. Do **not** ask per draft or re-ask severity. Wait for `1a` (or override).
12. On yes: **Post via `gh` only** — each draft as its **own** comment; Request changes if any Blocking, else Comment. **Never** a summary PR comment. **Never** write review helpers into the repo.
13. **Stop** — tell the user what posted **in chat**. Fix loop → `/code-review` then `/goal` (do not auto-start).

## Anti-patterns

- Summary / "posted N comments" / index comment on the PR
- `build-review.cjs` or other repo files to submit reviews
- One comment or review body containing multiple findings
- **Non-blocking** severity; per-draft Pass B questions; re-asking blocking vs nit after drafts are shown
- Asking about correctly closed priors with nothing to do
- `Reply like:` not matching recommended codes (descriptions, or one answer per line)
- Pass A only on the latest pass
- Skipping per-prior triage when actions exist; asking Pass B before Pass A questions are answered
- Skipping Wave 2; capping findings; accepting missing artifact shapes
- Posting before showing full drafts in chat
- Approving while prior blockers remain open
- Writing Linear comments; starting `/goal`; using inside `/goal`
- Auto-running `/create-test` or writing test files (recommend only; `/create-test` is user-invoked)
- Auto-launching `bugbot` / `security-review` when the user did not ask
