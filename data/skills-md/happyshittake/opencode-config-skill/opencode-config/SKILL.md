---
name: opencode-config
description: Use when modifying opencode.jsonc, adding providers or MCP servers, configuring agents, setting permissions, migrating legacy config keys, customizing TUI themes or keybinds, creating AGENTS.md instruction files, or validating opencode configuration. Also use when setting up opencode for the first time or onboarding team members.
---

# opencode-config

## Overview

Guides opencode agents through correctly reading, updating, migrating, and validating opencode configuration files. Covers the main config (`opencode.jsonc`), TUI config (`tui.json`), and instruction files (`AGENTS.md`, `CLAUDE.md`).

## Config File Locations

### Which file to edit

| Scenario | File to edit | Path |
|----------|-------------|------|
| Per-project settings | `.opencode/opencode.json` or `.opencode/opencode.jsonc` | Project root |
| User-wide defaults | `opencode.json` or `opencode.jsonc` | `~/.config/opencode/` |
| TUI appearance/keybinds | `tui.json` | Same location as config |
| Agent instructions | `AGENTS.md` | Project root or `~/.config/opencode/` |

### Merge hierarchy (later overrides earlier)

1. Remote `.well-known/opencode`
2. Global `~/.config/opencode/opencode.json`
3. Custom (`OPENCODE_CONFIG` env var)
4. Project `.opencode/opencode.json`
5. `OPENCODE_CONFIG_CONTENT` env var
6. Managed config (system-level)

## Format Rules

- **Format:** JSONC (JSON with Comments) — comments (`//`) and trailing commas allowed
- **Always include:** `"$schema": "https://opencode.ai/config.json"` as first property
- **TUI schema:** `"$schema": "https://opencode.ai/tui.json"`
- **Env var substitution:** Use `"${env.VAR_NAME}"` to reference environment variables, `"${home}"` for home directory
- **Never strip comments** when editing existing JSONC files — preserve them

## Common Operations

### Add a provider

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "my-provider": {
      "api": "openai",
      "name": "My Provider",
      "options": {
        "baseURL": "https://api.example.com/v1",
        "apiKey": "${env.MY_API_KEY}"
      }
    }
  }
}
```

### Add an MCP server

```jsonc
{
  "mcp": {
    "my-server": {
      "type": "local",
      "command": ["npx", "-y", "my-mcp-server"],
      "enabled": true
    }
  }
}
```

For remote MCP:

```jsonc
{
  "mcp": {
    "remote-server": {
      "type": "remote",
      "url": "https://mcp.example.com/sse",
      "headers": {
        "Authorization": "Bearer ${env.MCP_TOKEN}"
      }
    }
  }
}
```

### Configure an agent

```jsonc
{
  "agent": {
    "build": {
      "model": "anthropic/claude-sonnet-4-20250514",
      "steps": 50
    },
    "custom-agent": {
      "model": "openai/gpt-4o",
      "prompt": "You are a specialized assistant for...",
      "mode": "subagent",
      "description": "Does X, Y, Z"
    }
  }
}
```

### Set permissions

```jsonc
{
  "permission": {
    "bash": {
      "*.test.ts": "allow",
      "*": "ask"
    },
    "edit": "allow",
    "read": "allow",
    "webfetch": "deny"
  }
}
```

### Add plugins

```jsonc
{
  "plugin": [
    "opencode-skills-collection",
    "my-plugin@1.0.0"
  ]
}
```

### Add instruction files

```jsonc
{
  "instructions": [
    "CONTRIBUTING.md",
    "docs/style-guide.md",
    ".cursor/rules/*.md"
  ]
}
```

## TUI Configuration

TUI config lives in `tui.json` (separate from main config).

### Change theme

```jsonc
{
  "$schema": "https://opencode.ai/tui.json",
  "theme": "tokyonight"
}
```

Built-in themes: `opencode`, `tokyonight`, `everforest`, `ayu`, `catppuccin`, `catppuccin-macchiato`, `gruvbox`, `kanagawa`, `nord`, `matrix`, `one-dark`, `system`

### Customize keybinds

```jsonc
{
  "$schema": "https://opencode.ai/tui.json",
  "keymap": {
    "leader": "ctrl+x",
    "leader_timeout": 2000,
    "sections": {
      "global": {
        "command.palette.show": "ctrl+p",
        "session.new": "<leader>n",
        "session.list": "<leader>l"
      },
      "session": {
        "session.compact": "<leader>c"
      }
    }
  }
}
```

Keymap sections: `global`, `session`, `prompt`, `input`, `autocomplete`, `dialog_select`, `dialog_actions`, `model`, `permission`, `question`, `plugins`, `home_tips`

### Custom themes

Place JSON files in `~/.config/opencode/themes/` or `.opencode/themes/`. Schema: `https://opencode.ai/theme.json`.

## Instruction Files

### File discovery (first match wins within each category)

**Project-level** (walk up to git worktree root):
- `AGENTS.md` > `CLAUDE.md` > `CONTEXT.md`
- `.opencode/AGENTS.md` loaded **in addition** (not instead)

**Global:**
- `~/.config/opencode/AGENTS.md` > `~/.claude/CLAUDE.md`

**Both project and global are combined** (not overridden). Project rules appear first in prompt.

### Creating instruction files

```markdown
# Project Instructions

## Code Style
- Use TypeScript strict mode
- Prefer functional components with hooks

## Testing
- All new features require tests
- Use vitest for unit tests
```

### Context-aware instructions

Files matching `(.+[-_.])?AGENTS.md` are auto-injected when editing nearby files:
- `python.AGENTS.md` — injected when editing Python files
- `backend_AGENTS.md` — injected when editing in backend directories

## Migration Patterns

When updating existing configs, check for and migrate these legacy keys:

| Legacy Key | Modern Key | Notes |
|-----------|-----------|-------|
| `"mode"` | `"agent"` | Rename the key |
| `"tools"` | `"permission"` | Convert booleans to permission rules |
| `"autoshare"` | `"share"` | `true` → `"auto"`, `false` → `"manual"` |
| `"maxSteps"` | `"steps"` | In agent config |
| `"layout"` | _(remove)_ | Always uses stretch layout |
| `theme`, `keybinds`, `tui` in main config | Separate `tui.json` | Extract to dedicated file |
| TOML `~/.config/opencode/config` | `~/.config/opencode/config.json` | Convert format |

## Validation Checklist

After editing config, verify:

1. JSONC syntax is valid (no missing commas, brackets balanced)
2. `$schema` property is present
3. No unknown top-level keys (strict validation — `additionalProperties: false`)
4. Env var references use correct syntax: `"${env.VAR}"`
5. Model IDs use format: `provider/model-name`
6. MCP `command` is an array of strings, not a single string
7. Permission values are `"ask"`, `"allow"`, or `"deny"` only
8. Agent `mode` is `"primary"`, `"subagent"`, or `"all"`

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Editing global config for a project-specific change | Edit `.opencode/opencode.json` instead |
| Stripping comments when editing JSONC | Use JSONC-aware editing, preserve `//` comments |
| Using `"command": "npx server"` for MCP | Must be array: `"command": ["npx", "server"]` |
| Forgetting `$schema` | Always add as first property |
| Using `"model": "claude-sonnet"` | Must include provider: `"model": "anthropic/claude-sonnet-4-20250514"` |
| Setting permissions as `"bash": true` | Use `"bash": "allow"` or glob patterns |
| Putting TUI keys in main config | Use separate `tui.json` file |
| Using `~` in paths inside config | Use `"${home}"` for home directory substitution |

## Quick Reference

For complete field listings, see [config-reference.md](config-reference.md) and [tui-reference.md](tui-reference.md).

### Most common operations

| Operation | File | Key |
|-----------|------|-----|
| Set default model | opencode.json | `"model": "provider/model"` |
| Add API provider | opencode.json | `"provider": { "name": {...} }` |
| Add MCP server | opencode.json | `"mcp": { "name": {...} }` |
| Configure agent | opencode.json | `"agent": { "name": {...} }` |
| Set permissions | opencode.json | `"permission": { ... }` |
| Change theme | tui.json | `"theme": "name"` |
| Change keybinds | tui.json | `"keymap": { ... }` |
| Add project rules | AGENTS.md | Markdown at project root |
| Add global rules | AGENTS.md | `~/.config/opencode/AGENTS.md` |
| Add extra instructions | opencode.json | `"instructions": ["file.md"]` |
