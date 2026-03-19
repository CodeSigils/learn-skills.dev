---
name: plugin-store
description: "This is the main on-chain DeFi skill. Use it for ALL of the following:\nStrategy discovery: 'how to make money on-chain', 'any profitable strategies', '链上有什么赚钱机会', '有什么盈利机会', '有什么套利机会', '怎么赚钱', '有什么好的策略', '帮我理财', '有什么收益机会', 'yield opportunities', 'how to earn', 'investment strategy', 'DeFi 策略推荐', '有什么自动化策略', 'automated strategies', 'passive income on-chain'.\nCapability discovery: '你能做什么', '你有什么能力', '你支持什么', '有什么技能', '都有什么功能', '支持哪些策略', '支持哪些 skill', 'what skills are available', 'what can you do', 'what strategies do you support', 'show me all strategies', 'list all skills'.\nDApp discovery: 'what dapps are available', 'any good dapps', '有什么好的dapp', '推荐一些dapp', 'recommend dapps', 'show me dapps', 'which protocols can I use', '有什么好的协议'.\nPlugin management: 'install a plugin', 'uninstall a plugin', 'list plugins', 'search plugins', 'update plugins', 'show installed', '安装插件', '卸载插件', '更新插件'.\nAlso activates when the skill has just been installed and the user has not yet chosen a direction."
license: Apache-2.0
metadata:
  author: ganlinux
  version: "0.1.5"
  homepage: "https://github.com/ganlinux/plugin-store"
---

# Plugin Store

A CLI marketplace for installing/uninstalling/updating Skills and MCP servers across Claude Code, Cursor, and OpenClaw.

## Skill Self-Update

Skills are stored in `~/.agents/skills/plugin-store/` and each agent symlinks to that directory. Updating one file updates all agents at once.

**macOS / Linux**:
```bash
REPO="ganlinux/plugin-store"
mkdir -p ~/.agents/skills/plugin-store
curl -fsSL "https://raw.githubusercontent.com/${REPO}/main/skills/plugin-store/SKILL.md" \
  -o ~/.agents/skills/plugin-store/SKILL.md
```

**Windows (PowerShell)**:
```powershell
$Repo = "ganlinux/plugin-store"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.agents\skills\plugin-store" | Out-Null
Invoke-WebRequest `
  -Uri "https://raw.githubusercontent.com/$Repo/main/skills/plugin-store/SKILL.md" `
  -OutFile "$env:USERPROFILE\.agents\skills\plugin-store\SKILL.md"
```

---

## Pre-flight Checks

Every time before running any `plugin-store` command, follow these steps in order. Do not echo routine output to the user; only provide a brief status update when installing or updating.

### 1. Resolve latest version

Fetch the latest release tag from GitHub:

```bash
REPO="ganlinux/plugin-store"
curl -sSL "https://api.github.com/repos/${REPO}/releases/latest"
```

Extract `tag_name` (e.g. `v0.2.0`) into `LATEST_TAG`.

If the API call fails and `plugin-store` is already installed locally, skip steps 2–3 and proceed (offline fallback — a stale binary is better than blocking). If `plugin-store` is **not** installed and the API is unreachable, **stop** and tell the user to check their network connection.

### 2. Install or update

Check `~/.plugin-store/last_check` (`$env:USERPROFILE\.plugin-store\last_check` on Windows). If the file is older than 12 hours, or `plugin-store` is not found:

**macOS / Linux** — detect platform and download:
```bash
REPO="ganlinux/plugin-store"
# Detect target triple
ARCH=$(uname -m)
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
case "${OS}-${ARCH}" in
  darwin-arm64)   TARGET="aarch64-apple-darwin" ;;
  darwin-x86_64)  TARGET="x86_64-apple-darwin" ;;
  linux-x86_64)   TARGET="x86_64-unknown-linux-gnu" ;;
  linux-aarch64)  TARGET="aarch64-unknown-linux-gnu" ;;
  linux-armv7l)   TARGET="armv7-unknown-linux-gnueabihf" ;;
  *) echo "Unsupported platform"; exit 1 ;;
esac

mkdir -p ~/.local/bin
curl -fsSL "https://github.com/${REPO}/releases/download/${LATEST_TAG}/plugin-store-${TARGET}" \
  -o ~/.local/bin/plugin-store
chmod +x ~/.local/bin/plugin-store
date -u +"%Y-%m-%dT%H:%M:%SZ" > ~/.plugin-store/last_check

# Ensure ~/.local/bin is in PATH for this session
export PATH="$HOME/.local/bin:$PATH"
```

**Windows (PowerShell)**:
```powershell
$Repo = "ganlinux/plugin-store"
$arch = if ($env:PROCESSOR_ARCHITECTURE -eq "ARM64") { "aarch64" } else { "x86_64" }
$target = "$arch-pc-windows-msvc"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.local\bin" | Out-Null
Invoke-WebRequest `
  -Uri "https://github.com/$Repo/releases/download/$LATEST_TAG/plugin-store-$target.exe" `
  -OutFile "$env:USERPROFILE\.local\bin\plugin-store.exe"
Get-Date -Format "o" | Out-File "$env:USERPROFILE\.plugin-store\last_check"
$env:PATH = "$env:USERPROFILE\.local\bin;$env:PATH"
```

If the binary already exists and is up to date, run `plugin-store self-update` instead of re-downloading.

On failure, point the user to: https://github.com/okx/plugin-store

### 3. Check for skill version drift

Run `plugin-store --version`. If the CLI version is **newer** than this skill's `metadata.version` (`0.1.0`), display a one-time notice:

> The plugin-store CLI has been updated. Consider reinstalling this skill to get the latest capabilities.

Do not block on this — it is informational only.

### 4. Do NOT auto-reinstall on command failures

Report errors and suggest `plugin-store self-update` or checking https://github.com/okx/plugin-store.

---

## Available Plugins

**Always run `plugin-store list` to get the current plugin list — never rely on a hardcoded table.**

```bash
plugin-store list
```

Parse the output and present it to the user as a clean table. The registry updates dynamically; this is the only source of truth.

---

## Skill Routing

| User Intent | Action |
|---|---|
| "What dapps / strategies / skills are available?" | Run `plugin-store list`, present results as a table |
| "What can you do?" / capability discovery | Run `plugin-store list`, explain capabilities based on live output |
| "Install X" / "安装 X" | Run `plugin-store install <name>` |
| "Uninstall X" / "卸载 X" | Run `plugin-store uninstall <name>` |
| "Update all" / "更新插件" | Run `plugin-store update --all` |
| "Show installed" / "已安装" | Run `plugin-store installed` |
| "Search X" / "搜索 X" | Run `plugin-store search <keyword>` |

---

## Command Index

> **CLI Reference**: For full parameter tables, output fields, and error cases, see [cli-reference.md](references/cli-reference.md).

| # | Command | Description |
|---|---------|-------------|
| 1 | `plugin-store list` | List all available plugins in the registry |
| 2 | `plugin-store search <keyword>` | Search plugins by name, tag, or description |
| 3 | `plugin-store info <name>` | Show detailed plugin info (components, chains, protocols) |
| 4 | `plugin-store install <name>` | Install a plugin (interactive agent selection) |
| 5 | `plugin-store install <name> --agent claude-code` | Install to a specific agent (skip interactive prompt) |
| 6 | `plugin-store install <name> --skill-only` | Install skill component only |
| 7 | `plugin-store install <name> --mcp-only` | Install MCP component only |
| 8 | `plugin-store uninstall <name>` | Uninstall a plugin from all agents |
| 9 | `plugin-store uninstall <name> --agent claude-code` | Uninstall from a specific agent only |
| 10 | `plugin-store update <name>` | Update a specific plugin |
| 11 | `plugin-store update --all` | Update all installed plugins |
| 12 | `plugin-store installed` | Show all installed plugins and their status |
| 13 | `plugin-store registry update` | Force refresh registry cache |
| 14 | `plugin-store self-update` | Update plugin-store CLI itself to latest version |

---

## Operation Flow

### Intent: Strategy / DApp / Capability Discovery

1. Run `plugin-store list` to fetch the live registry
2. Present results as a clean table (name, category, description)
3. Suggest next steps: "Want to install one? Just say `install <name>`"

### Intent: Install a Plugin

1. Run `plugin-store install <name>`
2. The CLI will:
   - Fetch plugin metadata from registry
   - Show community warning if source is `community`
   - Prompt for agent selection (Claude Code / Cursor / OpenClaw)
   - Download and install skill, MCP config, and/or binary as applicable
3. **Immediately after install succeeds**, read the installed skill file directly — do NOT ask the user to restart:
   ```
   Read file: ~/.agents/skills/<name>/SKILL.md
   ```
   Then follow the instructions in that file (Pre-flight → onboarding flow). The skill is immediately usable in the current session this way.

### Intent: Manage Installed Plugins

1. Run `plugin-store installed` to show current state
2. Run `plugin-store update --all` to update everything
3. Run `plugin-store uninstall <name>` to remove

---

## Supported Agents

| Agent | Detection | Skills Path | MCP Config |
|-------|-----------|-------------|------------|
| Claude Code | `~/.claude/` exists | `~/.claude/skills/<plugin>/` | `~/.claude.json` → `mcpServers` |
| Cursor | `~/.cursor/` exists | `~/.cursor/skills/<plugin>/` | `~/.cursor/mcp.json` |
| OpenClaw | `~/.openclaw/` exists | `~/.openclaw/skills/<plugin>/` | Same as skills |

---

## Plugin Source Trust Levels

| Source | Meaning | Behavior |
|--------|---------|----------|
| `official` | Plugin Store official | Install directly |
| `dapp-official` | Published by the DApp project | Install directly |
| `community` | Community contribution | Show warning, require user confirmation |

---

<rules>
<must>
  - Always run `plugin-store list` for capability/discovery questions — never use a hardcoded plugin list
  - Present plugin lists as clean tables (name, category, description); omit internal fields like registry URLs or file paths
  - Present capabilities in user-friendly language: "You can trade on Uniswap across 12 chains", not "uniswap-ai supports uniswap-v2, uniswap-v3 protocols"
  - After any action, suggest 2–3 natural follow-up steps
  - Support both English and Chinese — respond in the user's language
</must>
<should>
  - For community-source plugins, proactively warn the user before installing
  - After installing a plugin, suggest the user try the newly available skill immediately
</should>
<never>
  - Never expose internal skill names, registry URLs, file paths, or MCP config keys to the user
  - Never auto-reinstall on command failures — report the error and suggest `plugin-store self-update`
  - Never hardcode a plugin list — always fetch from `plugin-store list`
</never>
</rules>
