---
name: gong
description: Search and retrieve Gong call transcripts via Gong's public REST API. Use when the user wants to find call context, pull quotes from customer conversations, summarize recent calls for an account, search transcripts for mentions of a feature/topic/competitor, semantic/natural-language search across calls, resolve what was discussed with specific participants, or download a call recording. Covers product use cases (feature requests, pain points, customer feedback on a feature area, input for PRDs/roadmap), sales/CS use cases (account prep, renewal context, deal reviews, competitive objections, discovery notes), and GTM/marketing use cases (voice-of-customer quotes, messaging research, case study sourcing, positioning against competitors, category language). Triggers include "find calls where...", "what did [customer] say about...", "summarize last week's calls with...", "pull Gong transcripts for...", "search Gong for...", "calls where customers expressed...", "download the video of...", "what are customers saying about [feature]...", "pull customer feedback on...", "find pain points around...", "feature requests for...", "research for a PRD on...", "voice-of-customer quotes about...", "customer language around...", "objections we're hearing about...", "how are prospects talking about [competitor]...", "renewal context for...", "prep me for the [account] call...".
allowed-tools: Bash(python3:*), Bash(~/.claude/skills/gong/scripts/*), Read
---

# Gong transcript search

<img src="../../assets/gong-logo.png" width="220" alt="Gong">

Turn [Gong](https://www.gong.io/) call transcripts into research your agent can act on. Local SQLite + FTS5 cache plus optional on-device semantic search means fast, rate-limit-free queries across every call your tenant has recorded.

## What you can do with it

- **Product research** — Pull every customer conversation about a feature area and have your agent synthesize a PRD input, pain-point summary, or roadmap brief grounded in real quotes.
- **Sales / CS prep** — Brief yourself before a renewal, surface the last 90 days of context on an account, catalog objections, review what was committed on a deal.
- **GTM / Marketing** — Mine voice-of-customer language for messaging, source case study quotes, track how prospects describe competitors, spot category language shifts.
- **Ad-hoc** — Attributed quotes for a deck, competitor-mention digests, or pulling a call recording to share outside Gong.

## How it works

| Capability | Script | Notes |
|---|---|---|
| Metadata search (account, participant, tracker, date) + FTS5 keyword | `search.py` | Fastest; use first for exact terms or known names |
| Regex + context-window search | `grep_transcripts.py` | Use when you need surrounding sentences or a regex |
| Semantic / intent search | `semantic_search.py` | Pass a natural-language query — "customers worried about renewal pricing" |
| Widest net (union of metadata + semantic) | `hybrid_search.py` | Every hit tagged with `matched_by: [metadata, semantic]` |
| Full transcripts with speaker attribution | `transcript.py` | Cached, fast; pipes from any search |
| Attributed quotes filtered by speaker affiliation | `quote_transcripts.py` | `--affiliation external` skips internal speakers |
| MP4 recording download | `download_media.py` | Short-lived pre-signed URLs from Gong |
| Incremental sync of calls, transcripts, users, trackers | `sync.py` | Rate-limited to 3/sec, auto-paginates |
| One-shot freshness refresh (sync + export + embed) | `refresh.py` | No-op if cache < 6h stale |

## Install

See [INSTALL.md](INSTALL.md) for the full walkthrough — it covers getting API credentials from your Gong admin, installing qmd for semantic search, and the initial sync. Once installed, your agent drives first-time setup conversationally the first time you ask it a Gong question.

---

# Agent instructions

*The section below is aimed at the agent — humans reading this can skip it.*

Authenticated access to Gong's REST API via local scripts. Credentials live in `~/.config/gong/credentials` (chmod 600). All query scripts read from a local SQLite cache at `~/.cache/gong/cache.db` — `sync.py` is the only one that calls the API for call/transcript data.

## First-time setup (you drive this, not the user)

Before running any script, check whether the skill is set up:

1. Does `~/.config/gong/credentials` exist? If not, the user has never set this up.
2. Does `sync.py --status` show `"calls": 0`? If so, the cache is empty.

**If either is true, walk the user through setup conversationally.** Read [INSTALL.md](INSTALL.md) and follow it yourself — don't paste the whole file at them or tell them to go read it. Execute each step in turn, explaining what's happening and asking for input only when you genuinely need it from them.

Concretely:

- **Credentials** — Never write the user's Access Key Secret yourself. Instead, tell them to run this in their own terminal:
  ```
  ~/.claude/skills/gong/scripts/setup_credentials.py
  ```
  It prompts for the secret via `getpass` (no echo, no shell history, no model context). Wait for them to confirm. If they don't have credentials yet, hand them the verbatim request block from INSTALL.md step 2 to send their IT / RevOps team, then pause.
- **qmd (optional)** — Check if `qmd` is on PATH. If not, ask whether they want semantic search (recommended). If yes, run the install yourself (`npm install -g @tobilu/qmd`); if no, note that `semantic_search.py` and the semantic half of `hybrid_search.py` will be unavailable.
- **Initial sync** — Run `refresh.py --force` yourself. That wraps `sync.py --full` (last 365 days) → `export_markdown.py` → `qmd collection add` + `qmd embed` + model warmup in one step. Warn the user it can take 5–30 minutes depending on call volume and that qmd will download ~2 GB of GGUF models on this first run.
  - If the user wants a narrower initial window, use `refresh.py --force --from YYYY-MM-DD`. **Never** call `sync.py --from` / `export_markdown.py` / `qmd collection add` / `qmd embed` directly during setup — they each succeed in isolation while leaving the pipeline half-wired (e.g. qmd collection wrong, embeddings empty, query model not downloaded), and the first real semantic query stalls mid-flight on the model download. `refresh.py --force` (optionally with `--from`) is the **only** setup command.
  - If `refresh.py --force --from YYYY-MM-DD` appears to fail with "Gong cache is empty", you're running an old copy of the skill — update it. The current version auto-routes to `sync.py --full --from` when the cache is empty.
- **Verify** — Run `sync.py --status` and report the numbers.

Only after setup is complete should you proceed with the user's original question.

## Freshness: always run this first

Before running any query script in response to a user request:

```bash
~/.claude/skills/gong/scripts/refresh.py
```

No-op if the cache was refreshed in the last 6 hours. Otherwise it runs `sync.py` → `export_markdown.py` → `qmd embed` to bring both the SQLite cache and the semantic index current. Output goes to stderr. Skip only if (a) the user is doing follow-up work in the same session and you've already refreshed, or (b) they explicitly say to work with cached data.

## Choosing the right search

| Need | Use |
|---|---|
| Exact term, known name, fast | `search.py --keyword` (FTS5 over transcripts) |
| Regex, case sensitivity, sentence context | `grep_transcripts.py` |
| Fuzzy intent / synonyms | `semantic_search.py` with a **natural-language query** |
| Metadata only (account, participant, tracker, date) | `search.py` filters |
| Cast the widest net | `hybrid_search.py` — union of metadata + semantic |

**Semantic query tip:** pass a natural-language sentence, not a keyword bag. `"customers asking for account-level risk scoring"` beats `"account intel account intelligence account data enrichment"` — the reranker is tuned for sentence-level queries and keyword soup confuses it.

## Defaults

- **Query date window: 90 days** across every script. Override with `--from YYYY-MM-DD --to YYYY-MM-DD`, or `--all-time` on scripts that support it (`find_account.py`, `list_trackers.py`).
- **Initial sync window: 365 days** (`sync.py --full`, also what `refresh.py --force` runs). Subsequent incremental syncs just pull what's new.
- **Names resolved:** user/account IDs become human names via the cached `users` table.
- **Tenant:** set via `GONG_API_BASE_URL` in the credentials file.

## Typical workflows

### 1. Find calls matching criteria (`search.py`)

Filters combine with AND. Keyword search uses FTS5 over the full transcript.

```bash
~/.claude/skills/gong/scripts/search.py --account "Acme Corp"
~/.claude/skills/gong/scripts/search.py --keyword "pricing"
~/.claude/skills/gong/scripts/search.py --participant "jane@customer.com" --affiliation external
~/.claude/skills/gong/scripts/search.py --tracker "Pricing"
~/.claude/skills/gong/scripts/search.py --account "Acme" --keyword "renewal" --from 2026-01-01 --to 2026-04-28
~/.claude/skills/gong/scripts/search.py --account "Acme" --ids-only    # pipe to next step
```

### 2. Fetch transcripts (`transcript.py`)

```bash
~/.claude/skills/gong/scripts/transcript.py --call-id 1234567890
~/.claude/skills/gong/scripts/transcript.py --call-ids 1234,5678 --format json
~/.claude/skills/gong/scripts/search.py --keyword "pricing" --ids-only | \
  ~/.claude/skills/gong/scripts/transcript.py --call-ids -
```

If `has_transcript=0` for a call, re-run `sync.py` — Gong may not have had it ready on the previous pull.

### 3. Pull attributed quotes (`quote_transcripts.py`) — *preferred over ad-hoc JSON parsing*

When the user asks "what are customers saying about X?", don't hand-roll Python to filter transcript JSON. Use `quote_transcripts.py`:

**Canonical pattern: stdin pipe from search → quote.** Do not build a CSV in a shell variable; pipe IDs through stdin. This is the shortest correct form and handles any number of IDs.

```bash
# External-speaker exchanges mentioning "account intel" — by default pattern
# matches anywhere in the context window, so customer answers come through
# even when the rep is the one who said the keyword.
~/.claude/skills/gong/scripts/search.py --keyword "account intel" --ids-only --limit 200 | \
  ~/.claude/skills/gong/scripts/quote_transcripts.py --call-ids - \
  --pattern "account intel" --affiliation external

# Or pass IDs directly if you already have them:
~/.claude/skills/gong/scripts/quote_transcripts.py --call-ids 123,456,789 \
  --pattern "account intel" --affiliation external

# All external quotes (no pattern filter), JSON for further processing
~/.claude/skills/gong/scripts/quote_transcripts.py --call-ids 123 \
  --affiliation external --format json

# Pipe from search → quotes
~/.claude/skills/gong/scripts/search.py --account "Acme" --keyword "pricing" --ids-only | \
  ~/.claude/skills/gong/scripts/quote_transcripts.py --call-ids - \
  --pattern "pricing|cost|budget" --regex --affiliation external

# Only match when the highlighted speaker themselves said the keyword
~/.claude/skills/gong/scripts/quote_transcripts.py --call-ids 123 \
  --pattern "too expensive" --affiliation external --pattern-scope highlighted
```

**Why the default is window-scope matching:** customers often respond to what your team just said without repeating the keyword ("rep: how's our pricing?" → "customer: way too high"). With `--pattern-scope window` (default) and `--context 2` (default), that exchange surfaces with both sides attributed. Use `--pattern-scope highlighted` when you only want quotes where the customer themselves uses the term.

Output includes speaker name, affiliation (internal/external), domain, timestamp, call title, account, and Gong URL. The matched line is prefixed with `>`; surrounding context lines keep their own speaker attribution. Use this for PRD research, voice-of-customer decks, or any "quotes from real customers" output.

### 4. Semantic search (`semantic_search.py`)

Natural-language / intent queries where FTS5 keyword matching misses synonyms. Pass a sentence, not a keyword list.

```bash
~/.claude/skills/gong/scripts/semantic_search.py "customers worried about renewal pricing"
~/.claude/skills/gong/scripts/semantic_search.py "discovery calls we lost to a competitor" --ids-only | \
  ~/.claude/skills/gong/scripts/transcript.py --call-ids -
```

### 5. Hybrid (widest net) (`hybrid_search.py`)

Union of metadata + semantic. Use when you want to combine "all calls with Acme" *and* "anything about pricing concerns" without losing either signal. Pass `--query` as a natural-language sentence.

```bash
~/.claude/skills/gong/scripts/hybrid_search.py \
  --query "customers asking for account-level risk scoring" \
  --account "Acme" --limit 30
```

Each hit is tagged `matched_by: [metadata]`, `[semantic]`, or both — dual-matched hits sort first.

**Query shape matters.** The reranker is tuned for natural-language sentences. Keyword bags return few or zero hits:

- ✗ BAD: `--query "problems pain points integration setup configuration bugs"`
- ✓ GOOD: `--query "customers hitting problems setting up the integration"`

If `hybrid_search.py` returns 0 results, read its stderr hints — they'll tell you which half (metadata or semantic) came back empty and how to fix it.

### 6. Regex / context-window search (`grep_transcripts.py`)

Use when you need regex, case-sensitivity, or surrounding-sentence context. Prefer `search.py --keyword` for simple term search (FTS5 is faster).

```bash
~/.claude/skills/gong/scripts/search.py --account "Acme" --ids-only | \
  ~/.claude/skills/gong/scripts/grep_transcripts.py "SMS\s+toll" --regex --call-ids -

~/.claude/skills/gong/scripts/grep_transcripts.py "renewal" --call-ids 123,456 --context 4
```

### 7. Discover accounts, users, trackers

```bash
~/.claude/skills/gong/scripts/find_account.py "acme"                    # 90-day window
~/.claude/skills/gong/scripts/find_account.py "acme" --all-time
~/.claude/skills/gong/scripts/find_user.py "jane"
~/.claude/skills/gong/scripts/list_trackers.py --min-hits 3
```

### 8. Download a call recording (`download_media.py`)

Gets a short-lived pre-signed URL and streams the MP4 to disk. Useful for posting a call externally to people without Gong access.

```bash
~/.claude/skills/gong/scripts/download_media.py --call-id 1234567890
~/.claude/skills/gong/scripts/download_media.py --call-id 1234567890 --output ~/Downloads/acme-demo.mp4
~/.claude/skills/gong/scripts/download_media.py --call-ids 123,456,789 --output-dir ~/Downloads/gong/
```

Pre-signed URLs expire quickly — don't save them, just stream.

## Searching tips

- **`search.py --keyword` searches transcripts** (via FTS5), not just metadata. Use it first; fall back to `grep_transcripts.py` for regex or context.
- **Account filter** matches Gong's CRM-linked account name. Resolve fuzzy names with `find_account.py` first.
- **Participant filter** takes email. For a name → email, use `find_user.py`.
- **Trackers** are high-leverage — Gong's classifier already fired on the topic for you. Discover with `list_trackers.py`, then filter with `--tracker "Name"`.
- **`--affiliation`** restricts participant matching to `internal` or `external`. Affiliation is inferred from email domain when Gong's own label is missing ("Unknown") — any domain Gong has ever labeled Internal, plus every domain in the `users` table, counts as internal; other domains count as external. Speakers with no email (transcribed voice-only invitees) stay `unknown` and are excluded by `--affiliation` filters — use `--affiliation external` on important synthesis work so unattributed speakers don't slip into customer quotes.
- **Empty hybrid but non-empty semantic?** You probably passed keyword soup to `--query`. Rephrase as a natural-language sentence.

## Output philosophy

When the user asks "what did Acme say about pricing?":

1. `search.py --account Acme --keyword pricing --ids-only --limit 200`
2. `quote_transcripts.py --call-ids - --pattern pricing --affiliation external --context 2`
3. Return a short synthesis with 2–4 attributed quotes, dates, and Gong links
4. Offer to go deeper (broader window, different account, etc.)

**Synthesis scope:** the default `--limit 50` exists to keep ad-hoc queries fast. For "what are customers saying about X" synthesis work, always bump to 200+ so you're not silently summarizing a cap. `search.py` prints a `NOTE:` to stderr when the limit was hit; if you see it, you're working off a truncated set — re-run with a higher limit before synthesizing.

**Always pair `--keyword` with `--pattern`.** If you searched with `--keyword foo`, `quote_transcripts.py` must get `--pattern foo` (or a regex alternation covering foo) so the output is actually filtered to the matched moments. Dropping `--pattern` dumps *every* external line across the matched calls — at that point you'll feel pressure to hand-roll a Python regex filter over the JSON to narrow it down, which strips the speaker-attribution guarantees the tool provides. **Never do that.** If your theme is broader than one keyword (e.g. "integration problems"), build a regex alternation and pass it via `--pattern "fail|broken|stuck|issue|bug|doesn't work" --regex` instead.

**When the user asks a theme question ("what problems are customers hitting with X?")**, the regex-alternation `--pattern` goes in the quote step, not the search step — search with the product term (`--keyword X`) to find the conversations, then pattern-filter within those conversations for the theme words.

Save large transcripts to a temp file and reference the path rather than pasting them.

**Attribution discipline.** Every quote you print must be traceable to a specific speaker on a specific call. Five gotchas that have burned past runs:

1. **Speaker ≠ mention.** If a rep on a Acme Co. call says "we saw the same issue at Widgets Inc.," that's not an Widgets Inc. quote — it's a a rep mentioning Widgets Inc. inside a Acme Co. call. Attribute every quote to (a) the speaker the quote output names, and (b) the account of the call the quote came from. Never attribute a quote to a customer whose name appears inside someone else's line.
2. **Affiliation is your filter against this.** Always pass `--affiliation external` when the user asks what customers are saying. Speakers resolved to `internal` or `unknown` shouldn't appear as customer voice.
3. **Verify the URL.** Before you paste a Gong URL for a quote, confirm the call ID in the URL matches the `call_id` in the tool output for that specific quote. If you catch yourself typing a URL from memory, stop — re-query.
4. **No hand-rolled regex filters over quote JSON.** If the quote output has too much noise, re-run `quote_transcripts.py` with a tighter `--pattern` (or `--pattern-scope highlighted`). Filtering the JSON yourself with Python regex will desync the `>`-matched line from its speaker block and you *will* misattribute.
5. **Always label the speaker's affiliation when you print them.** Every time you render a speaker name to the user — in synthesis, tables, block quotes, bullet points, or inline — tag it `(external)`, `(internal)`, or `(unknown)`. The affiliation comes directly from the `affiliation` field in `quote_transcripts.py` JSON output; use it verbatim. Format: `Jane Doe (external, acme.com), Acme Co. — 2026-04-24`. Never print a speaker name bare — the label is what keeps the reader from assuming every quote is a customer.

If you're about to synthesize across many calls, prefer `quote_transcripts.py --format flat` piped into a temp file (one TSV line per quote, `role\tspeaker\taffiliation\taccount\tdate\turl\ttimestamp\ttext`), or `--format json` if you need the nested shape. Do not paraphrase quotes — copy them verbatim from the tool output.

## References

- [references/filters.md](references/filters.md) — Full filter shape for `/v2/calls/extensive`
- [references/api-shape.md](references/api-shape.md) — Request/response shapes for endpoints used by `sync.py` and `download_media.py`
