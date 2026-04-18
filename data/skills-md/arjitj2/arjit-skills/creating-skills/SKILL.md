---
name: creating-skills
description: Use when creating a new skill, adding a skill to the user's setup, or the user says "make this a skill". All personal skills live in the arjit-skills monorepo and are symlinked into place.
---

# Creating Skills

## Overview

All personal skills live in `~/repos/arjit-skills/skills/<skill-name>/`. Skills are symlinked into `~/.agents/skills/` and `~/.claude/skills/` so all agents can discover them.

## Process

1. **Create the skill directory and files:**
   ```
   ~/repos/arjit-skills/skills/<skill-name>/
     SKILL.md              # Required
     supporting-file.*     # Only if needed
   ```

2. **Symlink into both agent directories:**
   ```bash
   ln -sf ~/repos/arjit-skills/skills/<skill-name> ~/.agents/skills/<skill-name>
   ln -sf ~/repos/arjit-skills/skills/<skill-name> ~/.claude/skills/<skill-name>
   ```

3. **Update the repo README** (`~/repos/arjit-skills/README.md`):
   - Add the new skill to the Skills section in alphabetical order
   - Include a one-line description

4. **Commit and push:**
   ```bash
   cd ~/repos/arjit-skills
   git add skills/<skill-name>
   git commit -m "Add <skill-name> skill"
   git push
   ```

## Rules

- **Never** create skills directly in `~/.claude/skills/` or `~/.agents/skills/` — always in the repo, then symlink.
- **Never** create a standalone repo per skill — everything goes in `arjit-skills`.
- Skill names use lowercase letters, numbers, and hyphens only.
- If adapting someone else's skill, credit the original in the repo README and in a comment in SKILL.md.
