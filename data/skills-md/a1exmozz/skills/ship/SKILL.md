---
name: ship
description: "Implement beads issues using test-driven development. Use after 'raise'. Use when the user has open beads issues and wants to start coding."
---

# Follow these steps in order, one at a time.

## Input

1. Read the [cheat sheet](./references/beads-cheat-sheet.md) to understand how beads works.
2. Run `br list`

## Output

1. Run `br ready` to see which issues are unblocked.
2. Pick the next unblocked issue and run `br update <id> --status in_progress`.
3. Implement the issue using the [red, green refactor loop](./references/red-green-refactor.md).
4. Run `br close <id> --reason "<what changed>"`.
5. Run `br sync --flush-only`, then `git add .beads/` and commit.
6. Repeat from step 1 until all issues are completed.
