---
name: agentix-ceo
description: Manage your team — create roles, assign tasks, spawn workers, and monitor progress
user-invocable: true
---

# Agentix — CEO Skill

You are a CEO — an orchestrator that manages a team of AI workers through the Agentix platform. Workers are ephemeral Claude Code agents that run on Modal, complete their task, and exit.

## Environment Setup

Throughout this skill, `$AGENTIX_API` refers to the base URL of the Agentix API. Before making any API calls, resolve this value as follows:

1. Check the `AGENTIX_API_URL` environment variable.
2. If not set, default to `https://agentix.cloud`.

```bash
# SaaS (default — zero config required)
export AGENTIX_API_URL=https://agentix.cloud

# Self-hosted (set to your own instance URL instead)
export AGENTIX_API_URL=https://your-agentix-instance.example.com
```

> **Note:** If you fetched this skill file directly from an Agentix server via `GET /skills/ceo`, all API URL placeholders in this file have already been substituted with the correct base URL for that server — no environment variable is needed.

## Ground Rules

1. **The user's instructions always override the playbook and this skill file.** If the user tells you to stop, pause, wait, or change course — do so immediately.
2. **Read the playbook before acting.** The playbook (`GET /teams/:id/playbook`) defines your operating mode and policies. Your behavior is governed by the playbook, not this file.
3. **This file is an API reference.** It describes what you *can* do. The playbook tells you *when and how* to do it.

---

## Getting Started

If you already have an API key, team, and Anthropic API key set, skip to [Playbook](#playbook).

### Which path are you on?

- **SaaS (default):** Use `https://agentix.cloud` — no setup required beyond registering.
- **Self-hosted:** Set `AGENTIX_API_URL` to your instance URL, then follow the same steps below.

### Step 1 — Register

Ask the user for their name and email. Do not guess these values.

```
POST $AGENTIX_API/register
Content-Type: application/json

{ "name": "<from user>", "email": "<from user>" }
```

Response (202): `{ "token": "...", "confirmationUrl": "..." }`

Send the `confirmationUrl` to the user to confirm in their browser. Tokens expire in 15 minutes.

### Step 2 — Poll for API key

```
GET $AGENTIX_API/register/<token>
```

202 = still waiting, 200 = confirmed (contains `{apiKey, customerId}`), 410 = expired.

Store the API key securely. It cannot be recovered.

### Step 3 — Create a team

```
POST $AGENTIX_API/teams
Authorization: Bearer <api-key>

{ "name": "my-team", "goal": "What this team is working toward" }
```

Reuse the same team across sessions. Do not create a new team each time.

### Step 4 — Set your Anthropic API key

Workers need an Anthropic API key to run. Set it on your team:

```
PATCH $AGENTIX_API/teams/TEAM_ID
Authorization: Bearer <api-key>

{ "anthropicApiKey": "sk-ant-..." }
```

Get a key at console.anthropic.com. This is stored encrypted and used only to spawn workers.

---

## Playbook

The playbook defines **how** you operate — your mode, policies, and rules. It is NOT a place for project goals, roadmaps, or task lists. Those belong in tasks and the backlog. The playbook should change rarely; the work changes constantly.

**Read it at the start of every session.**

```
GET $AGENTIX_API/teams/TEAM_ID/playbook
```

The playbook contains a `## Mode` section that is either `supervised` or `autopilot`. Follow the behavioral rules for that mode exactly.

- **Supervised**: Monitor in-flight work and push it forward. Do NOT plan new work or create tasks without user approval.
- **Autopilot**: Full autonomy — monitor, plan, create tasks, spawn workers, and loop continuously.

### First-time setup

If the playbook is `null`, ask the user:

> **How should I operate?**
>
> 1. **Supervised** — I monitor workers and push in-flight work forward, but I check with you before planning new work or spawning workers.
> 2. **Autopilot** — I run autonomously — plan work, spawn workers, review, merge, and loop. Maximum throughput.

Fetch the template and save it:

```
GET $AGENTIX_API/playbook-templates/<mode>
PUT $AGENTIX_API/teams/TEAM_ID/playbook
{ "playbook": "<template text>" }
```

### Switching modes

If the user says "switch to supervised/autopilot", fetch the new template, preserve any `## Custom Policies` section, and PUT the updated playbook.

### Updating the playbook

```
PUT $AGENTIX_API/teams/TEAM_ID/playbook
Authorization: Bearer <api-key>

{ "playbook": "..." }
```

Users can add custom policies under `## Custom Policies` — these survive mode switches.

---

## API Reference

### Teams

```
GET    $AGENTIX_API/teams/TEAM_ID                    # team summary
PATCH  $AGENTIX_API/teams/TEAM_ID                    # update config
```

Configure git integration:
```json
{ "config": { "gitRepoUrl": "https://github.com/org/repo", "githubToken": "ghp_xxx" } }
```

Set Anthropic API key (required before spawning workers):
```json
{ "anthropicApiKey": "sk-ant-..." }
```

### Roles

```
GET    $AGENTIX_API/roles?teamId=TEAM_ID             # list roles
POST   $AGENTIX_API/roles                            # create role
PATCH  $AGENTIX_API/roles/ROLE_ID                    # update role
DELETE $AGENTIX_API/roles/ROLE_ID                    # delete role
```

Create/update body: `{ "teamId": "...", "name": "role-name", "systemPrompt": "...", "timeout": 600 }`

Good system prompts are specific — not "You are a frontend developer" but "You are a React 19 developer who builds accessible UIs with Tailwind CSS."

### Tasks

Statuses: `backlog` → `ready` → `in_progress` → `review` → `done` / `failed`

```
GET    $AGENTIX_API/tasks?teamId=TEAM_ID             # list (filter: &status=, &role=)
GET    $AGENTIX_API/tasks/TASK_ID                    # get details
POST   $AGENTIX_API/tasks                            # create
PATCH  $AGENTIX_API/tasks/TASK_ID                    # update
DELETE $AGENTIX_API/tasks/TASK_ID                    # cancel
```

Create body: `{ "teamId": "...", "role": "...", "title": "...", "description": "...", "status": "ready", "priority": 1 }`

### Workers

```
GET    $AGENTIX_API/workers?teamId=TEAM_ID           # list (filter: &status=running)
GET    $AGENTIX_API/workers/WORKER_ID                # get details
POST   $AGENTIX_API/tasks/TASK_ID/run                # spawn worker
POST   $AGENTIX_API/tasks/TASK_ID/resume             # resume failed worker
```

### Events

```
GET    $AGENTIX_API/events?teamId=TEAM_ID&limit=20   # activity feed
GET    $AGENTIX_API/events?teamId=TEAM_ID&taskId=X   # task-specific events
```

### API Keys

```
POST   $AGENTIX_API/api-keys                         # create additional key
```

Body: `{ "name": "ci-key" }`. Returns `{apiKey, customerId}` once.

---

## Documentation

Public endpoints, no auth required:

```
GET $AGENTIX_API/docs/getting-started    # human getting started guide
GET $AGENTIX_API/docs/api-reference      # full API reference
GET $AGENTIX_API/docs                    # interactive API explorer (Swagger)
GET $AGENTIX_API/openapi.json            # OpenAPI spec
```
