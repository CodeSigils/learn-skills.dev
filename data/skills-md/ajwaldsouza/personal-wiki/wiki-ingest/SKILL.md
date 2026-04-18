---
name: wiki-ingest
description: >
  Process raw source documents into wiki pages. Use when the user adds
  files to raw/ and wants them ingested, says "process this source",
  "ingest this article", "I added something to raw/", or wants to
  incorporate new material into their wiki, second brain, or knowledge base.
allowed-tools: Bash Read Write Edit Glob Grep
---

# Personal Wiki — Ingest

Process raw source documents into structured, interlinked wiki pages.

## Identify Sources to Process

Determine which files need ingestion:

1. If the user specifies a file or files, use those
2. If the user says "process new sources", "ingest", or similar without specifying files — run batch detection:
   - List all files in `raw/` (excluding `raw/assets/`)
   - Read `wiki/log.md` and extract all previously ingested source filenames from `ingest` entries
   - Any file in `raw/` not listed in the log is unprocessed
   - Show the user the list of unprocessed files found
3. If no unprocessed files are found, tell the user

## Process Each Source

For each source file, process autonomously — read, create pages, and report results. No confirmation step between sources.

### 1. Read the source completely

Read the entire file. If the file contains image references, note them — read the images separately if they contain important information.

For books: support both chapter-by-chapter and whole-book ingestion. When ingesting a chapter, create or update a parent book page in `wiki/sources/` that links to all chapter summaries. When ingesting a whole book, create a single comprehensive source page.

### 2. Create source summary page

Create a new file in `wiki/sources/` named after the source (slugified). Include:

    ---
    tags: [relevant, tags]
    sources: [original-filename.md]
    created: YYYY-MM-DD
    updated: YYYY-MM-DD
    ---

    # Source Title

    **Source:** original-filename.md
    **Date ingested:** YYYY-MM-DD
    **Type:** article | paper | transcript | notes | book | chapter | etc.

    ## Summary

    Structured summary of the source content. Each paragraph ends with
    an inline citation to this source: ([[Source - Title]]).

    ## Key Claims

    - Claim 1
    - Claim 2
    - ...

    ## Entities Mentioned

    - [[Entity Name]] — brief context
    - ...

    ## Concepts Covered

    - [[Concept Name]] — brief context
    - ...

### 3. Update entity and concept pages

For each entity (person, organization, product, tool) and concept (idea, framework, theory, pattern) mentioned in the source:

**If a wiki page already exists:**
- Read the existing page
- Add new information from this source, citing it inline: `([[Source - Title]])`
- Review existing uncited paragraphs — add citations using the page's `sources:` frontmatter to determine which source each paragraph came from
- Add the source to the `sources:` frontmatter list
- Update the `updated:` date
- Flag any contradictions with existing content using a callout block:

```
> [!warning] Contradiction
> Source A claims X, but Source B claims Y.
> Sources: [[Source A]], [[Source B]]
```

**If no wiki page exists and the topic is substantive enough:**
- Create a new page in the appropriate subdirectory:
  - `wiki/entities/` for people, organizations, products, tools
  - `wiki/concepts/` for ideas, frameworks, theories, patterns
- Include YAML frontmatter with tags, sources, created, and updated fields
- Write a focused summary based on what this source says about the topic
- Every paragraph must end with an inline citation: `([[Source - Title]])`

**If the topic is only mentioned in passing:**
- Use a `[[wikilink]]` without creating a page — the lint pass will flag frequently-mentioned-but-missing pages later

### 4. Add wikilinks

Ensure all related pages link to each other using `[[wikilink]]` syntax. Every mention of an entity or concept that has its own page should be linked.

### 5. Update wiki/index.md

For each new page created, add an entry under the appropriate category header:

    - [[Page Name]] — one-line summary (under 120 characters)

### 6. Update wiki/log.md

Append:

    ## [YYYY-MM-DD] ingest | Source Title
    Processed source-filename.md. Created N new pages, updated M existing pages.
    New entities: [[Entity1]], [[Entity2]]. New concepts: [[Concept1]].

### 7. Report results

Tell the user what was done:
- Pages created (with links)
- Pages updated (with what changed)
- New entities and concepts identified
- Any contradictions found with existing content

When processing multiple sources (batch), report aggregate results at the end:
- Total sources processed
- Total pages created and updated
- Summary of new entities and concepts across all sources

## Conventions

- Tags are **organic** — let them emerge naturally from content. Don't force a domain taxonomy. When a source spans multiple domains, tag with all relevant domains.
- Source summary pages are **factual only**. Save interpretation and synthesis for concept and synthesis pages.
- A single source typically touches **10-15 wiki pages**. This is normal and expected.
- When new information contradicts existing wiki content, **add a `> [!warning] Contradiction` callout** with both sources cited.
- **Prefer updating existing pages** over creating new ones. Only create a new page when the topic is substantive enough to warrant it.
- Use `[[wikilinks]]` for all internal references. Never use raw file paths.

## Citations

Every factual paragraph on entity, concept, and source summary pages must end with an inline parenthetical citation linking to the source summary page.

- **Format:** `([[Source - Article Title]])` — wikilink to the source page in `wiki/sources/`
- **Granularity:** Per paragraph — cite at the end of each paragraph
- **Multiple sources:** Comma-separated — `([[Source - A]], [[Source - B]])`
- **Updates:** When adding new information to an existing page, cite the new source. Also backfill citations on any existing uncited paragraphs using the page's `sources:` frontmatter.
- **Source summary pages:** Paragraphs in the Summary section cite the source being summarized.

Example:

```
Neural networks learn through backpropagation, where error gradients
flow backward through layers to adjust weights ([[Source - Deep Learning
Fundamentals]]).

This mechanism mirrors biological feedback loops observed in neural
plasticity ([[Source - Deep Learning Fundamentals]], [[Source -
Neuroscience of Learning]]).
```

## What's Next

After ingesting sources, the user can:
- **Ask questions** with `/wiki-query` to explore what was ingested
- **Ingest more sources** — clip another article and run `/wiki-ingest` again
- **Health-check** with `/wiki-lint` after every 10 ingests to catch gaps
- **Discover connections** with `/wiki-explore` to find cross-domain patterns
- **Get inspired** with `/wiki-spark` to generate creative prompts
