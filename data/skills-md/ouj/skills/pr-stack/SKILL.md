---
name: pr-stack
description: Manage stacked pull requests on top of plain git and GitHub CLI. Use when the user wants to create, inspect, restack, move, retarget, submit, or sync a stack of dependent branches and PRs while tracking parent branches explicitly, keeping each GitHub PR based on its recorded parent branch, and avoiding unsafe history rewrites.
---

# PR Stack

Use this skill for stacked PR workflows built on top of plain `git` and `gh`.

## Mental Model

A stack has:

- A trunk branch, usually the repo default branch.
- Feature branches where each branch has one intended parent.
- Pull requests whose base branch is that parent, not always trunk.

Track stack relationships explicitly:

- Required: `stack.trunk=<branch>`, `branch.<name>.stackParent=<parent-branch>`
- Strongly recommended: `stack.remote=<remote>`, `branch.<name>.stackParentRemoteRef=<remote>/<parent-branch>`

Use `stack.trunk` and `branch.<name>.stackParent` as the source of truth. Resolve PR state live through `gh`. Derive children by scanning branches for matching `stackParent` values.

Treat GitHub PR bases as derived state that must match the recorded parent chain. In a healthy stack, each branch PR targets its previous branch in the stack, except the bottom branch which targets trunk.

If required metadata is missing, infer a recommended parent from Git ancestry or existing PR bases, mark it as inferred, and ask the user to confirm before any operation that would rewrite history or change PR bases.

## Rules

- Resolve state first: inspect `git status -sb`, current branch, trunk, and a concise branch graph; confirm `gh` auth for PR operations; never operate on detached HEAD.
- Protect history: never rewrite the default branch, never use plain `--force`, and check for existing PRs before creating new ones.
- Handle dirty trees deliberately: if the worktree is dirty, decide whether branch switching or rebasing is safe before continuing.
- Resolve conflicts automatically when the correct result is clear from local context and stack intent; otherwise stop and report the blocker.
- Treat merged parents specially: retarget the child to the next surviving parent or trunk, then restack.
- Repair PR base drift explicitly: during submit or retarget flows, update every existing GitHub PR base to the recorded parent branch, even if the PR already exists and even if only one branch's commits changed.
- If a branch's remote PR is closed or merged, ask whether the local branch should be deleted before cleaning it up.
- Recommend performing large stack work in a subagent or separate branch when practical so the active thread context stays focused.

## Commands

### `stack track`

1. Resolve trunk, remote, current branch, and intended parent.
2. Write or repair `stack.trunk` and `branch.<name>.stackParent`.
3. Write strongly recommended remote metadata when known.
4. Verify the parent chain is not self-referential or cyclic.

### `stack log`

1. Read stack metadata for all local branches.
2. Derive parent-child relationships from `stackParent`.
3. Resolve live PR state through `gh`.
4. Present stack order, parents, and PR status.

### `stack create`

1. Capture the source branch as the intended parent.
2. Create the child branch from that source branch.
3. Generate a commit message from the staged diff.
4. Create the commit.
5. Record the source branch explicitly as the new branch's parent.

### `stack restack`

1. Resolve the branch graph from parent metadata.
2. Find descendants of the selected branch in parent-to-child order.
3. Rebase each child onto its recorded parent.
4. Resolve conflicts automatically when the correct result is clear; otherwise stop and report the blocker.

### `stack move`

1. Resolve the branch's current parent and intended new parent.
2. Update the branch's parent metadata.
3. Restack that branch onto the new parent.
4. Restack descendants in parent-to-child order.

### `stack squash`

1. Resolve the current branch's parent.
2. Compute the full branch diff against that parent.
3. Rewrite the branch into a single commit on top of the parent.
4. Generate the new commit message from the squashed diff.

### `stack submit`

1. Resolve each branch's parent branch and existing PR state through `gh`.
2. Ask whether PR title and description should be refreshed.
3. Generate or refresh PR content from the branch diff against the parent branch when requested.
4. Push each branch.
5. Create missing PRs with base = parent branch.
6. Update every existing PR base branch to the resolved parent branch so the full stack tracks the previous branch correctly.
7. Refresh PR title and body when requested.

### `stack retarget`

1. Resolve the selected branch set in stack order, including each recorded parent.
2. Compare every existing GitHub PR base branch to its resolved parent branch.
3. Update any mismatched PR base branch so each PR targets the previous branch in the stack.
4. Report which PRs changed and which were already correct.

### `stack sync`

1. Fetch the remote trunk.
2. Rebase the bottom branch onto trunk.
3. Restack the branches above it in parent-to-child order.
4. Resolve conflicts automatically when the correct result is clear; otherwise stop and report the blocker.

## Content Generation

- Generate commit messages from the staged diff or squashed branch diff, not from branch names or prior commit subjects.
- Generate PR title and body from the branch diff against the parent branch.
- If the branch has multiple commits, summarize the branch holistically instead of mirroring the commit list.
- During `stack submit`, create missing PRs first, then explicitly update every submitted PR base branch to the resolved parent branch.
- Before updating an existing PR during `stack submit`, ask whether the PR title and description should be refreshed; if yes, regenerate them from the current branch diff after base branches are corrected.

## Output Expectations

- Report the trunk branch, current branch, resolved parent, and whether parentage was explicit or inferred.
- Report which branches were restacked, squashed, moved, pushed, or submitted.
- Report which PR base branches were changed, skipped as already correct, or could not be updated.
- Include PR URLs when created or updated.
- Call out conflicts, blocked rebases, or metadata inconsistencies explicitly.
