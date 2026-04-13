---
name: neo
description: Neo is your persistent knowledge graph. ALWAYS consult Neo before writing code — search for existing patterns, conventions, and architecture. When you create or discover new patterns, save them to Neo. Use when writing code, creating components, answering architecture questions, or making decisions.
metadata:
  author: nura-labs
  version: "3.0"
---

# Neo — Consult Before Coding

Neo remembers how your projects are built. Before writing any code, check what already exists.

## Rules

1. **Search first** — before creating anything, check if a pattern exists
2. **Follow what you find** — use the same naming, structure, and approach
3. **Save what you create** — new patterns must go back to Neo

## Quick Reference

```
how_to("create API endpoint")          → find the pattern
search("authentication")               → find related knowledge
get_overview()                         → see what's indexed
get_node(id)                           → full content + backlinks
get_related(id)                        → connected nodes
```

## When the Agent Writes Code

```
1. search/how_to → find existing pattern
2. Follow the pattern exactly
3. If no pattern exists → write code → save new pattern with neo-index skill
```

## When the User Asks a Question

```
1. search the topic in Neo
2. Answer with context from Neo, including code examples
3. Cite which nodes you referenced
```
