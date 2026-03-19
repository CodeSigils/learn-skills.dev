---
name: opencode-skill-creator
description: Creates new skills for Opencode following established conventions. Use when the user wants to create a new skill, extend an existing skill, or needs guidance on Opencode's skill architecture. Triggers on requests like "create a skill", "add a new rule", or "how do skills work in Opencode".
---

# Opencode Skill Creator

Guide for creating skills compatible with Opencode's agent system.

## About Opencode Skills

Skills in Opencode are modular knowledge packages that extend agent capabilities. They follow a structure optimized for both human review and agent consumption:

```
skill-name/
├── SKILL.md              # Core skill definition (metadata + core instructions)
├── rules/                # Specific rules and patterns
│   ├── rule-1.md
│   └── rule-2.md
└── AGENTS.md             # Expanded reference for agents
```

## When to Use This Skill

Use this skill when:
- User asks to "create a new skill"
- User wants to add rules to an existing skill
- User asks how skills work in Opencode
- User needs help structuring domain expertise into a skill
- User wants to document patterns and best practices

## Core Principles

### Concise and Context-Efficient

Opencode shares the context window across system prompt, conversation, skills metadata, and user requests.

**Rule of thumb:** Only add what Claude doesn't already know. Challenge every paragraph.

### Match Freedom to Fragility

- **High freedom (guidelines)**: When context determines the approach
- **Medium freedom (patterns)**: When a preferred pattern exists with some variation
- **Low freedom (scripts/templates)**: When consistency is critical

## Skill Structure

### SKILL.md

Required frontmatter:
```yaml
---
name: skill-name
description: Clear description of what the skill does and when to use it. Include triggers.
---
```

Body sections:
- **Overview**: What the skill provides
- **When to Use**: When this skill applies (redundant if description is good)
- **Core Concepts**: Essential domain knowledge
- **Rules/Patterns**: Specific guidelines with examples
- **Quick Reference**: Common patterns

### rules/ Directory

Individual rule files for specific patterns. Each rule:
- Has YAML frontmatter with title, impact, and tags
- Shows Incorrect → Correct code examples
- Is referenced from SKILL.md

Frontmatter format:
```yaml
---
title: Rule Title
impact: HIGH|MEDIUM|LOW
impactDescription: Brief impact statement
tags: tag1, tag2, tag3
---
```

### AGENTS.md

Expanded reference document combining all rules. Optimized for:
- Agent context loading
- Token efficiency
- Cross-reference navigation

## Skill Creation Workflow

### Step 1: Understand the Domain

Gather concrete examples from the user:
- "What tasks should this skill handle?"
- "Give me examples of how you'd use it"
- "What triggers should activate this skill?"

### Step 2: Plan the Structure

Determine:
- **SKILL.md**: Core workflow + selection guidance
- **rules/**: Individual patterns (max 5-10 core rules)
- **AGENTS.md**: Full expansion of rules
- **Bundled resources**: Scripts, templates, references as needed

### Step 3: Create the Skill Directory

```bash
mkdir -p skill-name/{rules,scripts,references,assets}
touch skill-name/SKILL.md skill-name/AGENTS.md
```

### Step 4: Write SKILL.md

Frontmatter requirements:
- `name`: kebab-case, descriptive
- `description`: Complete "when to use" - Claude reads only this for triggering

Body structure:
```markdown
# Skill Name

## Overview
Brief description of what this skill provides.

## When to Use
List of triggers and contexts that activate this skill.

## Core Concepts
Essential domain knowledge (concise).

## Rules
Reference to rule files with brief context.

## Quick Reference
Common patterns and examples.
```

### Step 5: Write Rules

Create individual rule files in `rules/`:
- Use frontmatter for discoverability
- Show Incorrect → Correct patterns
- Keep examples concise
- Tag appropriately for grep-based discovery

### Step 6: Generate AGENTS.md

Expand all rules into a single document for agent reference:
- Maintain rule order from SKILL.md
- Include full examples and explanations
- Add table of contents for navigation
- Cross-reference related rules

### Step 7: Validate Structure

Verify:
```
skill-name/
├── SKILL.md              # Valid frontmatter, concise body
├── rules/
│   └── *.md              # Valid frontmatter, code examples
└── AGENTS.md             # Full rule expansion
```

## Progressive Disclosure

Keep SKILL.md under 500 lines. Move details to:
- `rules/*.md` for specific patterns
- `references/*.md` for domain documentation
- `scripts/*.sh` or `*.py` for deterministic operations

## Example: Creating a New Skill

1. User: "I want a skill for validating React props"
2. You: Ask for examples, triggers, and constraints
3. Plan: SKILL.md + rules/prop-types.md + rules/validation-patterns.md
4. Create files following structure above
5. Validate with `ls -F` and frontmatter check

## Testing the Skill

After creation:
1. Verify triggering: Does it activate for relevant requests?
2. Verify content: Are rules discoverable via grep?
3. Verify examples: Do code samples work?
4. Verify structure: Are files in correct locations?

## Common Patterns

### Pattern: Adding a New Rule

1. Create `rules/new-rule.md` with frontmatter
2. Add reference in SKILL.md under "Rules"
3. Expand into AGENTS.md
4. Tag appropriately for discoverability

### Pattern: Updating an Existing Skill

1. Identify what changed (new patterns, framework updates)
2. Update relevant rule files
3. Sync changes to AGENTS.md
4. Keep frontmatter updated (version, tags)

## Quick Reference

| Component | Purpose | Size Limit |
|-----------|---------|------------|
| SKILL.md | Triggering + core workflow | <500 lines |
| rules/*.md | Specific patterns | Unlimited |
| AGENTS.md | Full reference | Unlimited |
| scripts/* | Deterministic code | N/A |
| references/* | Domain docs | N/A |

## File Naming Conventions

- Skills: `kebab-case` (e.g., `react-best-practices`)
- Rules: `kebab-case` with descriptive name (e.g., `rerender-defer-reads.md`)
- References: `UPPERCASE.md` for major docs (e.g., `GUIDELINES.md`)
- Scripts: `kebab-case.{sh,py,js}`

## Integration Points

Skills are discovered via:
1. Frontmatter `description` matching user request
2. Grep search in `.cursor/skills/`, `.agents/skills/`, `.opencode/skills/`
3. File content matching (tags in rules)

Ensure descriptions and tags cover:
- Functional domain (e.g., "React", "SQL", "Docker")
- Task type (e.g., "optimization", "debugging", "migration")
- Trigger phrases (e.g., "create skill", "optimize component")
