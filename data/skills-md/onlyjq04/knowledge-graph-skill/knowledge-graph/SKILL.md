---
name: knowledge-graph
description: "Create, update, query, and validate project knowledge graphs stored under `knowledge/` using Obsidian-flavored Markdown. Use when the user mentions knowledge graph, knowledge base, project docs, architecture docs, ADRs, Obsidian notes, note organization, docs health checks, broken links, stale docs, or asks to initialize, sync, query, or audit structured project documentation. Use proactively when a workspace contains a `knowledge/` directory: search it before answering project-context questions, making substantial code or design changes, reviewing changes, or updating documentation."
---

# Knowledge Graph

Manage a source-grounded project knowledge graph under `knowledge/`. Keep the graph useful for both Codex and Obsidian: concise notes, YAML frontmatter, wikilinks, callouts, Mermaid diagrams, and clear references back to source files or documents.

## Resource Map

Load only the reference needed for the current operation:

- `references/project-types.md`: project type detection, directory structures, and section name mappings.
- `references/note-templates.md`: note templates, decision record templates, and examples.
- `references/obsidian-syntax.md`: Obsidian-flavored Markdown syntax for wikilinks, embeds, callouts, tags, frontmatter, and Mermaid.

## Proactive Graph Lookup

When working in a workspace that contains `knowledge/`, search the graph before answering project-context questions or making substantial edits.

1. List graph files with `rg --files knowledge`.
2. Read `knowledge/00-index.md` first.
3. Read notes whose filenames, headings, tags, aliases, or source references match the task.
4. Follow wikilinks from the most relevant notes.
5. Verify important claims against the referenced source material before relying on them.
6. Mention stale, missing, or contradictory notes in the response or update them when the user asked for documentation changes.

## Operating Rules

- Verify claims against source material before writing them. Source material may be code, documentation, data files, legal materials, research artifacts, or existing notes.
- Treat existing `knowledge/` contents as user-owned. Preserve established directory names, note names, frontmatter conventions, and link style unless the user asks for a migration.
- Prefer topic-level and flow-level notes over one note per source file.
- Keep every note concise and scannable. Use tables and Mermaid diagrams when they reduce ambiguity.
- Maintain `knowledge/00-index.md` as the navigation source of truth.
- Use Obsidian wikilinks in the form `[[category/note-name]]` for internal graph links.
- Use the current local date for `date`, `last_verified`, and update log entries.
- If source material and existing notes disagree, trust source material and flag the stale note.
- If evidence is missing, state that it is unverified and list the exact source needed.

## Detect Project Type

Use the user's stated project type when provided. Otherwise inspect the workspace and select the strongest match from `references/project-types.md`: software, administrative, legal, research, personal, or general.

For an existing graph, prefer the graph's current structure over a template. Read `knowledge/00-index.md` and list directories under `knowledge/` before creating or moving notes.

## Initialize

Use this flow when the user asks to create, initialize, rebuild, or organize a knowledge graph.

1. Detect project type.
2. Read high-signal source context such as README files, package or build manifests, architecture docs, policy documents, data dictionaries, existing notes, and user-provided materials.
3. Create `knowledge/` and the type-appropriate directories from `references/project-types.md`, unless an existing structure is already present.
4. Create high-value notes from `references/note-templates.md`.
5. Create or update `knowledge/00-index.md` with categories, note links, short descriptions, and coverage gaps.
6. Cross-link related notes with wikilinks.
7. Add YAML frontmatter to every note with at least `title`, `description`, `date`, and `tags`.
8. Add required note sections: Purpose, References or type-specific source section, Related Notes, Key Facts or type-specific equivalent, Open Questions or type-specific equivalent, Update Log, and `last_verified`.

Return the detected project type, notes created, notes updated, coverage gaps, and items needing human review.

## Update

Use this flow when the user asks to sync documentation after project changes, stale docs, or changed files.

1. Identify changed paths from the user's request or from git diff. Include staged and unstaged changes when using git.
2. Read `knowledge/00-index.md` and notes whose source references match changed paths.
3. Classify impact:
   - Patch: typo, comment, or test-only change. Update `last_verified` when the note still matches reality.
   - Minor: refactor, helper, config, procedure, or policy detail change. Update affected content and `last_verified`.
   - Major: behavior, architecture, API, policy, case strategy, research method, or data model change. Update affected notes, links, index entries, and create a decision record when a durable decision was made.
4. Update only affected notes and dependent notes.
5. Add an update log row: `| YYYY-MM-DD | Change summary | Severity - scope |`.
6. Update `knowledge/00-index.md` for new, renamed, deprecated, or removed notes.
7. Flag references to deleted or renamed source files.

Return the changed path to note mapping, impact classification, files updated, stale notes found, and new decision records.

## Query

Use this flow when the user asks what something is, how a system works, why a decision was made, or wants context before acting.

1. Read `knowledge/00-index.md`.
2. Read relevant notes and follow their wikilinks when needed.
3. Verify important claims against referenced source files.
4. Read decision records and known issues for constraints.
5. Do not modify files.

Return:

- Relevant knowledge notes with High, Medium, or Low relevance.
- Relevant source references.
- Constraints and risks.
- Open questions.
- Recommended path with confidence labels: Confirmed, Inferred, or Speculative.
- Knowledge gaps and the exact files or notes that should be added or refreshed.

## Validate

Use this flow when the user asks for a health check, audit, broken link scan, or stale note review.

1. Scan every Markdown file under `knowledge/`.
2. Verify every wikilink target exists.
3. Check that `knowledge/00-index.md` matches files on disk.
4. Check required frontmatter: `title`, `description`, `date`, and `tags`.
5. Check required sections for each note type.
6. Flag notes with `last_verified` older than 30 days.
7. Flag source references that no longer exist.
8. Flag empty sections.
9. Check Mermaid blocks when the graph contains diagrams.
10. Do not modify files unless the user asks for fixes.

Return a health report with counts, specific file paths, errors, warnings, and recommended fixes.

## Note Quality Bar

Every graph note should answer:

- What is this topic and why does it exist?
- What source material supports it?
- What facts are stable enough to rely on?
- What related notes should Codex read next?
- What remains unverified or unresolved?
- When was it last checked?

Use decision records for durable choices that explain why one option was chosen over alternatives. Place them under the existing decisions directory or the project type's `07-decisions/` directory.
