---
name: recap
description: |
  Reviews recent prompt history to restore development context.
  Reads prompt record files from the prompts/ directory (created by commit-with-prompts),
  synthesizes key context (user focus areas, technical choices, design decisions),
  and asks the user whether to continue with this context or start fresh.
  Invoke with /recap.
---

# Recap

Prompt records capture the intent, reasoning, and decisions behind every code change. This skill reads those records, distills the recent development context, and presents it so both you and the user can pick up where things left off — no cold starts.

This skill is the **read** half of a closed loop: `commit-with-prompts` writes prompt records → `recap` reads them.

## Workflow

Execute these steps when the user invokes `/recap`.

### Step 1: Read Recent Prompt Records

1. List all `.md` files in the `prompts/` directory at the project root.
2. Sort filenames in **descending** order (filenames start with `YYYY-MM-DD`, so lexicographic sort naturally produces reverse-chronological order).
3. Read the **most recent 3** files in full.
4. If the `prompts/` directory does not exist or contains no `.md` files, output the following and **stop** — do not continue to subsequent steps:

```
No prompt history found.
```

### Step 2: Parse and Synthesize

From each prompt record file, extract:

- **Metadata** — date, branch, commit message (from the `- Date:`, `- Branch:`, `- Commit:` lines)
- **User prompts** — the original user prompt text in each numbered section (`### N`)
- **Insights** — content from `> **Insight**` blocks (design decisions and reasoning)
- **Affected files** — paths from `**Files:**` lines

Synthesize the extracted information into three dimensions:

1. **Recent Focus** — What features, bugs, or areas has the user been working on? Identify recurring themes and the current development direction.
2. **Technical Choices** — What technical or architectural decisions were made? What was chosen and why?
3. **Design Rationale** — What is the background and rationale behind key design choices? Pull from Insight blocks and commit messages.

Guidelines:
- Each dimension should have **2–5** bullet points. Be concise and scannable.
- If a dimension has no relevant content (e.g., pure bugfixes with no design decisions), **omit that dimension entirely** rather than forcing empty content.
- Preserve specificity — mention actual file names, function names, and technical terms rather than vague summaries.

### Step 3: Display Recap

Output the structured summary in this exact format:

```
Prompt Recap — Last N commits
═══════════════════════════════════════

Recent Focus
  - [topic]: [brief description]
  - ...

Technical Choices
  - [decision]: [what was chosen and why]
  - ...

Design Rationale
  - [design point]: [background and reasoning]
  - ...

Files touched: file1, file2, ...
Time range: YYYY-MM-DD ~ YYYY-MM-DD
─────────────────────────────────────
```

Where:
- `N` is the number of prompt record files that were read
- **Files touched** is a deduplicated, comma-separated list of all affected files across all records
- **Time range** spans from the oldest to the newest record's date
- Omit any dimension heading that has no bullet points
- Use the user's working language for the recap content (bullet point text), but keep the structural labels in English

### Step 4: Ask User

After displaying the recap, use the **AskUserQuestion** tool to ask the user how to proceed:

- **Option 1: "Continue" (Recommended)** — Accept the displayed context and continue working with it. Confirm that context is loaded and proceed to respond to the user's first message normally.
- **Option 2: "Load more"** — Load additional history. Go back to Step 1 and read **8 files total** (the original 3 plus 5 more). Re-synthesize and re-display the expanded recap, then ask again (but with only "Continue" and "Fresh start" as options — no further expansion).
- **Option 3: "Fresh start"** — Discard all displayed context. Output a brief confirmation and do **not** reference any of the previously shown history when responding to the user.

## Edge Cases

- **Fewer files than requested**: if there are fewer than 3 (or 8) files, read all available files. Adjust the recap count (`N`) accordingly.
- **Malformed files**: if a prompt record file doesn't follow the expected format, extract what you can and skip unparseable sections. Do not error out.
- **Very large prompt files**: read the full content — do not truncate. The most valuable context is often in longer records.

