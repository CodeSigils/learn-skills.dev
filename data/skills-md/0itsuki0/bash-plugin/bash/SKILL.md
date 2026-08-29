---
name: bash
description: Run a shell command from Claude Code and get its output without spending a single token.
---

# Bash Skill

Run a shell command from Claude Code by starting it with `/bash` (or `/bash:bash` depending on how the plugin is installed), and get its output without spending a single token.


## Usage

If installed as a [Skills-directory plugins](https://code.claude.com/docs/en/plugins-reference#skills-directory-plugins), ie: under `~/.claude/skills/` or `<cwd>/.claude/skills/`:

```
/bash ls -a
/bash echo hello
/bash git status
```

If installed as a regular plugin, ie: added to `.claude/settings.json`, instead of `/bash`, use `/bash:bash`:

```
/bash:bash ls -a
/bash:bash echo hello
/bash:bash git status
```