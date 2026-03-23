---
name: create-github-pull-request-from-specification
description: 'Create or update a GitHub pull request from .github/pull_request_template.md using the gh CLI.'
---

# Create GitHub Pull Request from Specification

Create or update a GitHub pull request using the specification at `${workspaceFolder}/.github/pull_request_template.md`.
If the template file does not exist, create it first from `assets/default-pull-request-template.md`.

## Prerequisites

- Run inside a Git repository with a checked out feature branch.
- `gh` must be installed and authenticated.
- `${input:targetBranch}` must be a valid base branch name.

## Process

1. Check whether `${workspaceFolder}/.github/pull_request_template.md` exists.
2. If it is missing, create `${workspaceFolder}/.github/` and copy `assets/default-pull-request-template.md` to `.github/pull_request_template.md`.
3. Read `${workspaceFolder}/.github/pull_request_template.md` and extract the required sections for the pull request title and body.
4. Determine the current branch and confirm `${input:targetBranch}` as the base branch.
5. Check whether a pull request already exists for the current branch. Use `gh pr list --head <current-branch>` or `gh pr view <current-branch>` for this lookup.
6. If no pull request exists, create a draft pull request targeting `${input:targetBranch}`. Use `gh pr create --draft --base <target-branch>`.
7. Once the pull request exists, inspect its code changes with `gh pr diff` so the title and body reflect the actual diff, not only the template text.
8. Update the pull request title and body with the extracted template content and diff summary. Use `gh pr edit --title ... --body ...`.
9. Mark the pull request ready for review after the draft content is complete. Use `gh pr ready`.
10. Fetch the authenticated GitHub username with `gh api user` and assign that user to the pull request. Use `gh pr edit --add-assignee <username>`.
11. Return the pull request URL to the user.

## Requirements

- Single pull request for the complete specification
- Clear title identifying the specification and the implemented change
- Fill the pull request body with enough detail from `pull_request_template.md`
- When the template is missing, create it from the bundled default template before continuing
- Verify against existing pull requests before creation
- Do not create a duplicate pull request for the same branch
- Stop and report the error if `gh` is unavailable, unauthenticated, or a required command fails
