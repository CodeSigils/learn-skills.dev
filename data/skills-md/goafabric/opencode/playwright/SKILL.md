---
name: playwright
description: Drive a live browser with Playwright MCP tools — navigate pages, click, fill forms, take screenshots, inspect console/network, and diagnose UI issues interactively. Use this skill whenever a task involves opening a URL, interacting with a web page, capturing what a page looks like, debugging frontend behavior, or verifying UI state without running a full test suite.
---

# Playwright Browser Skill

Use the Playwright MCP tools to control a live browser session. These tools are available directly — no CLI, no `npx`, no test runner needed.

## Tool reference

| Tool | When to use |
|------|-------------|
| `browser_navigate` | Open a URL |
| `browser_snapshot` | Get accessibility tree + page state — use this before clicking to find element refs |
| `browser_take_screenshot` | Capture the viewport as an image |
| `browser_click` | Click an element (use ref from snapshot) or coordinates |
| `browser_type` | Type into the currently focused element |
| `browser_fill_form` | Fill multiple form fields at once |
| `browser_press_key` | Send a key event (Enter, Tab, Escape, ArrowDown, etc.) |
| `browser_hover` | Hover to reveal tooltips, dropdowns, or hover states |
| `browser_drag` | Drag from one point to another |
| `browser_select_option` | Choose a `<select>` option |
| `browser_wait_for` | Wait for a selector or condition before proceeding |
| `browser_evaluate` | Run JavaScript in the page context |
| `browser_console_messages` | Read browser console output (errors, warnings, logs) |
| `browser_network_requests` | Inspect HTTP requests/responses the page has made |
| `browser_navigate_back` | Go back in browser history |
| `browser_tabs` | List or switch between open tabs |
| `browser_resize` | Change the viewport dimensions |
| `browser_handle_dialog` | Accept or dismiss alert/confirm/prompt dialogs |
| `browser_file_upload` | Upload a file via `<input type="file">` |
| `browser_close` | Close the browser session when done |

## Standard workflow

1. **Navigate** — `browser_navigate` to the target URL.
2. **Snapshot first** — always call `browser_snapshot` before interacting so you have element refs and understand what's on screen. Never guess coordinates.
3. **Act** — use the appropriate tool from the table above.
4. **Confirm** — after each meaningful action, take a snapshot or screenshot to verify the result.
5. **Debug** — if something looks wrong, check `browser_console_messages` and `browser_network_requests` for errors before drawing conclusions.
6. **Close** — call `browser_close` when the session is no longer needed.

## Guidance for subagents including this skill

When another skill or subagent references this one, follow the workflow above and use the tool table as your reference. The caller will specify the URL and the actions to perform. Capture screenshots at each key step and surface any console errors or failed network requests in your report.
