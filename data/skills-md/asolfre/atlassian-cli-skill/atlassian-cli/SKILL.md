---
name: atlassian-cli
description: >
  Use this skill when the user wants to execute Atlassian operations from the terminal using the
  `acli` command-line tool. Trigger when the user wants to actually run commands against Jira or
  Confluence (create issues, transition work items, search with JQL, manage sprints, export data,
  bulk operations), set up acli authentication or CI pipeline integration, or use Rovo Dev or
  Atlassian admin user management via CLI. Do NOT trigger for: conceptual questions about
  Jira/Confluence configuration (board columns, workflow design, SSO setup), general Atlassian best
  practices, reading web URLs, or writing custom API scripts in Python/etc. The key signal is intent
  to run terminal commands against Atlassian — not just discuss, design, or understand Atlassian
  products.
---

# Atlassian Cloud CLI (acli)

The Atlassian CLI (`acli`) is the official command-line tool for interacting with Atlassian Cloud
products. It lets you manage Jira work items, Confluence spaces, Rovo Dev sessions, and
organization-level user administration directly from the terminal.

This skill teaches you how to use `acli` to execute real commands on behalf of the user. You will
construct commands, execute them via bash, and present results back to the user.

## Prerequisites

- `acli` must be installed. On macOS: `brew tap atlassian/homebrew-acli && brew install acli`
- The user must be authenticated before running product commands. Check with `acli auth status` or
  the product-specific `acli <product> auth status`.
- For full auth details (OAuth, API tokens, API keys, CI setup), read `references/auth.md`.

## Command Structure

Every `acli` command follows this pattern:

```
acli <PRODUCT> <ENTITY> <ACTION> [FLAGS]
```

- **PRODUCT**: `jira`, `confluence`, `rovodev`, `admin`
- **ENTITY**: What you're acting on (e.g., `workitem`, `project`, `space`, `user`)
- **ACTION**: What you're doing (e.g., `create`, `search`, `edit`, `view`, `delete`)
- **FLAGS**: Parameters controlling the action (e.g., `--summary`, `--jql`, `--json`)

Some commands have deeper nesting. For example, comments on a work item:

```
acli jira workitem comment create --key "KEY-1" --body "This is a comment"
```

When in doubt about available subcommands or flags, run `acli <partial-command> --help`.

## Execution Workflow

When the user asks you to do something with Atlassian, follow this sequence:

### 1. Check authentication

Before running any product command, verify the user is authenticated:

```bash
acli auth status
```

Or for a specific product:

```bash
acli jira auth status
acli confluence auth status
```

If not authenticated, guide the user through login. See `references/auth.md` for details.

### 2. Construct the command

Build the `acli` command using the correct product, entity, action, and flags. Use the reference
files for exact flag names when needed:

- Jira commands: read `references/jira.md`
- Confluence commands: read `references/confluence.md`
- Admin commands: read `references/admin.md`
- Auth commands: read `references/auth.md`

### 3. Apply safety tier

Before executing, determine which safety tier the command falls into:

**Safe -- execute immediately, no confirmation needed:**
- Read-only operations: `search`, `list`, `view`, `get`, `auth status`
- These never modify data, so run them freely and present results.

**Moderate -- tell the user what you'll run, get confirmation first:**
- Data-creating or modifying operations: `create`, `edit`, `assign`, `transition`,
  `comment create`, `link create`, `sprint create`, `clone`, `update`
- These change data but are generally reversible. Show the exact command, ask the user
  to confirm, then execute.

**Dangerous -- show the command AND preview the impact, require explicit confirmation:**
- Destructive or high-impact operations: `delete`, `archive`, `admin user deactivate`,
  `admin user delete`, any bulk operation targeting multiple items via `--jql` or `--filter`
- Never auto-pass `--yes` on these. Always show what will be affected first.
  For bulk operations, consider running a `search` or `list` first to show the user
  how many items will be impacted before proceeding.

### 4. Execute and present results

Run the command via bash. Then:

- For tabular output, present it in a readable format to the user.
- When you need to parse output for a follow-up step, use `--json` and extract fields with `jq`.
- For large result sets, summarize key information rather than dumping raw output.
- On errors, read the error message and suggest a fix (expired auth, wrong key, missing flags, etc.).

## Core Workflows

### Jira: Work Items

The most common operations. "Work item" is acli's term for what Jira calls issues (tasks, bugs,
stories, epics, etc.).

**Create a work item:**
```bash
acli jira workitem create --summary "Fix login bug" --project "TEAM" --type "Task" --assignee "@me"
```

**Search with JQL:**
```bash
acli jira workitem search --jql "project = PROJ AND status = 'To Do' AND type = Bug" --limit 50
```

**View a specific work item:**
```bash
acli jira workitem view KEY-123
```

**Edit a work item:**
```bash
acli jira workitem edit --key "KEY-123" --summary "Updated summary" --assignee "user@example.com"
```

**Transition (change status):**
```bash
acli jira workitem transition --key "KEY-123" --status "In Progress"
```

**Add a comment:**
```bash
acli jira workitem comment create --key "KEY-123" --body "Working on this now"
```

**Bulk edit via JQL** (dangerous tier -- confirm with user first):
```bash
acli jira workitem edit --jql "project = TEAM AND status = 'To Do'" --assignee "user@example.com"
```

For the full Jira command reference with every flag, read `references/jira.md`.

### Jira: Projects, Boards, Sprints

**List projects:**
```bash
acli jira project list --limit 50
```

**View a project:**
```bash
acli jira project view --key "TEAM"
```

**Search boards:**
```bash
acli jira board search --project "TEAM" --type scrum
```

**Create a sprint:**
```bash
acli jira sprint create --name "Sprint 5" --board 10 --start 2025-06-01 --end 2025-06-14
```

**List work items in a sprint:**
```bash
acli jira sprint list-workitems --sprint 42 --board 10
```

### Confluence: Spaces, Pages, Blogs

**List spaces:**
```bash
acli confluence space list
```

**View a space:**
```bash
acli confluence space view --id 123456 --json
```

**Create a space:**
```bash
acli confluence space create --key "ENG" --name "Engineering Docs" --private
```

**View a page:**
```bash
acli confluence page view --id 789012 --body-format storage
```

**Create a blog post:**
```bash
acli confluence blog create --space-id 123456 --title "Release Notes v2.1" --body "<p>Content</p>"
```

**List blog posts:**
```bash
acli confluence blog list --space-id 123456 --limit 10
```

For the full Confluence command reference, read `references/confluence.md`.

### Admin: User Management

Admin commands require a separate API key (not the same as Jira/Confluence auth).
See `references/auth.md` for admin authentication.

**Activate users:**
```bash
acli admin user activate --email "john@example.com,anna@example.com"
```

**Deactivate users** (dangerous tier):
```bash
acli admin user deactivate --email "john@example.com"
```

**Delete a managed account** (dangerous tier):
```bash
acli admin user delete --email "user@example.com"
```

**Cancel a pending deletion:**
```bash
acli admin user cancel-delete --email "user@example.com"
```

For the full admin command reference, read `references/admin.md`.

### Rovo Dev

Rovo Dev is Atlassian's AI coding agent (Beta). It uses its own scoped API token.

**Authenticate:**
```bash
acli rovodev auth login --email "user@example.com" --token < token.txt
```

**Start an interactive session:**
```bash
acli rovodev run
```

**Check status:**
```bash
acli rovodev auth status
```

See `references/auth.md` for Rovo Dev authentication details.

## Automation Patterns

### Output Formats

Most commands support `--json` and many support `--csv`:

```bash
# JSON output (useful for programmatic parsing with jq)
acli jira workitem search --jql "project = TEAM" --limit 10 --json

# CSV output (useful for spreadsheets and data export)
acli jira workitem search --jql "project = TEAM" --csv

# Redirect to a file
acli jira workitem search --jql "project = TEAM" --csv > issues.csv
```

### Extracting Specific Data with jq

When you need to pull specific fields from JSON output:

```bash
# Get just the summary of an issue
acli jira workitem view KEY-123 --json | jq '.fields.summary'

# Get keys of all matching issues
acli jira workitem search --jql "project = TEAM" --json | jq '.[].key'
```

### Command Chaining

Chain commands with `&&` for sequential execution:

```bash
acli jira workitem create --summary "New task" --project "TEAM" --type "Task" && echo "Created successfully"
```

### Piping Output

Filter results with standard Unix tools:

```bash
acli jira workitem search --jql "project = TEAM" | grep "In Progress"
```

### Bulk Operations from Files

For large-scale operations, use `--from-json`, `--from-csv`, or `--from-file`:

```bash
# Bulk create from CSV
acli jira workitem create-bulk --from-csv issues.csv

# Bulk create from JSON
acli jira workitem create-bulk --from-json issues.json

# Generate example JSON structure
acli jira workitem create-bulk --generate-json

# Delete items listed in a file
acli jira workitem delete --from-file issue-keys.txt
```

### Pagination

For large result sets, use `--paginate` to fetch all pages automatically:

```bash
acli jira workitem search --jql "project = TEAM" --paginate
acli jira project list --paginate
```

Or use `--limit` to cap results:

```bash
acli jira workitem search --jql "project = TEAM" --limit 100
```

## Common Flags Cheat Sheet

| Flag | Description | Available on |
|---|---|---|
| `--json` | Output as JSON | Most commands |
| `--csv` | Output as CSV | `search`, `list`, `board search`, `filter search`, `dashboard search` |
| `--yes` / `-y` | Skip confirmation prompts | `edit`, `delete`, `archive`, `transition`, `assign`, `clone` |
| `--paginate` | Fetch all pages of results | `search`, `list` |
| `--limit` / `-l` | Max items to return | `search`, `list` |
| `--jql` / `-j` | JQL query to target items | `search`, `edit`, `delete`, `transition`, `assign`, `archive` |
| `--filter` | Filter ID to target items | `search`, `edit`, `delete`, `transition`, `assign`, `archive` |
| `--key` / `-k` | Work item key(s), comma-separated | `edit`, `delete`, `transition`, `assign`, `archive`, `clone` |
| `--from-file` / `-f` | Read input from a file | `create`, `delete`, `assign`, `archive` |
| `--from-json` | Read structured input from JSON | `create`, `edit`, `create-bulk`, `link create` |
| `--generate-json` | Generate example JSON template | `create`, `edit`, `create-bulk`, `link create` |
| `--ignore-errors` | Continue on errors in bulk ops | Most bulk operations |
| `--web` / `-w` | Open result in browser | `view`, `search`, `auth login` |
| `--fields` / `-f` | Select specific fields to display | `view`, `search` |

## Error Handling

When a command fails, `acli` provides:

- **Expected errors**: A clear error message describing the issue (wrong key, missing field, auth expired).
- **Unexpected errors**: A trace ID (e.g., `trace id: XXXXXXXX`) for Atlassian support.
- **Bulk operation errors**: Individual trace IDs for each failed item.

Common issues and fixes:

| Error pattern | Likely cause | Fix |
|---|---|---|
| "authenticate your Atlassian account" | Not logged in | Run `acli <product> auth login` |
| "no project found" or "project does not exist" | Wrong project key | Run `acli jira project list` to find correct key |
| "Field 'X' does not exist" | Invalid field name | Check field names with `acli jira field` commands |
| "Transition is not valid" | Invalid status name for that workflow | View the issue first to see available transitions |
| Permission errors | User lacks permissions | Check permissions in Jira/Confluence admin |

For general troubleshooting, you can also submit feedback:

```bash
acli feedback --summary "Problem description" --email "user@example.com" --details "More context"
```

## Reference Files

When you need exact flags and full syntax for a specific command, consult:

- **`references/jira.md`** -- All Jira commands: workitem, project, board, sprint, filter, dashboard, field
- **`references/confluence.md`** -- All Confluence commands: page, space, blog
- **`references/admin.md`** -- Admin user management: activate, deactivate, delete, cancel-delete
- **`references/auth.md`** -- All authentication methods: global OAuth, Jira/Confluence token auth, admin API key auth, Rovo Dev scoped token, CI pipeline setup

Read the relevant reference file whenever you need to look up the exact flag name, short form, or
behavior for a less common command. The SKILL.md you're reading now covers the most common
workflows; the reference files cover everything.
