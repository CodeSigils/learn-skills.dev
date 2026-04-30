---
name: comments
description: Guidelines for deciding whether to write, update, or remove code comments. Use when adding comments, reviewing comment quality, documenting non-obvious code, or deciding if a comment is necessary.
user-invocable: false
---

# Comment Guidelines

Use this skill when deciding whether code should have a comment. Comments should explain useful context that the code cannot express clearly on its own. Prefer clearer code over comments that restate what the code does.

## Core Principle

Write comments for future readers who need intent, constraints, or surprising context. Do not write comments to narrate syntax, repeat names, or compensate for unclear code that can be made clearer directly.

Before adding a comment, ask:

1. Can a better name, smaller function, or simpler structure make this obvious?
2. Does the comment explain why, not merely what?
3. Will the comment still be useful when the code changes later?

If the answer is no, improve the code instead of adding a comment.

## Remove Comments When They Are

- Redundant: the code is already self-explanatory.
- Obvious: the comment states what the code literally does.
- Outdated: the comment no longer matches behavior.
- Noise: commented-out code, placeholder notes, or TODOs without actionable context.

Examples to remove:

```javascript
const count = 0; // Initialize count to 0

// Loop through users
for (const user of users) { ... }

// TODO: fix this
// const oldCode = something;
```

## Add Comments When They Explain

- Complex logic: non-obvious algorithms, business rules, or edge cases.
- Unusual code: workarounds, hacks, or unconventional patterns.
- Context: why something is done a certain way.
- External constraints: limitations or requirements from outside systems.

Examples worth keeping or adding:

```javascript
// Using setTimeout to avoid a race with DOM rendering.
setTimeout(() => updateUI(), 0);

// Discount only applies to orders over 100 by marketing requirement JIRA-1234.
if (order.total > 100) { ... }

// Binary search is valid because fetchData sorts this list upstream.
const index = binarySearch(sortedItems, target);
```

## File Headers

For new or significantly changed files, follow the project's existing file header convention. If the project has no convention, use the language's normal documentation style:

- JS/TS: JSDoc `@file` header.
- Rust: module-level `//!` doc comment.
- Python: module docstring.

Only add a header when it meaningfully helps future readers understand the file's purpose.

## Daily Coding Guidance

- Match the project's existing comment style, language, and density.
- Keep comments close to the code they explain.
- Keep comments concise; a precise sentence is usually better than a paragraph.
- Update nearby comments when changing behavior.
- Delete stale comments instead of letting them drift.
- Do not add file headers, section dividers, or explanatory blocks unless they create real reader value.
- Do not paste issue history or implementation diary details into code comments; summarize the durable constraint.