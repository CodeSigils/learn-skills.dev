---
name: clean-comments
description: Strip unnecessary and jargony comments from code that was just written. Use when the user asks to clean up comments, remove redundant or obvious comments, delete leftover AI commentary, or says the code is over-commented.
---

# Clean comments

Review all the changes in the feature that was just built, and remove all the unnecessary and jargony comments. If the code explains it, we do not need comments there. This is not a request to summarize or rephrase those comments — delete them outright.

Also, no comments needed to explain why that code fixes one specific nuance — nothing like "increasing the padding from 3 to 6 to make it more spacious".

Keep comments that carry information the code genuinely can't: non-obvious external constraints, links to issues/specs, and intentional deviations that would otherwise look like bugs. Don't change behavior — comments only.

## Scope

By default, work on the changes from this session. If that's unclear, fall back to the uncommitted diff plus the commits on this branch that aren't on the repository's default branch.

If the user passed extra instructions when invoking this skill — narrowing the scope to certain files, loosening or tightening the rules above, or asking for something extra — follow them. Where they conflict with the defaults above, they win.
