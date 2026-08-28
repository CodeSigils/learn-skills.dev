---
name: pr
description: >-
  Creates or updates a GitHub pull request for the current branch. Use when the
  user asks to publish committed branch changes as a PR or refresh the body of
  an existing PR. Do not use for draft-only PR copy, PR review, CI repair,
  review-comment fixes, or a push that does not include creating or updating a PR.
allowed-tools: >-
  Read Glob Grep AskUserQuestion
  Bash(git status:*) Bash(git branch:*) Bash(git log:*) Bash(git diff:*)
  Bash(git fetch:*) Bash(git push:*) Bash(git rev-parse:*)
  Bash(git symbolic-ref:*) Bash(git rev-list:*)
  Bash(gh pr create:*) Bash(gh pr list:*) Bash(gh pr view:*) Bash(gh pr edit:*)
---

Create or update one GitHub pull request for the current branch. Treat the PR as
durable knowledge transfer: explain the changed behavior and its reason, not a
file inventory. Follow explicit user instructions first, then applicable
repository guidance, before the defaults below. Write the title in English. Write
the body in the language the user explicitly requests, or otherwise in the
language of the user's request; this skill does not impose a fixed body language.
Write the user-facing response in the user's language.

## 1. Inspect and Guard

1. Read applicable repository guidance and any pull request template before
   composing content.
2. Inspect the current branch and worktree:

   ```bash
   git branch --show-current
   git status --short --branch
   git symbolic-ref --quiet --short refs/remotes/origin/HEAD
   ```

   Keep the symbolic-ref result only as the fallback base for a new PR. Derive
   its branch name by removing only the leading `origin/`; do not select the
   comparison ref until the PR lookup below is complete.
3. Refresh remote refs with `git fetch --prune origin`. If the fetch fails, show
   the error and stop; do not make publish decisions from stale remote state.
4. Find an open PR for the exact head branch:

   ```bash
   gh pr list --head <branch> --state open --limit 1 \
     --json number,title,url,body,isDraft,baseRefName,headRefName
   ```

   If the command fails, show the error and stop. Save the result for later use;
   an empty array means create and one result means update.
5. Choose the effective base only after that lookup:

   - For an existing PR, use its `baseRefName`. If the user explicitly requested
     a different base, stop and clarify instead of comparing against either one
     silently.
   - For a new PR, use the user-requested base when supplied; otherwise use the
     remote default branch. If neither is available, stop and ask for the base.

   Normalize a supplied `origin/<base>` by removing only the leading `origin/`,
   then set `<comparison-ref>` to `origin/<base>`. Verify that ref exists after
   the fetch. Stop if the current branch equals the effective base or if
   `git log <comparison-ref>..HEAD --oneline` contains no commits.
6. If tracked or untracked changes are present, tell the user they are not part
   of the PR and ask whether to commit them first. Continue only after the user
   commits them or explicitly chooses to exclude them.
7. Determine the upstream with:

   ```bash
   git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}'
   ```

   - With no upstream, run `git push -u origin <branch>`.
   - With an upstream, compute `git rev-list --left-right --count <upstream>...HEAD`.
     If the left count is nonzero, stop and report that the local branch must be
     synchronized; do not merge, rebase, or force-push implicitly. If only the
     right count is nonzero, run `git push`.
   - If a push fails, show the error and stop. Never retry with `--force`.

## 2. Build the PR Model

Using the saved PR lookup and the effective `<comparison-ref>` selected above,
inspect every PR commit and the complete PR diff:

```bash
git log <comparison-ref>..HEAD --format='%h%x09%s%n%b'
git diff --stat <comparison-ref>...HEAD
git diff <comparison-ref>...HEAD
```

Treat these outputs as the exclusive PR change set when selecting body depth,
composing claims, checking change coverage, and reporting commit and file counts.
Throughout the remaining steps, “branch commits” means exactly the commits
returned by `git log <comparison-ref>..HEAD`. A commit reachable from
`<comparison-ref>` is base history, not a PR change, even when it is absent from
the remote default branch; do not include its behavior in the body.

Use commit history as evidence, not as the narrative structure. Synthesize the
final behavior across commits, ignoring intermediate states that the complete PR
diff supersedes. Before drafting, separate each material workflow or component
and map its evidenced actor, trigger, input and time scope, state or output,
downstream handoffs and failure behavior, and rollout or migration ordering, as
applicable. Check internally that every material branch change is covered, but
do not expose that coverage as a chronological commit list.

From the retained evidence, identify the primary before-and-after behavior.
Include a reason, semantic explanation, impact, constraint, tradeoff, or risk
only when the evidence supports that exact connection; omit it rather than infer
it from related changes. Use the saved empty lookup result to create, or its
single result to update.

## 3. Compose Grounded Content

### Title for a new PR

- Start with a concise imperative English verb and name the core behavior.
- Keep the title at most 40 characters, excluding a ticket prefix.
- If the branch contains an identifier matching letters or alphanumerics followed
  by a hyphen and digits, uppercase it and prepend it in brackets. For example,
  `feature/proj-42-fix-layout` becomes `[PROJ-42] Fix layout`.
- Do not change the title of an existing PR.

### Body depth

Count commits and changed files, then use the more detailed level when the two
measures disagree:

| Level | Threshold | Generated sections |
|-------|-----------|--------------------|
| Simple | 1-2 commits and at most 3 files | Summary, Changes |
| Standard | 3-10 commits or 4-10 files | Summary, Key Changes, Validation |
| Complex | 11+ commits or 11+ files | Summary, themed Key Changes, Validation, Review Notes |

Keep the body proportional even when a repository template adds required
sections. Apply these content rules:

- Lead with the behavioral before-and-after model and why it matters.
- State the single core intuition that explains most of the PR, then group
  supporting changes by behavior or reviewer concern. When material workflows
  do not share one evidenced reason or outcome, keep their before-and-after
  explanations distinct instead of forcing an umbrella narrative. Do not
  organize the body by commit order, narrate files, or restate every diff hunk.
- Omit secondary and mechanical edits from `Summary` and `Key Changes` unless
  they alter the mental model or require reviewer action. Report test commands
  and results in `Validation` instead of listing routine test implementation as
  a key change.
- Use one minimal toy example when concrete input, state, or output makes a
  non-obvious rule faster to understand. For example: `Requests r1, r1, r2 used
  to create three jobs; they now create two because request ID defines identity.`
  Keep the behavior faithful to the diff, and do not force an example when prose
  is clearer.
- Omit commit hashes and a commit-by-commit log unless the user or a repository
  template explicitly requires them.
- Report validation only when supported by evidence. Attribute results reported
  only in commit history, and do not present changed tests or static inspection
  as passing execution results. Name any material runtime, integration,
  deployment, migration, or external-service boundaries the reported checks did
  not exercise. When a required validation section has no evidence of executed
  checks, state the language-equivalent of `Not run`; never guess.
- Include migration notes, risks, or reviewer guidance only when the diff
  supports them.

Wrap only generated content in these exact ownership markers:

```markdown
<!-- pr-skill:start -->
<generated sections>
<!-- pr-skill:end -->
```

When updating:

- If both markers exist once and in order, replace only the marked block and
  preserve all text outside it byte-for-byte.
- If the body has no markers, preserve the entire existing body byte-for-byte and
  append one marked generated block.
- If markers are malformed, duplicated, or out of order, stop and ask the user
  how to proceed. Do not risk deleting authored content.

Add `--draft` when creating if the user requested a draft or the branch starts
with `draft/` or `wip/`. Updating the body must preserve the existing draft state.

## 4. Verify, Execute, and Confirm

Before any `gh pr create` or `gh pr edit`, verify that:

1. The create title satisfies the language, length, verb, and ticket rules.
2. The body matches the chosen depth, leads with the core intuition, and covers
   every material branch change without relying on a chronological commit list.
3. Every factual claim is grounded in the inspected diff, history, guidance, or
   template.
4. Existing content outside the ownership markers is unchanged.

Pass the body through standard input so shell interpolation cannot alter it:

```bash
gh pr create --title "<title>" --assignee @me --base "<base>" \
  --head "<branch>" [--draft] --body-file - <<'EOF'
<body>
EOF

gh pr edit "<number>" --body-file - <<'EOF'
<body>
EOF
```

Do not include the bracketed optional flag literally; either add `--draft` or
omit it. After success, run `gh pr view <number-or-url> --json
number,title,url,body,isDraft,commits,files` and verify the published title, body,
draft state, commit count, and file count. If creation, update, or verification
fails, show the error and stop without claiming success.

Report the PR number and title, URL, created or updated status, draft state,
commit count, and changed-file count.
