---
name: skill-creator
description: "Skill development assistant that creates new Claude Code skills following Anthropic's official conventions. Guides through requirements gathering, resource planning, SKILL.md authoring, and validation. Use this skill when the user says things like: 'create a skill', 'build a new skill', 'make a skill for...', 'new skill for...', 'I want a skill that...', 'add a skill to the repo', 'skill for...', 'write a SKILL.md', or wants to create, scaffold, or develop a Claude Code skill."
---

# Skill Creator

A guided skill that creates new Claude Code skills following Anthropic's official skill development conventions and the patterns established in this repository. Ensures every skill produced is lean, well-structured, and discoverable.

This is NOT a template filler. It's a structured authoring process: understand the domain, plan the resources, write a focused SKILL.md, and validate everything before committing.

## Workflow Overview

```
Input (idea, domain, use case)
  -> Requirements (guided questions)
    -> Research (scan existing skills + domain context)
      -> Resource Planning (references, examples, assets)
        -> SKILL.md Authoring (frontmatter + imperative body)
          -> Supporting Files (references/, examples/, assets/)
            -> Validation (structure, style, completeness)
              -> README Update (add to project listing)
```

---

## Step 0: Gather Requirements

Ask the user these questions in a single message. Do not proceed until answers are clear.

| Question | Purpose |
|----------|---------|
| What does the skill do? | Core purpose and domain |
| What are 3-5 things a user would say to trigger it? | Trigger phrases for the description |
| Does it need external data? (APIs, MCP tools, web scraping) | Determine MCP dependencies |
| Does it produce output files? (HTML, PDF, images) | Determine output strategy |
| Does it need reference docs, templates, or example files? | Plan supporting resources |
| Should it integrate with Notion, Cloudflare Workers, or other services? | Determine integrations |

**Implicit detection:** If the user's opening message already describes the skill in detail, extract the answers directly and confirm with a summary table instead of asking.

---

## Step 1: Research Phase

### 1A: Scan Existing Skills

Read the project directory at the skills repository root. Check every existing `SKILL.md` to confirm:
- No existing skill already covers this domain
- No naming conflict with the proposed skill name
- Identify patterns or MCP tools that the new skill could reuse

Present findings:
> "I found [N] existing skills. None overlap with your request. The closest is [skill-name], which [brief description]. I'll proceed with creating [new-skill-name]."

If overlap is found, propose either extending the existing skill or differentiating the new one. Ask the user to decide.

### 1B: Domain Research (if applicable)

If the skill domain benefits from external context (industry patterns, API docs, competitor tools):

- Use **Context7 MCP** to fetch library/framework documentation when the skill wraps a specific technology
- Use **Social Toolkit MCP** or **SearchAPI MCP** if the skill involves social media, web scraping, or market research
- Use **PerplexitySonarSearchTool** for general domain overviews
- Read any files the user provides (docs, specs, examples)

Summarize key findings that should inform the skill's instructions.

---

## Step 2: Plan Resources

Based on requirements, decide which supporting files the skill needs. Present the plan as a directory tree:

```
skill-name/
+-- SKILL.md              # Core skill (target: 1,500-2,000 words)
+-- references/            # Detailed domain docs (optional)
|   +-- patterns.md
|   +-- api-reference.md
+-- examples/              # Working code samples (optional)
|   +-- example1.sh
|   +-- example2.json
+-- assets/                # Templates, HTML, config files (optional)
|   +-- template.html
+-- evals/                 # Evaluation data for testing (optional)
    +-- evals.json
```

**Rules:**
- SKILL.md stays lean (1,500-2,000 words). Move detailed content to `references/`.
- Only create directories that have files in them.
- Reference files use markdown. Example files use the appropriate language.
- Asset files are production-ready templates, not stubs.

Confirm the resource plan with the user before writing files.

---

## Step 3: Write SKILL.md

### 3A: Frontmatter

Write YAML frontmatter with exactly two fields:

```yaml
---
name: skill-name
description: "One-line purpose. Detailed trigger description. Use this skill when the user says things like: 'phrase 1', 'phrase 2', 'phrase 3', 'phrase 4', or [contextual triggers]."
---
```

**Frontmatter rules:**
- `name` — lowercase kebab-case, matches the directory name
- `description` — a single long string (not multiline YAML). Start with a one-line purpose, then list concrete trigger phrases in quotes. Use third-person format: "Use this skill when the user says..."

### 3B: Body Structure

Follow this template structure, adapting sections to the skill's needs:

```markdown
# Skill Title

One-paragraph summary of what the skill does and how it differs from a naive approach.

## Workflow Overview

[ASCII diagram showing the pipeline from input to output]

---

## Step 0: [Initial Input / Gather Inputs]

[What to ask the user or detect from their message]

## Step 1: [First Major Phase]

[Instructions in imperative form]

## Step 2: [Second Major Phase]

[Instructions in imperative form]

...

## Step N: [Final Output / Delivery]

[How to present results, deploy, or save output]
```

### 3C: Writing Style Rules

Follow these rules strictly when writing the SKILL.md body:

- **Imperative form** — "Fetch the profile", "Extract key themes", "Generate the HTML". Not "You should fetch" or "We will fetch".
- **No second-person** — Never use "you" or "your". Use "the user" when referring to the person invoking the skill.
- **Lean body** — Target 1,500-2,000 words in SKILL.md. Move detailed reference material, protocol descriptions, or extensive code examples to `references/`.
- **Tables for structured inputs** — Use markdown tables when listing inputs, parameters, or options.
- **MCP tools by name** — Reference MCP tools explicitly (e.g., `FetchInstagramProfileTool`, `google_maps_search`, `notion-create-pages`).
- **ASCII workflow diagrams** — Use indented arrow diagrams for pipeline overviews.
- **Step numbering** — Use "Step 0", "Step 1", etc. Step 0 is always input gathering.
- **Parallel operations** — When multiple independent operations can run simultaneously, note "Fetch all in parallel" or "Run these in parallel".
- **Confirm before proceeding** — At key decision points, include a confirmation prompt pattern: `> "Here's what I have: [summary]. Ready to proceed?"`
- **Output strategy** — Specify where output goes (`/tmp/`, project directory, Cloudflare Workers, Notion) and how to present it (open in browser, return URL, save file).

---

## Step 4: Create Supporting Files

Write all planned supporting files:

- **References** — Detailed markdown docs covering domain knowledge, API patterns, protocol specs, or advanced techniques that would bloat SKILL.md.
- **Examples** — Complete, working code samples. Not stubs or pseudocode.
- **Assets** — Production-ready templates (HTML with proper structure, JSON with realistic data).
- **Evals** — Test scenarios in JSON format for validating skill behavior.

Every file referenced in SKILL.md must exist. Verify all cross-references after creation.

---

## Step 5: Validate

Run through this checklist before presenting the skill as complete:

| Check | Criteria |
|-------|----------|
| Frontmatter | Has `name` and `description` fields |
| Description | Includes 4+ concrete trigger phrases in quotes |
| Name match | `name` field matches directory name (kebab-case) |
| Word count | SKILL.md body is 1,500-2,000 words |
| Writing style | Imperative form, no "you/your", no second-person |
| Workflow diagram | ASCII pipeline diagram present |
| Step structure | Steps numbered starting from 0 |
| File references | All referenced files exist |
| No duplication | No overlap with existing skills |
| MCP tools | Referenced by correct tool name |

If any check fails, fix it before proceeding.

---

## Step 6: Update README

Add the new skill to the project `README.md` following the established format:

1. Add a new `### skill-name` section under "Available Skills" with:
   - 2-3 sentence description
   - Bullet list of key capabilities (4-7 bullets)
   - Install command: `npx skills add AAlvAAro/skills@skill-name`

2. Add a `/skill-name` entry to the Workflow section at the bottom with a brief description.

Match the tone and detail level of existing README entries.

---

## Conventions Reference

These patterns are established across existing skills in this repository. Follow them for consistency:

- **Research-first approach** — Skills that produce content should research before generating.
- **Document check** — If the skill can accept input docs, always ask "Do you have a brief/doc I should start from?" before guided questions.
- **Question batching** — Group related questions into rounds (max 3 rounds). Never ask one question at a time.
- **Confirmation gates** — Summarize and confirm before major phases (research, generation, deployment).
- **HTML output pattern** — Generate self-contained HTML, save to `/tmp/skill-name/` or a project-specific directory, open in the default browser.
- **Cloudflare deployment** — For shareable output, deploy via `wrangler` to Cloudflare Workers.
- **Notion integration** — Use `notion-create-pages` for structured storage, `notion-search` and `notion-fetch` for reading.
- **Language detection** — Default to auto-detecting language from content. Support explicit language override.
- **Parallel MCP calls** — When fetching from multiple sources, call all MCP tools in parallel.
