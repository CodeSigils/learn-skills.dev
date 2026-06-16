---
name: createos
description: "Deploy apps, manage projects, configure environments, and add domains
  on CreateOS cloud platform. Use when the user wants to: deploy an app, host something,
  ship a project, go live, put something online, launch a site, publish an app,
  set up a staging environment, add a custom domain, or check deployment status.
  Integrates with opencode-createos plugin for tool-based interaction."
---

# CreateOS — Deployment Platform Skill

This skill helps you deploy and manage applications on CreateOS through opencode.

---

## Overview

CreateOS is a deployment platform that turns code into live applications.

**Key capabilities:**
- Create and manage projects (VCS from GitHub, upload, or Docker image)
- Deploy with one command
- Configure environment variables and secrets
- Add custom domains
- Monitor deployment status and logs

---

## Available Tools

If the `opencode-createos` plugin is installed, these tools are available:

### Deploy
| Tool | Description |
|------|-------------|
| `createos_deploy` | Deploy a project to CreateOS. Supports VCS (GitHub) and Upload modes. Creates project + environment + triggers first deployment. |

### Project Management
| Tool | Description |
|------|-------------|
| `createos_list_projects` | List all projects on the account with key metadata |
| `createos_get_project` | Get detailed project info + deployment status + environments |

### Environment Variables
| Tool | Description |
|------|-------------|
| `createos_set_env` | Set environment variables (merges with existing) |
| `createos_list_env` | List environment variables with truncated values |

### Domains
| Tool | Description |
|------|-------------|
| `createos_add_domain` | Add a custom domain + shows DNS setup instructions |
| `createos_list_domains` | List configured domains with status |

---

## Quick Start

### Prerequisites
1. CreateOS account at https://createos.nodeops.network
2. API key from Profile → API Keys
3. `export CREATEOS_API_KEY=your_key_here`

### First Deployment (Upload mode)
```
createos_deploy({
  projectName: "my-app",
  framework: "nextjs"
})
```

### First Deployment (VCS / GitHub)
```
// 1. List GitHub accounts:
=> ListConnectedGithubAccounts (MCP)

// 2. List repos for the account:
=> ListGithubRepositories("gh_12345")

// 3. Deploy:
createos_deploy({
  projectName: "my-app",
  type: "vcs",
  vcsInstallationId: "gh_12345",
  vcsRepoId: "repo_67890",
  framework: "nextjs"
})
```

---

## Deployment Patterns

### VCS (GitHub Auto-Deploy) — Recommended
Best for production apps. Every push to the branch auto-deploys.

1. Use `createos_deploy` with `type: "vcs"`, `vcsInstallationId`, and `vcsRepoId`
2. Poll `createos_get_project` until status is "ready"
3. Done — subsequent pushes auto-deploy

### Upload (File-based)
Best for quick demos, prototypes, or static sites.

1. Use `createos_deploy` with `type: "upload"`
2. Upload files via CreateOS MCP `UploadDeploymentFiles` tool
3. Poll `createos_get_project` for status

### Image (Docker)
For containerized apps.

1. Create project with `type: "image"` (via MCP or createos_deploy)
2. Use CreateOS MCP `CreateDeployment` with the image name
3. Monitor via `createos_get_project`

---

## Environment Management

### Set Variables
```
createos_set_env({
  projectId: "proj_abc123",
  envVars: {
    DATABASE_URL: "postgresql://user:pass@host:5432/db",
    NODE_ENV: "production"
  },
  environmentName: "production"
})
```

### Security Rules
- ❌ Never log or display secret env var values in output
- ❌ Never write secrets to files
- 🔒 Always mask values in responses
- 👤 Ask the user to paste sensitive values directly into the tool call

---

## Domain Configuration

### Add a Custom Domain
```
createos_add_domain({
  projectId: "proj_abc123",
  domain: "example.com",
  environmentName: "production"
})
```

### DNS Setup (guide the user)
1. Add a CNAME record at their DNS provider:
   - **Name:** `@` (root) or `www`
   - **Target:** `[project-name].createos.nodeops.network`
   - **TTL:** 300 or Auto
2. Wait 5-30 minutes for propagation
3. Keep old DNS records active until verified

### Verify
```
createos_list_domains({ projectId: "proj_abc123" })
```
Status should show "active".

---

## Troubleshooting

| Issue | Likely Cause | Solution |
|-------|-------------|----------|
| Build fails | Wrong runtime/framework | Check build logs via `GetBuildLogs` MCP, retry with explicit `installCommand`/`buildCommand` |
| Deployment stuck | Build taking long | Poll `createos_get_project` every 10s, max 5 min |
| `CreateOS_API_KEY not set` | Missing env var | Run `export CREATEOS_API_KEY=your_key` before opencode |
| Environment not found | Wrong `environmentName` | Use `createos_get_project` to list available environments |
| Domain not resolving | DNS not propagated | Use `RefreshDomain` MCP tool, check DNS records |
| VCS deployment fails | GitHub not connected | Guide user to install GitHub app in CreateOS dashboard |
| Rate limited | Too many API calls | Wait 60 seconds and retry |
