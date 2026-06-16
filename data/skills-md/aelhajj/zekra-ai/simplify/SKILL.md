---
name: simplify
description: Review changed code for reuse, quality, and efficiency, then fix any issues found
disable-model-invocation: false
allowed-tools: Read Grep Glob Edit Bash(git diff*)
---

Review recently changed code for opportunities to simplify. If $ARGUMENTS specifies files, review those. Otherwise review uncommitted changes.

## What to look for

1. **Duplication** — same logic in multiple places? Extract only if it appears 3+ times (rule of three)
2. **Over-engineering** — abstractions that serve only one call site? Inline them
3. **Dead code** — unused imports, unreachable branches, commented-out code? Remove
4. **Verbose patterns** — can be replaced with Pythonic idioms (comprehensions, unpacking, walrus, truthiness)?
5. **Type issues** — missing annotations, `Any` cop-outs, wrong return types?
6. **Naming** — unclear or abbreviated names that violate PEP 20?

## Rules

- Don't add features or change behavior — only simplify existing code
- Don't add comments, docstrings, or type annotations to code that wasn't changed
- Don't create helpers for one-time operations
- If something is fine as-is, say so — don't force changes

## Action

Find issues, then fix them directly. Show what you changed and why.
