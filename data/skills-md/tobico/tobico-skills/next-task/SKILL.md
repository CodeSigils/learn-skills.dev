---
name: next-task
description: Pick up and implement the next sequential task from .tasks/. TDD-style with a hard approval gate before commit; deletes the task file on commit and prompts the user to clear the context before the next task. When the final task is completed, prompts the user to finish the feature and open a draft PR instead. Use when user says "next task", "work on the next one", or "start the next task".
---

# Next Task

Implement the next sequential task from a local plan created by `/to-tasks`.

The most important thing this skill enforces: **one task per context window**. After each task is committed, stop and prompt the user to clear the context before continuing.

`.tasks/` holds one feature's plan at a time.

## Workflow

### 1. Find the next task

Look in `.tasks/`. The "next task" is the **lowest-numbered `NN-*.md` file that still exists** (excluding `TODO.md`).

If no numbered task files remain, the feature is already done — a previous session must have skipped the finish gate. Jump straight to **step 8 (finish gate)** to clean up and open the PR.

### 2. Read the task

Assume the feature branch is already checked out (created by `/to-tasks` when the plan was made). Don't create or switch branches.

Read the full task file. Summarise the goal in 2-3 sentences before writing any code. Note the acceptance criteria — they define "done".

If the task is genuinely vague, ask ONE clarifying question before starting. Don't over-engineer based on assumptions.

### 3. Implement

Work through the task using `/tdd` (red → green → refactor) when tests are appropriate. Keep scope tight — implement exactly what this task's acceptance criteria describe, nothing more.

When the acceptance criteria are met, **stop and go to step 4**. Do not proceed to commit.

### 4. ⛔ APPROVAL GATE — STOP BEFORE COMMITTING

> This is a hard stop. Do **not** run `git commit` or any step below this line until the user has explicitly said to proceed.

1. Summarise what was done (files changed, tests added, behaviour delivered, criteria met).
2. Ask: **"OK to proceed with the commit, or are changes needed first?"**
3. Wait for the response before doing anything else.
4. If changes are requested, make them and return to step 4.2.
5. Only move to step 5 once the user's answer is an explicit approval.

### 5. Commit

Delete the task file, check off the entry in `TODO.md`, then commit both alongside the code changes:

    rm .tasks/NN-<slug>.md
    # edit .tasks/TODO.md to change "- [ ] NN: ..." to "- [x] NN: ..."
    git add -A
    git commit -m "<type>: <task summary>

    Co-Authored-By: Claude <noreply@anthropic.com>"

Choose a conventional-commit type (`feat`, `fix`, `refactor`, `test`, `docs`, `chore`).

### 6. Check if this was the last task

After the commit succeeds, look in `.tasks/` for any remaining `NN-*.md` files (excluding `TODO.md`).

- **If numbered task files remain:** go to step 7 (context-clear gate).
- **If none remain:** the feature is done — go to step 8 (finish gate) instead.

### 7. ⛔ CONTEXT-CLEAR GATE — STOP HERE

Tell the user:

> Task NN complete and committed. **Clear the context now** (`/clear`) before starting the next task — this is the whole point of the workflow. Then run `/next-task` in a fresh session.

**Do NOT proceed to the next task in the same conversation**, even if the user asks. Politely remind them to clear the context first. The one-task-per-context rule is the reason this skill exists.

### 8. ⛔ FINISH GATE — LAST TASK DONE

This was the final task. Do **not** run the cleanup or open a PR until the user has explicitly approved.

1. Tell the user the feature plan is complete and list what's about to happen:
   - Delete `.tasks/TODO.md` and the `.tasks/` directory.
   - Create a `chore: finish <feature-name>` commit.
   - Push the branch and open a draft PR.
2. Ask: **"OK to finish up and open a draft PR, or hold off?"**
3. Wait for explicit approval before continuing.
4. On approval, run the cleanup commit:

        git rm .tasks/TODO.md
        rmdir .tasks
        git add -A
        git commit -m "chore: finish <feature-name>"

5. Push the branch and open a **draft** PR (e.g. `gh pr create --draft`). Use the feature name for the title and summarise the completed tasks in the body. Return the PR URL to the user.

## Tips

- Never force-push or amend published commits.
- Keep commits atomic — one task per commit.
- The approval gate is a hard stop, even when everything passes and the work feels obviously complete.
- The context-clear gate is also a hard stop. If the user says "just do the next one too", respond that this defeats the workflow and ask them to clear first.
- The finish gate is a hard stop too — never run the cleanup commit or open the PR without explicit approval.
