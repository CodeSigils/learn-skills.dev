---
name: market-data
description: |
  Multi-source real-time market data via the Dataline API. Covers:
  crypto spot & perpetual prices (BTC, ETH, SOL, …), funding rates, and
  exchange announcements plus prediction market odds & events (Polymarket, Kalshi).
  Trigger on: "price of", "how much is", "funding rate", "perp rate",
  "exchange announcement", "listing announcement", "delisting", "maintenance notice",
  "market odds", "prediction market", "what are the odds", "BTC/ETH price",
  "election odds", "polymarket", "kalshi".
  Driven by a bundled OpenAPI spec — endpoints stay in sync with the shipped skill.
compatibility:
  runtime: python>=3.8
  required_commands:
    - uv
  dependencies:
    - httpx
---

# market-data — Dataline Market Data Skill

## Quick Start

> 👤 **For human users**: see [references/user-guide.md](references/user-guide.md) — what to say to your agent to use this skill.

If the intent is already clear (see Intent Mapping Guide below), call `query.py` directly —
no need to run Steps 1–2:

> ⚠️ **Requires `uv`** — install once: `curl -LsSf https://astral.sh/uv/install.sh | sh`
> Scripts use PEP 723 inline metadata. No `pip install` needed after uv is installed.

```bash
# SKILLDIR: the absolute path to this skill directory.
# Get it from skill_view() metadata field `skill_dir`, or set manually:
#   SKILLDIR=~/.agents/skills/market-data
SKILLDIR=<path-from-skill_dir-metadata>
uv run "$SKILLDIR/scripts/query.py" --intent get_spot_price --base-currency BTC
uv run "$SKILLDIR/scripts/query.py" --intent get_funding_rate --base-currency ETH
uv run "$SKILLDIR/scripts/query.py" --intent get_exchange_announcement_list --query "listing"
uv run "$SKILLDIR/scripts/query.py" --intent search_odds_events --query "US election"
```

---

## Setup

Required environment variables:

```
DATALINE_API_KEY=***
DATALINE_SECRET_KEY=***
DATALINE_BASE_URL=https://www.dataline.xyz   # default
```

Dependency: [uv](https://docs.astral.sh/uv/) — scripts declare their own deps via PEP 723
inline metadata. No `pip install` needed.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Full Pipeline (5 Steps)

Use the full pipeline when the request is ambiguous or you need to discover available
parameters before calling.

### Step 1: INTENT — Discover available intents

```bash
uv run "$SKILLDIR/scripts/fetch_intents.py"
```

Returns a JSON object with an `intents` array. Each intent has `id`, `description`, and
`endpoint`. Select the intent that best matches the user's request.

### Step 2: ROUTE — Resolve endpoint + params schema

```bash
uv run "$SKILLDIR/scripts/resolve_intent.py" --intent <intent_id>
```

Returns the HTTP method, path, and required/optional parameters with types and descriptions.

### Step 3: PARAMS — Fill parameters

Map the user's natural language to parameter values using the schema from Step 2.
Examples: "Bitcoin" → `base_currency=BTC`, "perp" → `kind=perp`.

### Step 4: FETCH — Execute the query

```bash
uv run "$SKILLDIR/scripts/query.py" \
  --intent <intent_id> \
  [--base-currency X] [--quote-currency Y] [--kind Z] \
  [--source S] [--category C] [--source-category-id ID] \
  [--query Q] [--announcement-id ID] [--external-id ID] \
  [--provider P] [--event-id E] [--platform F] \
  --base-url $DATALINE_BASE_URL
```

HMAC authentication is handled automatically from `DATALINE_API_KEY` / `DATALINE_SECRET_KEY`.

### Step 5: OUTPUT — Present results

`query.py` produces a pipeline trace then the JSON payload:

```
[01/05] INTENT    get_spot_price
[02/05] ROUTE     GET /api/v1/data/price?base_currency=BTC&kind=spot
[03/05] AUTH      HMAC-SHA256 signed
[04/05] FETCH     200 OK · 84ms · sources: okx, binance, hyperliquid, coinbase
[05/05] OUTPUT    ↓

{ "base": "BTC", "average_price": 80759.17, "sources": [...] }
```

Present results naturally: prices as currency, funding rates as percentage,
announcements as concise title/time/source summaries with links, and odds as probability list.

---

## Script Reference

| Script | Purpose | Key args |
|--------|---------|----------|
| `fetch_intents.py` | List available intents (loaded from bundled `openapi.json`) | (none) |
| `resolve_intent.py` | Get endpoint + param schema for an intent | `--intent` |
| `query.py` | Execute authenticated API call with pipeline trace | `--intent`, `--base-currency`, `--quote-currency`, `--kind`, `--source`, `--category`, `--source-category-id`, `--query`, `--start-time`, `--end-time`, `--status`, `--include-content`, `--announcement-id`, `--external-id`, `--provider`, `--event-id`, `--platform`, `--page`, `--limit`, `--kalshi-market-id`, `--polymarket-market-id`, `--base-url` |

All scripts support `--help` for full usage.

---

## Intent Mapping Guide

| User says | Intent | Key params |
|-----------|--------|------------|
| "BTC price", "price of Bitcoin" | `get_spot_price` | `base_currency=BTC` |
| "ETH perp price" | `get_perp_price` | `base_currency=ETH`, `kind=perp` |
| "BTC funding rate" | `get_funding_rate` | `base_currency=BTC` |
| "what exchange announcement categories exist" | `get_exchange_announcement_categories` | (none) |
| "latest Binance listing announcements", "search exchange announcements for listing" | `get_exchange_announcement_list` | `source=binance`, `query=listing` |
| "detail for announcement 123" | `get_exchange_announcement_detail` | `announcement_id=123` |
| "what prediction categories exist" | `get_odds_categories` | (none) |
| "election events", "crypto odds" | `get_odds_event_list` | `category=politics` |
| "search odds on X" | `search_odds_events` | `query=X` |
| "detail of event Y" | `get_odds_event_detail` | `provider=polymarket`, `event_id=Y` |
| "orderbook for market X" | `get_odds_event_orderbook` | `kalshi_market_id=X` or `polymarket_market_id=X` |
