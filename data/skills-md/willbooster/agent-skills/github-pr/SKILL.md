---
name: github-pr
description: Use for GitHub pull request workflows, especially opening PRs, checking GitHub Actions status for the latest workflow results, reviewing unresolved comments, and replying to review threads.
allowed-tools: Bash(gh:*), Bash(git:*), Bash(ruby:*)
---

# GitHub PR Operations

## Open a pull request

```bash
ruby scripts/create_pull_request.rb <<'EOF'
Summary of the change
EOF
```

## Check whether the latest test workflows for the current PR succeeded

```bash
ruby scripts/show_test_ci_results.rb
```

The script can take up to 1 hour, so set the timeout to 1 hour.
It classifies the latest result of each workflow as `successful`, `running`, or `failed`.

## Fetch unresolved review threads for a PR

```bash
ruby scripts/list_unresolved_review_threads.rb
```

## Reply to unresolved review threads and resolve them

```bash
ruby scripts/reply_and_resolve_review_threads.rb <<'EOF'
{
  "replies": {
    "PRRT_kwDORiWJ-851nXBt": "Fixed in the latest update.",
    "PRRT_kwDORiWJ-851nXBu": "Kept as-is intentionally. Added clarification in the code."
  }
}
EOF
```

The JSON object must contain `replies`, keyed by review thread ID.

## Notes

- Run the scripts from the repository that owns the PR you want to inspect.
- Run `git commit` and `git push` sequentially to avoid conflicts
