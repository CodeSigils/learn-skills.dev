---
name: lessons-learned
description: Run at the end of a dev session to write learnings directly to the zibaldone. Use when wrapping up work or when asked to capture what was learned.
allowed-tools: Read, Edit, Write, Bash
---

# Lessons Learned

Write learnings from this dev session directly into the zibaldone.

## Instructions

1. Review the conversation history for this session
2. Extract decisions, surprises, and learnings — not implementation details that live in the code
3. Get the repo name and branch name
4. Sanitize the branch name by replacing `/` with `-`
5. Write the file to `~/Documents/Notes/zibaldone/{repo}-{branch}.md`
   - Example: `zibaldone/ledge-api-feat-auth-rework.md`
6. If the file already exists, append new entries to it
7. Write raw thoughts, one entry per distinct idea using `- ` list format. No headers, no categories. This is a zibaldone — unstructured capture
8. Keep entries concise but preserve the *reasoning* and *why*, not just what happened
9. A few honest entries beat many filler ones
