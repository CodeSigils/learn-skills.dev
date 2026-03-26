---
name: screenshot
description: Universal screenshot tool for capturing web pages, desktop apps, and images. Supports viewport presets (mobile/tablet/desktop), CSS selectors, batch capture, auto-upload to image hosts, and markdown output for PRs. Use when user says "take a screenshot", "screenshot this", "capture the page", "screenshot of [app/url]", "batch screenshots", "all viewports", or "upload screenshot".
allowed-tools:
  - Bash(python3 */screenshot/scripts/*.py *)
  - Bash(python3 */screenshot/scripts/adapters/*.py *)
  - Bash(npx @playwright/mcp playwright-cli *)
  - Bash(npx playwright-cli *)
  - Bash(playwright-cli *)
  - Bash(which playwright-cli)
  - Bash(npm install -g @playwright/mcp@latest)
  - Bash(screencapture *)
  - Bash(scrot *)
  - Bash(gnome-screenshot *)
  - Bash(import *)
  - Bash(sips *)
  - Bash(convert *)
  - Bash(curl -s *)
  - Bash(pbcopy)
  - Bash(gh gist create *)
  - Bash(which *)
  - Bash(command -v *)
---

# Universal Screenshot Skill

A unified screenshot tool that captures any source (web, desktop, images) with viewport presets, element targeting, batch capture, and auto-upload.

## Agent Behavior Rules

**DO:**
- Detect source type automatically from input (URL, app name, file path)
- Use `--mobile`, `--tablet`, or `--desktop` for web captures
- Wait for `networkidle` before capturing web pages
- Use `--markdown` when user wants output for PRs or docs
- Use `--upload` when user wants shareable links
- Run pre-flight checks before first capture

**DO NOT:**
- Assume viewport without user context (default to desktop for web)
- Use `--full` unless explicitly asked for full-page/scroll capture
- Skip the networkidle wait on dynamic pages
- Upload without asking if destination is unclear

## Source Detection

| Input Pattern | Source Type | Tool Used |
|---------------|-------------|-----------|
| `http://`, `https://`, `file://` | Web | playwright-cli |
| App name (e.g., "Figma", "Xcode") | Desktop | OS screenshot |
| `.png`, `.jpg`, `.pdf` path | Image | sips/ImageMagick |
| Figma URL (`figma.com/...`) | Figma | Web capture |

## Quick Reference

```bash
# Set skill path
export SCREENSHOT_SKILL="$HOME/.claude/skills/screenshot"

# Basic web capture
python3 "$SCREENSHOT_SKILL/scripts/screenshot.py" https://example.com

# Mobile viewport with selector
python3 "$SCREENSHOT_SKILL/scripts/screenshot.py" https://example.com --mobile --selector ".hero"

# Desktop app capture
python3 "$SCREENSHOT_SKILL/scripts/screenshot.py" --app "Figma"

# Capture existing image region
python3 "$SCREENSHOT_SKILL/scripts/screenshot.py" image.png --crop 100,100,800,600

# Batch capture with multiple viewports
python3 "$SCREENSHOT_SKILL/scripts/screenshot.py" --batch urls.txt --viewports mobile,tablet,desktop

# Capture with upload and markdown
python3 "$SCREENSHOT_SKILL/scripts/screenshot.py" https://example.com --upload --markdown
```

## Command Options

### Viewport Presets (web only)
| Flag | Dimensions | Use Case |
|------|------------|----------|
| `--mobile` | 375x812 | iPhone viewport |
| `--tablet` | 768x1024 | iPad viewport |
| `--desktop` | 1440x900 | Default for web |
| `--size WxH` | Custom | Any dimensions |
| `--full` | Full scroll | Full page capture |

### Element Targeting (web only)
| Flag | Description |
|------|-------------|
| `--selector ".class"` | CSS selector |
| `--text "Button"` | Text content match |
| `--id "element-id"` | Element ID |

### Desktop App Capture
| Flag | Description |
|------|-------------|
| `--app "Name"` | Capture app by name |
| `--window "Title"` | Specific window title |
| `--active` | Capture active window |
| `--region x,y,w,h` | Capture region |

### Image Processing
| Flag | Description |
|------|-------------|
| `--crop x,y,w,h` | Crop region |
| `--resize WxH` | Resize output |
| `--format png/jpg` | Output format |

### Batch Capture
| Flag | Description |
|------|-------------|
| `--batch file.txt` | URLs/apps from file |
| `--viewports m,t,d` | Capture all viewports |

### Output Options
| Flag | Description |
|------|-------------|
| `--output dir/` | Output directory |
| `--name prefix` | Filename prefix |
| `--upload` | Upload to 0x0.st |
| `--upload gist` | Upload to GitHub Gist |
| `--markdown` | Generate markdown table |
| `--copy` | Copy result to clipboard |

## Pre-flight Checks

The tool automatically:
1. Checks for playwright-cli availability
2. Installs if missing: `npm install -g @playwright/mcp@latest`
3. Verifies OS screenshot tools on desktop captures
4. Checks for curl (uploads) and gh CLI (gist)

## Vercel Protection Handling

For `.vercel.app` URLs returning 401/403:
1. Tool detects protected deployment
2. Prompts for bypass token or suggests alternatives
3. Can use `vercel inspect` if Vercel CLI is available

## Output Examples

**Single capture:**
```
Screenshot saved: ~/Downloads/example-desktop-1706900000.png
```

**With upload:**
```
Screenshot saved: ~/Downloads/example-desktop-1706900000.png
Uploaded: https://0x0.st/abc123.png
```

**Markdown output:**
```markdown
| Viewport | Screenshot |
|----------|------------|
| Desktop | ![desktop](https://0x0.st/abc123.png) |
| Mobile | ![mobile](https://0x0.st/def456.png) |
```

## Error Handling

| Error | Resolution |
|-------|------------|
| `playwright-cli not found` | Auto-installs via npm |
| `Element not found` | Verify selector, try broader match |
| `401/403 on URL` | Protected deployment, see above |
| `App not found` | Check app name, ensure visible |
| `Upload failed` | Retry or try different host |

## Integration with PR Workflow

```bash
# Capture staging vs production
python3 "$SCREENSHOT_SKILL/scripts/screenshot.py" https://staging.example.com --upload --markdown > screenshots.md

# Append to PR
gh pr edit --body-file <(cat <(gh pr view --json body -q .body) screenshots.md)
```
