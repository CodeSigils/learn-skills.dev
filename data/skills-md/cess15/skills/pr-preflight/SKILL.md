---
name: pr-preflight
description: Parses PR URLs into structured data and validates environment readiness (git, MCP configuration, git_identity). Runs inline in orchestrator context.
---

# pr-preflight skill

**Single Responsibility:** Parse PR URL + validate environment. Return structured JSON.

## Input

Receive PR URL string. Example: `https://bitbucket.org/workspace/repo/pull-requests/123`

## What you do

### 1. Parse URL

Supported patterns (regex):
```
github.com/<org>/<repo>/pull/<id>
gitlab.com/<group>[/<subgroup>...]/<repo>/-/merge_requests/<id>
bitbucket.org/<workspace>/<repo_slug>/pull-requests/<id>
```

Extract: domain, workspace (org/group), repo_slug, pr_number.

### 2. Identify provider

```
"github"    in domain → provider="github",    mcp_server="github-mcp-server"
"gitlab"    in domain → provider="gitlab",    mcp_server="gitlab-mcp-server"
"bitbucket" in domain → provider="bitbucket", mcp_server="mcp-server-atlassian-bitbucket"
```

### 3. Validate environment

Use Bash tool:
- `which git` — confirm git available
- `git config --global user.name` and `user.email` — get reviewer identity
- MCP availability: check tool list for provider-specific tool name:
  - `bitbucket` → look for `mcp__bitbucket__bb_get`
  - `github` → look for `mcp__github__` prefix
  - `gitlab` → look for `mcp__gitlab__` prefix
  - If tool not found: set `mcp_available: false`, add warning `MCP_SERVER_NOT_CONFIGURED`

## Output (JSON only)

`status` enum: `"SUCCESS"` | `"BLOCK"` | `"FAILURE"` — see Status rules.

```json
{
  "agent_name": "pr-preflight",
  "version": "1.0",
  "status": "SUCCESS",
  "parsed_data": {
    "domain": "bitbucket.org",
    "provider": "bitbucket",
    "workspace": "acme",
    "repo_slug": "web-app",
    "pr_number": 123,
    "mcp_server": "mcp-server-atlassian-bitbucket"
  },
  "environment": {
    "git_available": true,
    "git_version": "2.40.0",
    "mcp_available": true,
    "git_identity": {
      "name": "John Doe",
      "email": "john@example.com"
    }
  },
  "errors": []
}
```

## Error cases

Status rules:
- `BLOCK` — hard failure, pipeline must stop (git missing, invalid URL, MCP not configured)
- `FAILURE` — partial/ambiguous failure (git identity missing but git present)
- `SUCCESS` — all checks pass

**Git not available:**
```json
{
  "status": "BLOCK",
  "errors": [{"code": "GIT_NOT_FOUND", "message": "Git not installed", "fix": "Install git"}]
}
```

**Invalid URL:**
```json
{
  "status": "BLOCK",
  "errors": [{"code": "INVALID_URL_PATTERN", "message": "URL matches no supported pattern", "provided": "..."}]
}
```

**CRITICAL:** Return ONLY valid JSON. No markdown fences. No explanations.
On catastrophic failure (cannot construct output): emit `{"status":"BLOCK","errors":[{"code":"INTERNAL_ERROR","message":"<reason>"}]}`.
