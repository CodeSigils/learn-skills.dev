---
name: project-brain
description: Access and ground work in a separate Project Brain knowledge repository through the authenticated GitHub CLI. Use at the start of substantive work in any Git repository to check its root for `.project-brain.json`; when the marker exists, using this skill and consulting the brain is mandatory before planning, implementation, diagnosis, review, documentation, or project answers. Also use when explicitly asked for Project Brain context, decisions, requirements, terminology, source-system records, or knowledge-graph output.
---

# Project Brain

Use `gh` to read the project's separate Git-backed knowledge base. Treat the brain as evidence: cite repository paths and the commit inspected, distinguish documented facts from inference, and say when the repository does not answer the question.

## Mandatory preflight

Before planning, answering, reviewing, diagnosing, documenting, or changing files in a Git worktree:

1. Resolve the current worktree root with `git rev-parse --show-toplevel`.
2. Check that root for `.project-brain.json`.
3. If the file exists, invoke this workflow and consult the brain before substantive reasoning or action. The marker is an unconditional instruction; do not wait for the user to mention Project Brain and do not decide that consultation is unnecessary.
4. Read enough relevant brain material to ground the task. At minimum, read `agent-guide.md` when it exists, then discover and read the sources relevant to the request.
5. If the brain cannot be reached, report the specific blocker. Do not silently continue with ungrounded assumptions.

The Project Brain is a separate repository identified by the marker. Do not expect it inside the active project, add it as a child directory, or clone it into the active worktree.

## Resolve the brain

1. Read `.project-brain.json` from the active worktree root. Accept this shape:

   ```json
   {
     "repository": "owner/project-brain-repo",
     "defaultBranch": "main"
   }
   ```

2. Require `repository`. If an explicitly invoked workflow has no marker, or the field is missing, ask for the Project Brain repository instead of guessing. If the marker exists but is invalid, report the configuration error and stop.
3. Run `gh auth status`. If authentication is missing, ask the user to run `gh auth login` and stop.
4. Use `defaultBranch` when present; otherwise resolve it with `gh repo view OWNER/REPO --json defaultBranchRef --jq '.defaultBranchRef.name'`.
5. Resolve the current commit with `gh api repos/OWNER/REPO/commits/BRANCH --jq '.sha'` and include its short SHA in the answer.

Never print tokens or authentication details.

## Read context

For a specific known path, fetch it without cloning:

```sh
gh api --method GET "repos/OWNER/REPO/contents/PATH" -f "ref=BRANCH" -H "Accept: application/vnd.github.raw+json"
```

For discovery or multi-file questions, clone the configured branch into a newly created temporary directory outside the active project worktree:

```sh
gh repo clone OWNER/REPO TEMP_DIR -- --depth 1 --branch BRANCH
```

Search the clone locally. Read in this order when the files exist:

1. `agent-guide.md`
2. `graphify-out/wiki/index.md`
3. Relevant wiki pages linked from the index
4. `graphify-out/GRAPH_REPORT.md` when the wiki is absent or insufficient
5. Referenced source files, especially human-authored material under `context/`
6. Machine-ingested records under `raw/` for supporting detail

Prefer human-authored decisions and requirements over generated summaries when they disagree. Note conflicts and freshness concerns explicitly. Do not treat `graphify-out/` summaries as stronger evidence than their source files.

## Answer and act

- Cite every material claim with a brain-relative path such as `context/decisions/auth.md`.
- End context-heavy answers with `Project Brain: OWNER/REPO@SHORT_SHA`.
- Separate documented facts, reasonable inference, and missing information.
- Keep access read-only by default.
- Do not edit the brain merely because the current code differs from it.
- If the user explicitly requests a knowledge update, do not push to the default branch. Clone, create a branch, edit only the relevant human-owned files, and open a pull request with `gh pr create` for review. Never edit machine-owned `raw/` content.
