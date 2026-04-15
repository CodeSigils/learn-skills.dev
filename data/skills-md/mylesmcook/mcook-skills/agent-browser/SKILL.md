---
name: agent-browser
description: Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task. Triggers include requests to "open a website", "fill out a form", "click a button", "take a screenshot", "scrape data from a page", "test this web app", "login to a site", "automate browser actions", or any task requiring programmatic web interaction.
allowed-tools: Bash(npx agent-browser:*), Bash(agent-browser:*)
---

# Browser Automation with agent-browser

Use `agent-browser` when the browser itself is the work surface: local dev QA, auth flows, CRUD verification, scraping, screenshots, or reproducing UI issues.

On this machine:

- install or update with `vp install -g agent-browser@latest`
- verify with `agent-browser --version`
- run `agent-browser install` after install or upgrade to pin Chrome for Testing locally
- prefer the PowerShell-safe patterns in [references/windows-powershell.md](references/windows-powershell.md)

## Fast Rules

1. Give every task or scenario its own `AGENT_BROWSER_SESSION`. Name it `<run-id>-<scenario>`.
2. Refs are session-local and page-local. Never reuse `@e...` across sessions. Re-snapshot after navigation or DOM changes.
3. In PowerShell, quote refs: `agent-browser click '@e1'`. Do not use Bash-style `&&`.
4. Use this locator ladder: fresh refs, re-snapshot, semantic `find`, CSS selector, keyboard fallback.
5. For dialogs, popovers, comboboxes, sheets, and menus: open first, then snapshot the live subtree before the next action.
6. For mutations, clear the network log, perform the action, wait, inspect requests, then capture URL, title, errors, and a screenshot.
7. Prefer URL or element waits. Use `wait --load networkidle` only on pages whose activity actually settles.
8. Run interactive QA serially on one machine. Parallel sessions are fine for light scraping, but they add noise to mutation-heavy testing.
9. Use `--session-name` or `AGENT_BROWSER_SESSION_NAME` only when you intentionally want cookies and localStorage restored across runs.

## PowerShell Quick Start

```powershell
$runId = "probe-$(Get-Date -Format yyyyMMdd-HHmmss)"
$env:AGENT_BROWSER_SESSION = "$runId-login"

agent-browser open https://example.com/login
agent-browser snapshot -i --json
agent-browser fill '@e1' 'user@example.com'
agent-browser fill '@e2' 'password'
agent-browser click '@e3'
agent-browser wait 1500
agent-browser get url
agent-browser screenshot
agent-browser errors
```

## Standard Workflow

1. Open the route or page you actually want to validate.
2. Take `snapshot -i --json` if the next action depends on refs.
3. Interact using fresh refs.
4. Re-snapshot after anything that changes the DOM or active route.
5. For mutations, verify with `network requests`, `errors`, `console`, and a screenshot.
6. Restore baseline state before leaving the scenario unless the data is intentionally disposable.

## Local Dev Apps

For local web-app testing, use `agent-browser` as the primary browser executor and keep the app bootstrap outside the browser.

- start the app first, then test it
- use one session per scenario such as `cresa-ab-<run-id>-events`
- capture at least one screenshot per scenario
- record final URL, title, and page errors
- validate route correctness before treating a blank page as an agent-browser failure

Use [references/local-dev-e2e.md](references/local-dev-e2e.md) for the full pattern.

## Locator Strategy

Start with refs from a fresh snapshot. If the click or fill no-ops:

1. re-snapshot
2. retry with the new ref
3. use `find role`, `find text`, or `find label`
4. fall back to a CSS selector when the semantic target is stable
5. if a dialog submit still no-ops, try `focus` plus `press Enter`

Use [references/snapshot-refs.md](references/snapshot-refs.md) and [references/evidence-triage.md](references/evidence-triage.md) for the deeper workflow.

## Auth Choices

Use the simplest auth pattern that fits:

- one-off reuse of an already logged-in browser: state export or auto-connect
- recurring automation: `--profile` or `--session-name`
- secure stored credentials: auth vault

Details live in [references/authentication.md](references/authentication.md).

## Deep-Dive References

| Reference | Use When |
| --- | --- |
| [references/windows-powershell.md](references/windows-powershell.md) | PowerShell quoting, session env vars, and Windows shell behavior |
| [references/local-dev-e2e.md](references/local-dev-e2e.md) | Local app smoke tests, CRUD passes, mobile passes, and artifact capture |
| [references/evidence-triage.md](references/evidence-triage.md) | Verifying mutations, diagnosing no-op clicks, and collecting evidence |
| [references/snapshot-refs.md](references/snapshot-refs.md) | Ref lifecycle, dynamic widgets, and stale-ref recovery |
| [references/session-management.md](references/session-management.md) | Session isolation, persistence, and cleanup |
| [references/authentication.md](references/authentication.md) | Login flows, state reuse, OAuth, and 2FA handling |
| [references/commands.md](references/commands.md) | Command reference and less-common CLI options |
| [references/video-recording.md](references/video-recording.md) | Recording workflows for demos and bug reports |
| [references/profiling.md](references/profiling.md) | Performance and trace capture |
| [references/proxy-support.md](references/proxy-support.md) | Proxy and geo-testing configuration |

## Templates

| Template | Description |
| --- | --- |
| [templates/powershell-session.ps1](templates/powershell-session.ps1) | Create an isolated PowerShell session and run a small command block |
| [templates/local-dev-smoke.ps1](templates/local-dev-smoke.ps1) | Open a local app route, snapshot it, and capture evidence |
| [templates/crud-scenario.md](templates/crud-scenario.md) | Reusable CRUD scenario checklist with restore steps |
| [templates/form-automation.sh](templates/form-automation.sh) | Basic form filling flow |
| [templates/authenticated-session.sh](templates/authenticated-session.sh) | Login once and reuse saved state |
| [templates/capture-workflow.sh](templates/capture-workflow.sh) | Content extraction with screenshots |
