---
name: literature-review
description: Search, collect, deduplicate, classify, and summarize academic papers into structured literature reviews. Use when the user asks for journal issue/quarter reviews, top-journal tracking, paper summaries, DOI/metadata extraction, research trend analysis, annotated bibliographies, or Excel/Word literature review outputs for journals such as Remote Sensing of Environment, ISPRS JPRS, Nature, Science, IEEE TGRS, or other scholarly sources.
---

# Literature Review

Use this skill for academic literature discovery and synthesis. It is designed for tasks like "summarize 2026 Q1 RSE papers", "track recent papers on remote sensing foundation models", or "create an Excel literature table plus Chinese review".

## Workflow

1. Clarify scope only when needed: journal/source, date range, topic filters, language, output format, and whether full text is required.
2. Collect metadata from primary scholarly indexes before general web search.
   - Prefer OpenAlex for journal/date searches and abstracts.
   - Use Crossref for DOI and publisher metadata fallback.
   - Use publisher pages, arXiv, PubMed, Semantic Scholar, or institutional pages when the user requests full-text or PDF-level review.
3. Save a machine-readable bibliography first, then synthesize.
   - Use `scripts/search_literature.py` for OpenAlex/Crossref retrieval when possible.
   - Keep DOI, URL, source, publication date, abstract, and OA status.
4. Deduplicate by DOI first, then normalized title.
5. Classify papers by topic, method, data source, study region, and application domain.
6. Summarize at two levels:
   - Per-paper structured summary.
   - Cross-paper synthesis of themes, trends, gaps, and recommended reads.
7. Produce the requested artifact.
   - Excel for literature databases.
   - Word/Markdown for narrative review.
   - Both when the user wants a reusable research report.

## Retrieval Script

Use:

```bash
python literature-review/scripts/search_literature.py --journal "Remote Sensing of Environment" --from-date 2026-01-01 --to-date 2026-03-31 --format xlsx --output rse_2026_q1.xlsx
```

Helpful options:

- `--source openalex`: best default for abstracts and OA links.
- `--source crossref`: useful DOI fallback.
- `--source both`: merge OpenAlex and Crossref results.
- `--query "forest biomass"`: add a topic keyword.
- `--max-results 200`: cap result count.

If the script cannot reach an API or returns sparse data, fall back to official publisher pages and web search. Clearly label which fields are inferred or missing.

## Review Schema

For Excel/Word outputs, use the schema in `references/review-schema.md`. Load it when creating tables or reports.

For search-source caveats and API choices, use `references/source-strategy.md`.

## Quality Rules

- Do not invent papers, DOIs, abstracts, issue numbers, or findings.
- Cite metadata source links for each paper when practical.
- Distinguish abstract-level summaries from full-text reviews.
- For paywalled papers, summarize only available metadata/abstract unless the user provides the PDF.
- When ranking "important" papers, explain the ranking basis: relevance, novelty, citations, journal prominence, method importance, or user topic fit.
- Preserve English titles exactly; write Chinese summaries unless the user requests otherwise.
- Prefer compact, structured tables over long prose for large batches.
