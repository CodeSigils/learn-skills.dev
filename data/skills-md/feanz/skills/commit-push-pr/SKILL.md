---
name: commit-push-pr
description: Commit, push, and open a PR in one step
argument-hint: ticket number
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`

## Your task

Based on the above changes:

1. Create a new branch if on main, branch name should follow [Conventional Branch](https://conventional-branch.github.io/) format. If an  ticket was provided in $ARGUMENTS, include it in the branch name (e.g. `feature/42/add-login-page`).
2. Create a single commit with an appropriate message, the commit message should follow the [conventional commits](https://www.conventionalcommits.org/) format. If a ticket was provided in $ARGUMENTS, include `resolves <ticket>` in the commit message body (e.g. `resolves #42` or `resolves HC-123`).
3. Push the branch to origin
4. Create a pull request using `gh pr create`. If a ticket was provided, include `resolves <ticket>` in the PR body as well.
5. You have the capability to call multiple tools in a single response. You MUST do all of the above in a single message. Do not use any other tools or do anything else. Do not send any other text or messages besides these tool calls.