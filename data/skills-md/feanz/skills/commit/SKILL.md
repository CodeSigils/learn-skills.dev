---
name: commit
description: Create a git commit using conventional commits format
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Based on the above changes, create a single git commit.
Create a single commit with an appropriate message, the commit message should follow the [conventional commits](https://www.conventionalcommits.org/) format. Include any tickets or issues resolved in message e.g. resolves #{ticket-number}

You have the capability to call multiple tools in a single response. Stage and create the commit using a single message. Do not use any other tools or do anything else. Do not send any other text or messages besides these tool calls.