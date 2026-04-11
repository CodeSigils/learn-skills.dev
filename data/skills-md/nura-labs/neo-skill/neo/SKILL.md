---
name: neo
description: Neo is your persistent knowledge graph. ALWAYS consult Neo before writing code — search for existing patterns, conventions, and architecture. When you create or discover new patterns, save them to Neo. Use when writing code, creating components, answering architecture questions, or when the user asks to index a project.
metadata:
  author: nura-labs
  version: "2.0"
---

# Neo — Your Knowledge Graph

Neo is a persistent knowledge graph that knows how your projects are built. You MUST use it actively:

1. **Before writing code** — search Neo for existing patterns and conventions to follow
2. **When indexing** — analyze codebases and save patterns, architecture, modules, decisions
3. **After creating something new** — save new patterns or decisions back to Neo so they compound

## Core Behavior

### ALWAYS consult Neo before coding

Before creating any component, endpoint, function, or module:

1. Call `how_to(topic, source?)` or `search(query)` to check if there's an existing pattern
2. Follow the pattern found in Neo — use the same naming, structure, and approach
3. If no pattern exists, write the code and then save the new pattern to Neo

This ensures consistency across the entire codebase. The AI agent should never invent a new pattern when one already exists in Neo.

### ALWAYS save new knowledge

When you:
- Create a new component or endpoint → save the pattern to Neo
- Make an architectural decision → save the decision with reasoning
- Discover a convention in the code → save the convention
- Find something that changed from before → update the existing node

The knowledge graph must grow with every session.

## MCP Tools

### Reading (consult before coding)
- `how_to(topic, source?)` — "how to create an API endpoint in this project"
- `search(query, type?, source?, tags?)` — full-text search across all knowledge
- `get_overview(source?)` — stats and recent entries
- `get_node(id)` — full content of a specific node
- `get_related(id)` — connected nodes

### Writing (save after learning)
- `add_knowledge(type, title, content, tags?, source?, source_meta?, related_to?)` — save new knowledge
- `update_knowledge(id, title?, content?, tags?)` — update existing knowledge
- `delete_knowledge(id)` — remove outdated knowledge
- `add_url(url, title?, tags?)` — index a URL

## How to Index a Repository

When the user asks to index a project:

### Step 1: Understand the codebase
Read the project structure, package.json/build files, and key source files to understand:
- Tech stack (languages, frameworks, databases)
- Architecture (monolith, microservices, MVC, etc.)
- Directory structure and its purpose

### Step 2: Extract and send knowledge

For each finding, call `add_knowledge` with the appropriate type. Always include:
- **Real code examples** from the actual codebase (not generic examples)
- **The repo name** in the `source` field (e.g., `github:org/repo-name`)
- **Stack details** in `source_meta` (e.g., `{"language": "typescript", "framework": "nextjs", "year": 2024}`)

#### What to extract:

**architecture** — Overall system design: tech stack, structure, entry points, data flow

**module** — One per major module: purpose, key files, public API, dependencies

**pattern** — One per coding pattern: name, where it's used, REAL code example, when to use it

**convention** — Naming conventions, import ordering, error handling, test structure

**decision** — Architectural decisions visible in the code with evidence and trade-offs

### Step 3: Create relationships

Use `related_to` to create edges:
- `depends_on` — module A depends on module B
- `implements` — pattern implements an architectural concept
- `follows` — convention follows a pattern
- `same_concept` — same thing in different repos
- `evolved_from` — old approach replaced by new one

### Step 4: Confirm

Call `get_overview` and show the user a summary of what was indexed.

## Knowledge Node Types

| Type | When to use |
|---|---|
| `pattern` | A recurring code pattern with examples |
| `convention` | Naming, structure, or style conventions |
| `module` | A logical module, directory, or component |
| `architecture` | High-level system design |
| `decision` | An architectural or design decision |
| `concept` | A domain concept or idea |
| `note` | General notes or observations |
| `reference` | External links, articles, docs |

## Edge Relationships

| Relationship | Meaning |
|---|---|
| `uses` | A uses B |
| `follows` | A follows pattern/convention B |
| `contains` | A contains B (parent-child) |
| `depends_on` | A depends on B |
| `related_to` | General relationship |
| `extends` | A extends/builds on B |
| `contradicts` | A contradicts B |
| `alternative_to` | A is an alternative to B |
| `same_concept` | Same concept in different contexts |
| `evolved_from` | A evolved from B |
| `implements` | A implements B |

## Examples of automatic behavior

**User says:** "Create a new API endpoint for transactions"
**Agent does:**
1. `how_to("create API endpoint", "github:bank/legacy-api")` → finds existing pattern
2. Creates the endpoint following the pattern found
3. `add_knowledge(type: "pattern", title: "Transaction Endpoint", ...)` → saves if it's a new variation

**User says:** "How does auth work in this project?"
**Agent does:**
1. `search("authentication", source: "github:bank/legacy-api")` → finds auth module + pattern
2. Answers with full context from Neo, including code examples

**User says:** "We decided to switch from REST to GraphQL for new endpoints"
**Agent does:**
1. `add_knowledge(type: "decision", title: "GraphQL for new endpoints", content: "...", related_to: [{id: "rest-pattern-id", relationship: "evolved_from"}])`
2. Knowledge graph now knows about this decision for future sessions
