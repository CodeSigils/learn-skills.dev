---
name: tabbit-devtools
description: Use Tabbit instead of Chrome by reading Tabbit's live DevToolsActivePort file and connecting to the browser WebSocket endpoint. Trigger when the user says things like "用我的 tabbit 浏览器", "在 Tabbit 里", "Tabbit 当前页", "Tabbit 当前标签", or asks to inspect, summarize, scrape, or debug a page that is open in Tabbit rather than the default Chrome DevTools session. Default to the lightweight local Python script for current-page extraction instead of requiring an extra custom MCP server.
---

# Tabbit Devtools

Prefer this skill whenever the request is explicitly about Tabbit or includes phrases like `用我的 tabbit 浏览器`, `在 Tabbit 里`, `Tabbit 当前页`, or `Tabbit 当前标签`.

## Quick Path

1. Read `~/Library/Application Support/Tabbit/DevToolsActivePort` first.
2. Use both lines in that file:
   - line 1: TCP port
   - line 2: browser path such as `/devtools/browser/<id>`
3. Build the full browser endpoint as `ws://127.0.0.1:<port><path>`.
4. Prefer that `wsEndpoint` over `http://127.0.0.1:<port>`. Tabbit may expose the browser WebSocket while `/json/version` and `/json/list` still return `404`.
5. For lightweight requests such as “读取当前页面内容”, use [scripts/read_current_tabbit_page.py](scripts/read_current_tabbit_page.py) with `python3`.
6. The helper script keeps a local daemon and reuses the same browser WebSocket by default, so Tabbit should only ask for permission on the first connection after the daemon starts.
7. Prefer the explicit three-step flow for the first connection:
   - `--start-connect` to begin background connection
   - `--status` every 5 seconds until status becomes `connected`
   - `--read-if-connected` once the channel is ready
8. Do not require a dedicated custom MCP server for the default path.

## Workflow

1. For content-reading requests, start with [scripts/read_current_tabbit_page.py](scripts/read_current_tabbit_page.py) `--start-connect`.
2. If the result is `connecting`, wait about 5 seconds and run the same script with `--status`.
3. Once status is `connected`, run the script with `--read-if-connected`.
4. Only use the default no-flag invocation when a one-command path is specifically more convenient than the explicit polling flow.
5. The helper script already lists browser `page` targets and identifies the active Tabbit page.
6. Prefer `document.hasFocus() === true` or `document.visibilityState === "visible"` when deciding which page is current.
7. Ignore `chrome://` and extension pages unless the user explicitly wants the remote-debugging page or internal settings.
8. For “查看 Tabbit 当前页面上的内容”, extract the page title, URL, major visible text blocks, and primary links before summarizing.
9. For list or commerce pages, prefer a JSON array of objects. For article or detail pages, prefer an object like `{ title, url, summary, content }`.
10. If the current visible page is the remote-debugging page itself, tell the user that Tabbit is currently focused on that page and ask them to switch tabs if they want another page inspected.

## Extraction Guidance

- For “当前页面内容”, default to the smallest useful JSON payload instead of dumping the whole DOM.
- Prefer the bundled local Python script for current-page extraction because it has the lowest installation cost, reuses a local long-lived connection, and does not require a dedicated Tabbit MCP server.
- Prefer the explicit `--start-connect` / `--status` / `--read-if-connected` flow when the connection may still be awaiting Tabbit approval.
- Return structured JSON first, then summarize for the user.
- Keep the default path focused on current-page reading rather than the full DevTools feature set.

## Constraints

- Do not assume a dedicated `tabbit-devtools` MCP server exists.
- Do not assume the generic `chrome-devtools` session is already pointed at Tabbit.
- If the task only needs current-page content, use the local Python helper instead of asking the user to install another MCP server.
- The helper script defaults to daemon-backed connection reuse; only use `--direct` when the user explicitly wants a fresh one-shot connection or is debugging the helper itself.
- Do not automatically fall back to `--direct` after a slow first connection, because that defeats connection reuse and can retrigger Tabbit's allow dialog.
- If the first connection is waiting on Tabbit approval, keep polling `--status` instead of claiming the script is still running after the command has already exited.
- If the task needs the full DevTools tool surface, tell the user this skill's default path is intentionally lightweight and may need a separately configured DevTools setup.

## Resources

- Setup and direct-connection notes: [references/setup.md](references/setup.md)
- Endpoint discovery rules and environment variables: [references/discovery.md](references/discovery.md)
- Lightweight current-page reader: [scripts/read_current_tabbit_page.py](scripts/read_current_tabbit_page.py)
