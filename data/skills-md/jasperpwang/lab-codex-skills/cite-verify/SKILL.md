---
name: cite-verify
description: Verify academic citations, bibliography metadata, DOI/arXiv/OpenAlex/Semantic Scholar consistency, claim-reference alignment, retraction risk, and whether cited sources actually support manuscript claims. Use for Cite Verify, citation audit, reference checking, DOI validation, claim support, broken citations, or 引用核验.
---

# Cite Verify

Core job: verify support, not merely find more references.

Checklist:
1. Parse claims and cited references.
2. For each reference, verify title, authors, year, venue, DOI/arXiv/URL, and publication status using primary or reliable metadata sources.
3. Check whether the cited source actually supports the claim. Label each as `supports`, `partial`, `misaligned`, `not found`, or `needs human read`.
4. Flag retractions, preprint-vs-published drift, wrong year/venue, duplicate references, and fabricated metadata.
5. Return a table plus specific replacement or repair actions.

Do not invent DOI values or infer citation support from a title alone. When uncertain, say what still needs manual reading.

