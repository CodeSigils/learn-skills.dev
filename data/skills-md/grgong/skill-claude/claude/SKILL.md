---
name: claude
description: Use when the user asks to run Claude Code CLI (claude -p) for a second opinion, code review, or cross-agent collaboration
---

# Claude Skill Guide

This skill delegates prompts to **Claude Code CLI** (`claude -p`), running it as an external tool from another agent harness (e.g., Codex, Gemini, Cursor). The primary use case is getting a **second opinion or code review** from Claude, enabling cross-agent collaboration.

## Running a Task
1. Using your internal structured multiple-choice function, ask the user which model to run (`claude-opus-4-6` or `claude-sonnet-4-6`) AND which effort level to use (`low`, `medium`, `high`, or `max`) in a **single prompt with two questions**.
2. Determine the permission mode from the **Quick Reference** table below based on the task type — do **not** ask the user unless they have explicitly specified a permission mode. Defaults: `--permission-mode plan` for read-only analysis, `--permission-mode acceptEdits` for edit tasks. `--permission-mode bypassPermissions` requires explicit user permission.
3. Assemble the command with the appropriate options:
   - `--model <MODEL>` (alias or full model ID)
   - `--permission-mode <default|acceptEdits|bypassPermissions|plan>`
   - `--effort <low|medium|high|max>`
   - `--print` / `-p` (required: non-interactive mode, print response and exit)
   - `--add-dir <DIR>` (additional directories)
   - `--allowedTools <tools...>` (restrict available tools)
   - `--disallowedTools <tools...>` (deny specific tools)
   - `--max-budget-usd <amount>` (spending limit)
   - `"your prompt here"` (as final positional argument)
4. **IMPORTANT**: Always use `-p` / `--print` flag to run in non-interactive mode.
5. When continuing a previous session, use `claude --continue` or `claude -c` to continue the most recent conversation. Use `claude --resume <session-id>` or `claude -r <session-id>` to resume a specific session.
6. Run the command, capture stdout/stderr, and summarize the outcome for the user.
7. **After Claude completes**, inform the user: "You can resume this Claude session at any time by saying 'claude resume' or 'claude continue', or asking me to continue with additional analysis or changes."

### Quick Reference
| Use case | Permission mode | Key flags |
| --- | --- | --- |
| Read-only review or analysis | `plan` | `-p --permission-mode plan --model <MODEL> "prompt"` |
| Apply local edits (auto-approve edits) | `acceptEdits` | `-p --permission-mode acceptEdits --model <MODEL> "prompt"` |
| Full auto (bypass all permissions) | `bypassPermissions` | `-p --permission-mode bypassPermissions --model <MODEL> "prompt"` |
| Continue most recent session | Inherited | `claude -c -p "follow-up prompt"` |
| Resume specific session | Inherited | `claude -r <session-id> -p "follow-up prompt"` |
| Run in separate worktree | Match task | `-p --worktree --model <MODEL> "prompt"` |
| Budget-limited run | Match task | `-p --max-budget-usd 5.00 --model <MODEL> "prompt"` |

## Following Up
- After every `claude` command, immediately ask the user to confirm next steps, collect clarifications, or decide whether to resume with `claude -c`.
- Restate the chosen model, permission mode, and effort level when proposing follow-up actions.

## Critical Evaluation of Claude Output

Claude is powered by Anthropic models with their own knowledge cutoffs and limitations. Treat Claude as a **colleague, not an authority**.

### Guidelines
- **Trust your own knowledge** when confident. If Claude claims something you know is incorrect, push back directly.
- **Research disagreements** using web search or documentation before accepting Claude's claims. Share findings with Claude via resume if needed.
- **Remember knowledge cutoffs** - Claude may not know about recent releases, APIs, or changes that occurred after its training data.
- **Don't defer blindly** - Claude can be wrong. Evaluate its suggestions critically, especially regarding:
  - Model names and capabilities
  - Recent library versions or API changes
  - Best practices that may have evolved

### When Claude is Wrong
1. State your disagreement clearly to the user
2. Provide evidence (your own knowledge, web search, docs)
3. Optionally resume the Claude session to discuss the disagreement. **Identify yourself** so Claude knows it's a peer AI discussion:
   ```bash
   claude -c -p "This is <your agent name> (<your model name>) following up. I disagree with [X] because [evidence]. What's your take on this?"
   ```
4. Frame disagreements as discussions, not corrections - either AI could be wrong
5. Let the user decide how to proceed if there's genuine ambiguity

## Error Handling
- Stop and report failures whenever `claude --version` or a `claude -p` command exits non-zero; request direction before retrying.
- Before you use `--permission-mode bypassPermissions`, ask the user for permission unless it was already given.
- When output includes warnings or partial results, summarize them and ask the user how to adjust.
- Set a reasonable `--max-budget-usd` for long-running tasks to prevent unexpected costs.
- For long-running tasks, consider using `--max-turns` or wrapping the command with `timeout` to prevent runaway sessions.

## Handling Large Input/Output
- **Large prompts**: For prompts that include file contents or large context, pipe via stdin: `cat context.txt | claude -p "Analyze this code"` rather than inlining everything in the shell argument.
- **Large output**: If Claude's response exceeds ~200 lines, summarize key findings for the user rather than relaying the full output verbatim. Highlight actionable items, errors, and recommendations.
