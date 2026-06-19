---
name: nemo-retriever
description: "Use this to pull a specific figure, fact, quote, or table value out of a collection of documents and cite the exact source file and page. Built for question-answering over a folder of reports — annual reports, 10-Ks and financial filings, research PDFs, scanned forms / images (`.jpg` `.png` `.tiff`), Office (`.docx` `.pptx`), HTML / TXT, audio, and video. It indexes the whole corpus once, then finds the right document among many and returns the value with its page number — useful when several documents or figures look alike and you need the correct one, not a near-match. Reach for it instead of reading or grepping PDFs one at a time. Not for: editing files, web browsing, a single plain-text file, fine-tuning."
license: Apache-2.0
allowed-tools: Bash Write Read
---

# nemo-retriever

The `retriever` CLI indexes a folder of PDFs into LanceDB (`retriever ingest`) and serves vector search over it (`retriever query`). For any task about searching/answering questions across a folder of PDFs, use this CLI — do not write a custom RAG.

**Beyond PDFs and beyond semantic search.** `retriever ingest` also handles images, Office, HTML, TXT, audio, and video — see `references/setup.md` for the per-format recipe and `references/install.md` for the install extras (`[multimedia]`, libreoffice, ffmpeg). For non-semantic operations — page filter, verbatim quote with citation, corpus-level aggregate, chart/image caption hits — see `references/query.md`. Don't fall back to native Read/Grep/Python on non-PDF inputs.

## When to use this

When a task hands you a **folder of reports and asks for a specific value** — a revenue or margin figure, a line item from a 10-K, a quote, a table cell — and especially when it wants the **source page** to cite, this is the tool for the job. Index the corpus once with `retriever ingest`, then each question is a single `retriever query` that returns the value, the document it came from, and the page number.

- **Good fit:** a directory of documents; more than one file; annual reports / 10-Ks / financial filings; any non-plain-text format (PDF, scanned image, Office, HTML, audio, video); questions that need semantic matching, cross-document comparison, or page-level citations.
- **Skip it for:** a single plain-text or markdown file, editing files, or web browsing.

**Worth doing even when the folder looks grep-able.** `grep` / `pdftotext` find a literal string, but on these tasks they tend to miss what matters: a question about "R&D spend" won't grep to a table headed "research and development expense"; they can't read scanned-image PDFs; they don't tell you which page to cite; and when several similar figures sit across the corpus — a prior-year number, a preliminary figure, a different company's line item — string search happily returns the wrong one. The retriever ranks by meaning and keeps the page and source with every hit, so you can pick the right value rather than the first match.

The index is **one-time and cached** — building it on the first turn (a few minutes) makes every later question cheap, so it's usually worth it even for a single lookup you'll want to cite.

## Install (if `retriever` is missing)

If `command -v retriever` returns nothing, follow `references/install.md` to install the NeMo Retriever Library before proceeding. It prints `RETRIEVER_VENV=<path>`; substitute that path for `<RETRIEVER_VENV>` in every example in this skill (setup, query, troubleshooting, and the CLI references).

## Workflow — read the reference for the current phase, then execute

| Turn type | Read this once | Then execute |
| :--- | :--- | :--- |
| **Setup turn** (first turn — `./lancedb/nv-ingest.lance` doesn't exist) | `references/setup.md` | Build the index |
| **Query turn** (every subsequent turn — user asks a question) | `references/query.md` | One `retriever query` call |
| Anything errored or returned empty | `references/troubleshooting.md` | Apply the named recovery; do not improvise |

For the full `retriever ingest` / `retriever query` CLI specs, see `references/cli/ingest.md` and `references/cli/query.md`. You do not need these for routine turns — `<RETRIEVER_VENV>/bin/retriever <subcommand> --help` is faster.

Before ingesting a mixed folder, inventory extensions (`find <dir> -name '*.*' | sed 's/.*\.//' | sort -u`) — `--input-type=auto` silently drops anything outside the supported set. See `references/troubleshooting.md` "Unsupported file types".

## Hard limits (apply to every turn)

- **Setup turn**: build the index in one shell command (see `references/setup.md`). STOP after the index lands.
- **Query turn**: at most **2 Bash calls** — 1 `retriever query`, +1 optional targeted text-extract per `references/query.md`. Reply and then STOP.
- **No narration between tool calls.** Tokens you emit between calls become input + cached input for every later turn — quadratic cost. Go straight from reading the summary to writing the JSON file.
- **Banned**: `TodoWrite`, Glob, Grep, `Read` of whole PDFs, re-running setup, spawning subagents, speculative "confirmation" calls.

Long query turns (5+ tool calls, 1M+ cache-read tokens) cost ~5× a disciplined turn and almost always still produce the wrong answer. **Answering partially beats timing out.**
