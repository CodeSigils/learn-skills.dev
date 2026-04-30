---
name: code-quality
description: Code quality principles and comment conventions. Use when writing, reviewing, or designing code in any language.
user-invocable: false
---

# Code Quality & Comments

## Quality Principles

Priority order: Correctness > Readability > Simplicity > Efficiency.

### Avoid

- **Poor naming** — Vague names (`data`, `info`, `temp`, `result`), excessive abbreviations (`usr`, `mgr`), verbose names that add noise, or names that don't match actual behavior. Names should convey purpose without reading the implementation
- **Unnecessary defensive code** — Paranoid null checks inside system boundaries. Only validate at system boundaries (user input, external APIs)
- **Over-abstraction** — Wrappers, helpers, factories for one-time-use code. Three similar lines > premature abstraction
- **Template patterns** — Design patterns (Factory, Strategy, etc.) where simple direct code suffices
- **Inefficient algorithms** — O(n²) when O(n) is achievable, unnecessary iterations, missing hash-based lookups
- **Poor error handling** — Silently swallowed errors, overly broad catch blocks, missing error context
- **Floating-point money** — Never use native floating-point for monetary calculations (IEEE 754 precision issues). Always use an arbitrary-precision decimal library. See language-specific skills for package choices
- **Raw date/time manipulation** — Never manipulate native Date objects or format date/time strings manually. Always use a dedicated date/time library. See runtime/framework skills for package choices
- **Magic values** — Unexplained numbers and strings; use named constants
- **Dead code** — Unused imports, variables, functions, unreachable code. Don't comment out and keep — delete it (version control has history)
- **Deep nesting** — More than 3 levels of if/for/try nesting. Use early returns, guard clauses, or extract functions to flatten
- **Long functions** — A function doing too many things. If you need comments to separate sections, it should be split
- **Hidden side effects** — Functions that modify external state, send requests, or write files without the name indicating it. Side effects should be explicit, predictable, and concentrated at clear boundary layers

### Acceptable when

- Meaningful error handling with useful context
- Necessary validation at system boundaries
- Useful abstractions reused 3+ times
- Performance optimizations backed by actual needs
- Idiomatic patterns for the language/framework

## Comment Conventions

Comments explain WHY, not WHAT. If the code needs a comment to explain what it does, the code should be rewritten. Use the `comments` skill for detailed guidance on adding, removing, or updating comments and file headers.
