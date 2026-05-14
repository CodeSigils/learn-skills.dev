---
name: conventional-commits
description: This skill should be used when the user asks to "create commit", "commit message", "git commit", "generate commit message", "write a commit", "commit local repository changes", or describes changes to be committed. Generates high-quality Conventional Commits formatted messages based on staged changes without executing the commit command.
---

# Conventional Commits Guidelines

Follow the Conventional Commits specification to generate professional commit messages based on staged changes.

## Message Composition Rules

1.  **Enforce Format**:
    *   Construct the message using the format: `<type>(<scope>): <subject>`
    *   Include a blank line followed by a detailed `<body>`. Ensure the body reflects technical changes.
    *   Wrap the final output in a **Markdown code block**.

2.  **Select Appropriate Type**:
    *   Follow the standard types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`.
    *   Refer to `references/type-definitions.md` for detailed selection criteria.

3.  **Extract Scope (Path-Based Only)**:
    *   Derive the scope strictly from the file path of the staged changes.
    *   Priority 1 (Module): Use the top-level or second-level directory name (e.g., `src/components/`, `api/`) if all changes fall within it.
    *   Priority 2 (Platform): Use `ios` or `android` if changes are specifically inside those folders.
    *   Priority 3 (Global): Use `*` only if changes affect more than three top-level modules or involve root-level configuration.
    *   Refer to `references/scope-guidelines.md` for detailed extraction rules.

4.  **Compose Subject Line**:
    *   Integrate User Input: Use text provided in quotes verbatim as the `<subject>`. Ignore other instructional words in the prompt.
    *   Generate Concisely: Generate a concise subject in **Traditional Chinese (Taiwan)** based on the staged diff if no text is provided.
    *   Limit Length: Keep the subject line under 50 characters.

5.  **Draft Body Content**:
    *   Analyze Diff: Generate the `<body>` exclusively from `git diff --cached` analysis.
    *   Prohibit Hallucination: Exclude user instructions, tool metadata, or conversation context.
    *   Language Policy: Use **Traditional Chinese (Taiwan)** for descriptions, keeping technical terms in **English**.
    *   Requirement: Include a `<body>` for every commit. Extract at least one technical bullet point from the git diff even for small changes.
    *   Focus: Describe "what" changed in the code (e.g., modified a function, changed a style property).

6.  **Apply Language Constraints**:
    *   `type`: English.
    *   `scope`: English.
    *   `subject`: Verbatim (if provided) or Traditional Chinese (Taiwan).
    *   `body`: Traditional Chinese (Taiwan) with English technical terms.

7.  **Handle Staged Changes**:
    *   Analyze ONLY staged changes.
    *   Stop and inform the user if no changes are staged: "目前沒有已暫存（staged）的變更，請先執行 git add。"

8.  **Control Output Behavior**:
    *   Follow the strict prohibition on calling tools or functions to execute git commits. Output the generated text only.
    *   Limit tool usage to `git diff --cached` and `git ls-files`.

9.  **Implement Interactive Refinement**:
    *   Append Refinement Prompt: Append the refinement prompt ONLY during the initial generation (Phase 1):
        > 「💡 **提示**：若本次改動較複雜，建議提供以下資訊，我將為你潤飾更專業的描述：
        > **背景/動機**：(說明為什麼改)
        > **關鍵改動**：(說明做了什麼)
        > **預期影響**：(說明改完後的好處)」
    *   Regenerate with Context: Replace the automatically generated body with a polished version if the user provides additional context.
    *   Maintain Silence: Avoid repeating the refinement prompt in phase 2 (after context is provided).

## Operational Workflow

### Phase 1: Initial Generation
1.  Execute `git diff --cached` to gather context.
2.  Stop if no changes are staged.
3.  Analyze the diff to identify the logical `type`.
4.  Determine the **scope** based on the representative directory name.
5.  Compose the subject line following priority rules.
6.  Draft the message text (Subject + Mandatory Body).
7.  Output the text in a Markdown code block.
8.  Stop all actions after output. Avoid calling further tools.
9.  Append the Refinement Prompt.

### Phase 2: Contextual Refinement
1.  Discard the old body if user provides "背景/動機", "關鍵改動", or "預期影響".
2.  Use the user-provided context as the primary source, supplemented by technical facts from the diff.
3.  Output the polished commit message in a new code block.
4.  Stop and do not provide the refinement prompt again.

## Additional Resources

### Reference Files
- **`references/type-definitions.md`** - Detailed commit type definitions.
- **`references/scope-guidelines.md`** - Comprehensive scope extraction rules.

### Example Files
- **`examples/feature-example.md`** - Example of a new feature commit.
- **`examples/fix-example.md`** - Example of a bug fix commit.
