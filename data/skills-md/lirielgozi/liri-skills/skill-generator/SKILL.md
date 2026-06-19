---
name: skill-generator
description: Automates the creation of new skills by following the liri-skills framework with research, structure, and template generation
version: 1.0.0
author: liri-skills
tags: [meta, automation, scaffolding, generator]
---

# Skill Generator

> Automates the creation of new liri-skills with research-driven design, proper structure, and intelligent scaffolding

## When to Use

- Creating a new skill from scratch
- Need consistent skill structure across the project
- Want research-driven skill design with best practices
- Building skills with multiple sub-agents and workflows
- Ensuring modularity and maintainability from the start

## When NOT to Use

- Modifying existing skills (edit directly instead)
- Creating one-off scripts (not a full skill)
- Tasks that don't fit the skill pattern

---

## Orchestrator

This skill coordinates the following sub_agents:

| Sub-Agent | Purpose | Invoked During |
|-----------|---------|----------------|
| `context-enhancer` | Expands and clarifies user input into comprehensive context | Phase 0 |
| `requirements-gatherer` | Collects user requirements interactively | Phase 1 |
| `domain-researcher` | Researches best practices via web search | Phase 2 |
| `structure-builder` | Creates directory structure and scaffolds | Phase 3 |
| `template-generator` | Generates main skill file with orchestrator | Phase 4 |

---

## Workflows

### Primary: Create Skill (Full)
**Path**: `workflows/create-skill.md`

Complete workflow with context enhancement and research:
0. **Enhance Context** → Expand and clarify user input
1. **Gather Requirements** → Interactive Q&A (pre-populated from context)
2. **Research Domain** → Web search for best practices
3. **Build Structure** → Create directories and scaffolds
4. **Generate Templates** → Create main skill file
5. **Register & Validate** → Update registry, verify structure

### Secondary: Quick Create
**Path**: `workflows/quick-create.md`

Fast workflow for simple skills:
0. Light context enhancement (optional)
1. Minimal requirements gathering
2. Skip research phase
3. Basic structure creation
4. Placeholder templates with TODOs

---

## Context Integration

### Shares Context With
- `registry.yaml`: Skill metadata for discovery
- All generated skills: Structure patterns and conventions

### Receives Context From
- User input: Skill requirements and preferences
- Web search: Domain best practices and patterns

---

## Commands

### `/skill-generator` or `/skill-generator:create`
Full skill creation workflow with research.

**Usage**:
```
/skill-generator
> Follow interactive prompts to define your skill
```

### `/skill-generator:quick`
Quick skill creation without research phase.

**Usage**:
```
/skill-generator:quick <skill-name> "<description>"
```

### `/skill-generator:research <skill-name>`
Run research phase for an existing skill (fills RESEARCH.md).

**Usage**:
```
/skill-generator:research my-skill
```

### `/skill-generator:enhance "<description>"`
Run context enhancement standalone to clarify and expand input.

**Usage**:
```
/skill-generator:enhance "I want a skill that helps with API testing"
```

**Output**: Enhanced context document with background, examples, scope, and structured summary. Can be used to refine ideas before full skill creation.

---

## Implementation

### Entry Point Logic

When `/skill-generator` is invoked:

```
1. Parse command arguments
2. Determine workflow (full or quick)
3. Initialize state tracker
4. Run context enhancement (Phase 0)
5. Execute remaining workflow steps sequentially
6. Handle errors with rollback
7. Report final status
```

### State Management

Track progress through skill creation:

```yaml
state:
  workflow: create-skill | quick-create
  current_phase: 0-5
  enhanced_context: null | EnhancedContextObject
  requirements: null | RequirementsObject
  research: null | ResearchObject
  structure: null | StructureObject
  errors: []
  rollback_actions: []
```

---

### Phase 0: Context Enhancement

**Dispatch to**: `sub_agents/context-enhancer.md`

**Orchestrator Actions**:
1. Accept user's raw input (can be brief/vague)
2. Invoke context-enhancer sub-agent
3. Analyze input for intent, domain, gaps
4. Expand with background and terminology
5. Clarify problem statement (what/why/who)
6. Generate examples and scope boundaries
7. Present enhanced context for user review
8. Store in state, save to `references/CONTEXT.md`

**Enhancement Pipeline**:

```
Raw Input → Analysis → Expansion → Clarification → Examples → Structured Output
```

**Output Structure**:
```yaml
enhanced_context:
  original_input: "user's brief description"
  expanded_description: "detailed, clarified version"
  background:
    domain: "primary domain"
    terminology: {term: definition}
  problem_statement:
    what: "concrete description"
    why: "motivation and value"
    who: "target users"
  scope:
    core: ["must-have capabilities"]
    extended: ["nice-to-have"]
    excluded: ["out of scope"]
  examples:
    use_cases: ["scenario descriptions"]
    input_output: [{input: "", output: ""}]
  structured_summary: "formatted for Claude"
```

**Checkpoint**: User reviews enhanced context, can refine before proceeding

---

### Phase 1: Requirements Gathering

**Dispatch to**: `sub_agents/requirements-gatherer.md`

**Input**: Enhanced context from Phase 0

**Orchestrator Actions**:
1. Pre-populate fields from enhanced context
2. Invoke requirements-gatherer sub-agent
3. Validate returned requirements object
4. Store in state
5. Present summary for user confirmation

**Prompt Sequence**:
1. Identity: skill name (kebab-case), one-sentence description
2. Purpose: problem it solves
3. Tasks: 2-10 tasks, mark sub-agent candidates
4. Integrations: web search, APIs, CLI, MCP, none
5. Collaboration: related skills

**Validation** (per Claude skill best practices):
- skill_name matches `/^[a-z][a-z0-9-]*$/` (max 64 chars)
- skill_name cannot contain "anthropic" or "claude"
- description ≤ 1024 characters (written in third-person)
- description includes what it does AND when to use it
- tasks count between 2-10
- At least one sub-agent if tasks > 4

**Error Handling**:
- Invalid skill_name → Suggest correction, re-prompt
- Too broad scope → Suggest splitting into multiple skills
- Duplicate name → Check registry, warn user

---

### Phase 2: Domain Research

**Dispatch to**: `sub_agents/domain-researcher.md`

**Orchestrator Actions**:
1. Inform user research is starting
2. Construct search queries from requirements
3. Invoke domain-researcher sub-agent
4. Monitor progress (show what's being searched)
5. Store research findings in state
6. Create `references/RESEARCH.md`

**Search Query Construction**:

```python
queries = [
    f"{requirements.purpose} best practices {current_year}",
    f"{requirements.domain} implementation patterns",
    f"Claude Code skill {requirements.similar_functionality}",
    f"{requirements.tasks[0]} automation tools",
]
```

**Research Output Structure**:

```yaml
sources_reviewed:
  - url: "https://..."
    title: "..."
    key_insight: "..."
    applicable: true/false

best_practices:
  - practice: "..."
    source: "..."
    priority: high/medium/low

techniques_to_avoid:
  - technique: "..."
    reason: "..."

recommended_architecture:
  pattern: "orchestrator-workers"
  sub_agents:
    - name: "..."
      responsibility: "..."
  workflows:
    - name: "..."
      steps: [...]
```

**Progress Updates**:
```
🔍 Researching: "{query}"
   Found: {N} relevant sources

📚 Analyzing: {source_title}
   Key insight: {insight}

✓ Research complete: {N} sources, {M} best practices identified
```

**Error Handling**:
- No results → Broaden search terms, try alternative queries
- Rate limited → Wait and retry with backoff
- Timeout → Save partial results, continue with available data

---

### Phase 3: Structure Building

**Dispatch to**: `sub_agents/structure-builder.md`

**Orchestrator Actions**:
1. Determine target path: `skills/{skill_name}/`
2. Verify path doesn't exist (or confirm overwrite)
3. Invoke structure-builder sub-agent
4. Create directories
5. Scaffold sub-agent files
6. Scaffold workflow files
7. Create script placeholders
8. Verify structure completeness

**Directory Creation**:

```bash
.claude/
├── agents/
│   └── {skill_name}.md           # Orchestrator agent
│
└── skills/{skill_name}/
    ├── SKILL.md                  # Main file (MUST be named SKILL.md)
    ├── references/
    │   └── RESEARCH.md           # From Phase 2
    ├── scripts/                  # Based on integrations
    ├── sub_agents/               # One per identified task
    │   ├── {task_1}.md
    │   ├── {task_2}.md
    │   └── ...
    └── workflows/                # Based on research
        └── primary-workflow.md
```

**IMPORTANT**:
- The main skill file MUST be named `SKILL.md` (not `{skill_name}.md`). This is required by Claude's skill discovery system.
- An orchestrator agent is ALWAYS created at `.claude/agents/{skill_name}.md` to coordinate sub-agents.

**Scaffold Templates**: See `../.template/` for sub-agent and workflow templates.
Each scaffold includes: Purpose, Inputs/Outputs, Process steps, Error handling.

**Progress Updates**:
```
📁 Creating: skills/{skill_name}/
   ├── references/ ✓
   ├── scripts/ ✓
   ├── sub_agents/ ✓
   │   ├── {sub_agent_1}.md ✓
   │   └── {sub_agent_2}.md ✓
   └── workflows/ ✓
       └── primary-workflow.md ✓
```

**Error Handling**:
- Directory exists → Prompt: overwrite/rename/cancel
- Permission denied → Report, suggest fix
- Disk full → Abort with clear message

---

### Phase 4: Template Generation

**Dispatch to**: `sub_agents/template-generator.md`

**Orchestrator Actions**:
1. Collect all inputs (requirements, research, structure)
2. Invoke template-generator sub-agent
3. Generate main skill file (SKILL.md)
4. Generate orchestrator agent (`.claude/agents/{skill_name}.md`)
5. Validate line count (target: 500-550)
6. Adjust if needed (move content to references)
7. Write final files

**Template Sections**:

1. **YAML Frontmatter** (required):
   ```yaml
   ---
   name: skill-name          # lowercase, hyphens, max 64 chars
   description: Does X and Y. Use when Z.  # max 1024 chars, third-person
   ---
   ```
2. **Title and Quick Start** (most important info first)
3. **When to Use / When NOT to Use**
4. **Orchestrator Table** (sub-agents and purposes)
5. **Workflows Section** (references to workflow files)
6. **Context Integration** (collaborations)
7. **Commands** (invocation patterns)
8. **Implementation** (orchestrator logic)

**Best Practice**: Description must include BOTH what the skill does AND when to use it.

**Line Count Management** (per Claude best practices):

```
Target: Under 500 lines (optimal performance)

If > 500:
  - Move detailed examples to references/
  - Use progressive disclosure (link to separate files)
  - Summarize verbose sections
  - Claude reads additional files only when needed

Key principles:
  - Be concise: Claude is smart, don't over-explain
  - Use progressive disclosure: SKILL.md → reference files
  - Keep references one level deep from SKILL.md
```

**Validation Checklist**:
- [ ] YAML frontmatter valid
- [ ] All sub-agents referenced exist
- [ ] All workflows referenced exist
- [ ] Line count: {actual} (target: 500-550)
- [ ] No orphan placeholders
- [ ] Orchestrator agent created at `.claude/agents/{skill_name}.md`
- [ ] Agent references SKILL.md correctly

---

### Phase 5: Registration & Validation

**Orchestrator Actions**:
1. Read current `skills/registry.yaml`
2. Add new skill entry
3. Write updated registry
4. Run final validation
5. Report success/issues

**Registry Entry**:

```yaml
- name: {skill_name}
  description: {description}
  path: skills/{skill_name}/SKILL.md
  tags: [{derived_tags}]
  collaborates_with: [{from_requirements}]
  created: {timestamp}
  version: 1.0.0
```

**Final Validation**:

```
✓ Validating skill structure...

Directory Structure:
  ✓ .claude/skills/{skill_name}/ exists
  ✓ SKILL.md exists ({line_count} lines)
  ✓ references/CONTEXT.md exists (enhanced input)
  ✓ references/RESEARCH.md exists
  ✓ sub_agents/ contains {N} files
  ✓ workflows/ contains {M} files

Orchestrator Agent:
  ✓ .claude/agents/{skill_name}.md exists
  ✓ References SKILL.md correctly
  ✓ Lists all sub-agents
  ✓ Contains workflow references

Content Validation:
  ✓ YAML frontmatter valid (name + description required)
  ✓ name: lowercase, hyphens only, max 64 chars
  ✓ description: max 1024 chars, third-person
  ✓ Body under 500 lines
  ✓ All sub-agent references resolve
  ✓ All workflow references resolve
  ✓ No broken internal links

Registry:
  ✓ Added to skills/registry.yaml
```

---

### Error Handling & Rollback

**Rollback Strategy**:

Each phase records rollback actions:

```yaml
rollback_actions:
  - action: delete_directory
    path: skills/{skill_name}
  - action: restore_registry
    backup: {original_content}
```

**On Failure**:
1. Stop current phase
2. Execute rollback actions in reverse order
3. Report what failed and why
4. Suggest manual resolution

**Common Errors**:

| Error | Phase | Resolution |
|-------|-------|------------|
| Input too vague | 0 | Generate clarifying questions |
| Invalid skill name | 1 | Re-prompt with valid format |
| Research timeout | 2 | Continue with partial data |
| Directory exists | 3 | Prompt overwrite/rename |
| Line count exceeded | 4 | Auto-refactor to references |
| Registry conflict | 5 | Prompt resolution |

---

### Success Output

```
╔════════════════════════════════════════════════════════════╗
║  ✓ Skill Created Successfully!                             ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  📁 Skill: .claude/skills/{skill_name}/                    ║
║  🤖 Agent: .claude/agents/{skill_name}.md                  ║
║                                                            ║
║  Files Created:                                            ║
║    • SKILL.md ({line_count} lines)                         ║
║    • Orchestrator agent                                    ║
║    • references/CONTEXT.md (enhanced input)                ║
║    • references/RESEARCH.md                                ║
║    • sub_agents/ ({N} agents)                              ║
║    • workflows/ ({M} workflows)                            ║
║                                                            ║
║  Next Steps:                                               ║
║    1. Review generated files                               ║
║    2. Expand sub-agent implementations                     ║
║    3. Test with: /{skill_name}                             ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

---

## Configuration

| Setting | Default | Override Flag |
|---------|---------|---------------|
| target_lines | 500-550 | `--lines=N` |
| research_timeout | 60s | `--timeout=N` |
| max_sub_agents | 8 | `--max-agents=N` |
| skills_root | skills/ | `--root=PATH` |

---

## Orchestrator Agent

This skill has an associated orchestrator agent at `.claude/agents/skill-generator.md` that coordinates the sub-agents through phases. The orchestrator:

- Enhances user context (Phase 0)
- Gathers requirements interactively (Phase 1)
- Researches domain best practices (Phase 2)
- Builds directory structure and scaffolds (Phase 3)
- Generates templates and orchestrator agents (Phase 4)
- Registers and validates the new skill (Phase 5)

---

## References

- `references/RESEARCH.md` - Research findings for this skill
- `sub_agents/*.md` - Sub-agent documentation
- `workflows/*.md` - Workflow definitions
- `../registry.yaml` - Skill registry
- [Claude Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) - Official documentation

## Claude Skill Requirements Summary

| Requirement | Value |
|-------------|-------|
| Main file name | `SKILL.md` (required) |
| `name` field | lowercase, hyphens, max 64 chars |
| `description` field | max 1024 chars, third-person, includes triggers |
| Body length | Under 500 lines for optimal performance |
| File references | One level deep from SKILL.md |
| Reserved words | Cannot use "anthropic" or "claude" in name |
