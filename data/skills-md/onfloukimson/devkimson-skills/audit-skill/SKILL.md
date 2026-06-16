---
name: audit-skill
description: Audit personal skills from the local devkimson-skills repository or its GitHub remote against globally installed agent skills, and install any missing skills with npx skills. Use when checking, repairing, or refreshing the user's global Codex, Gemini CLI, and Cursor skill availability.
---

# Purpose

Keep every skill in `devkimson-skills` available globally through the official `skills` CLI instead of KPA-local runtime mirrors.

# Source

Resolve the source in this order:

1. Local repository when it exists:
   - `D:/kimson/01_development/00_personal/devkimson-skills`
2. GitHub fallback:
   - `onfloukimson/devkimson-skills`

Repository layout:

- `skills/<hyphen-case-name>/SKILL.md`
- Target scope: global
- Target agents: `codex`, `gemini-cli`, and `cursor`

# Workflow

1. Confirm `npx` is available.
2. Resolve `<skill-source>` using the source priority above.
3. List source skills without installing:

```powershell
npx skills add <skill-source> --list
```

4. List globally installed skills for the target agents:

```powershell
npx skills ls -g -a codex -a gemini-cli -a cursor
```

5. Compare skill names exactly. Treat lowercase hyphen-case as canonical.
6. For each source skill missing from one or more target agents, install that skill globally:

```powershell
npx skills add <skill-source> -g -a codex -a gemini-cli -a cursor --skill <skill-name> -y
```

7. Do not reinstall skills already present unless the user asks for an update.
8. When installed versions appear stale, use the official update command only after reporting the affected skills:

```powershell
npx skills update -g <skill-name> -y
```

9. Run the global list command again and verify every source skill is present for all target agents.
10. Report installed, already present, failed, and still missing skills separately.

# Naming Rule

- Skill names and directories must use lowercase letters, digits, and hyphens only.
- Reject underscores, spaces, and mixed-case directory names as repository defects.
- Require the `name` field in `SKILL.md` to equal the containing directory name.

# Safety Rules

- Do not modify KPA-local `.codex/skills`, `.gemini/skills`, or `.cursor/skills` mirrors.
- Do not delete global skills automatically.
- Do not run `--all` when only some skills are missing.
- Do not update already installed skills unless the user requested an update or approved a reported version mismatch.
- If source access, authentication, `npx`, or network access fails, report the exact blocker and leave existing global installations unchanged.

# Verification

- Source skill names were obtained from `npx skills add <skill-source> --list`.
- Global state was obtained from `npx skills ls -g`.
- Every source skill is present for `codex`, `gemini-cli`, and `cursor`, or the remaining exception is reported.
- Every source directory and frontmatter `name` uses matching hyphen-case.
