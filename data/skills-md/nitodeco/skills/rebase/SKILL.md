---
name: rebase
description: Safely rebases the current branch onto a specified base branch, interprets diffs and conflict markers to resolve merges without losing intent, and escalates ambiguous conflicts that could cause regressions. Use when the user asks to rebase, sync with main/develop, resolve rebase conflicts, or continue an interrupted rebase.
---

# Rebase (safe workflow)

## When to use

Apply this skill whenever the user wants to rebase the checked-out branch onto another branch (or equivalent: `git rebase <base>`), including conflict resolution and `git rebase --continue`.

## Before rebasing

1. Confirm the working tree is suitable: prefer a clean state (`git status`). If there are uncommitted changes, either stash, commit, or ask what the user wants unless they already said to include them.
2. Identify the **current branch** and the **target base** (explicit name from the user, e.g. `main`, `develop`, `origin/main`).
3. Fetch if the base might be stale: `git fetch origin` (or the relevant remote), then rebase onto the resolved ref (e.g. `origin/main` if that is the source of truth).
4. Optional safety: suggest or create a backup ref before rewriting history, e.g. `git branch backup/<branch>-pre-rebase` — especially if the branch was already pushed.

## Running the rebase

1. Run `git rebase <base>` (or `git rebase -i` only if the user asked for interactive rebase).
2. On failure due to conflicts, do **not** blindly pick one side. Follow the conflict resolution process below.

## Understanding intent and conflicts

1. **Current branch intent**: Read recent commits on the branch (`git log --oneline <base>..HEAD`), PR description if available, and the diff that introduced conflicting hunks (`git show <commit>` or `git diff` as needed). Summarize what the branch is trying to change.
2. **Upstream intent**: Identify what changed on the base in the conflicting region (`git log -L` or `git blame` on the base version, `git show` on commits touching those lines). Understand why the same lines diverged.
3. **Conflict anatomy**: Open conflicted files, map `<<<<<<< ours` (rebased commits — typically _your_ patch being replayed) vs `=======` vs `>>>>>>> theirs` (incoming from the base). Verify with `git status` and `git diff --merge` / `git diff` which stage is which when unsure.

## Resolving conflicts safely

1. **Integrate both intentions** when possible: keep upstream fixes (security, correctness, API changes) and preserve the branch’s feature behavior unless they are mutually exclusive.
2. **Preserve behavior contracts**: public APIs, serialization formats, auth checks, migrations, and error handling paths deserve extra care — do not drop guards or validation just to silence the conflict.
3. **Delete conflict markers** and ensure the file builds/tests as far as you can reasonably verify (syntax, typecheck, or targeted tests if the project makes that easy).
4. After each resolved file: `git add <path>`. When all resolved: `git rebase --continue`. If the message editor opens and the user did not ask to change it, keep the proposed message.

Once everything is rebased, ask the user if they want to push the changes. If they confirm they do, push the checked out branch to the remote using `git push --force-with-lease`.

## When to stop and ask the user

Ask for clarification (show both sides and the conflicting snippet) when:

- **Semantic ambiguity**: Either resolution plausibly matches the text but changes runtime behavior (e.g. different defaults, ordering, feature flags, or business rules).
- **Policy or product choice**: UX copy, analytics events, permissions, or kill switches where the “right” merge is not inferable from code alone.
- **Large deletions vs edits**: One side deleted a block the other heavily modified — might mean a feature was intentionally removed upstream.
- **Generated or vendor files**: Lockfiles, generated SDKs, or minified assets — confirm whether to regenerate, take one side, or merge manually.
- **Binary conflicts**: Do not guess; ask which version to keep or how to reproduce the correct binary.

If the user cannot decide quickly, suggest `git rebase --abort` (or finish one file at a time with explicit approval) and outline options.

## If something goes wrong

- **Abort**: `git rebase --abort` restores pre-rebase state (when no cleaner option exists).
- **Lost commits**: Use `git reflog` to recover SHAs; recreate branch pointers if needed.
- **Do not force-push** unless the user explicitly wants to update a remote rewritten branch and understands the implications for collaborators.

## Additional resources

For a longer conflict playbook and command reference, see [reference.md](reference.md).
