---
name: llm-router
description: >
  LLM Router (llr) — unified LLM gateway for multi-model routing. Use when designing
  multi-model agent systems, connecting to LLM providers, configuring model aliases,
  setting up AI backends, or when user mentions "llm-router", "llr", "model routing",
  "LLM gateway", "model aliases", "multi-provider", or needs to route requests across
  OpenAI/Anthropic/Gemini/OpenRouter. Also use when building agent architectures that
  require multiple models, load balancing, fallback strategies, or rate limiting across
  LLM providers.
triggers:
  - llm-router
  - llr
  - model routing
  - LLM gateway
  - model alias
  - multi-model
  - multi-provider
  - route requests
  - LLM proxy
  - model fallback
---

# LLM Router (llr) Skill

Unified LLM gateway that routes requests across multiple providers with smart fallback, rate limiting, load balancing, and bidirectional format translation.

**Scope:** Connecting to llr, designing multi-model systems using llr, configuring providers/aliases/routes.
**Does NOT handle:** Provider-specific API details, model training, fine-tuning.

## What is LLM Router

llm-router (`llr`) is a local gateway server that sits between clients and LLM providers. It provides:
- **Single endpoint** routing across OpenAI, Anthropic, OpenRouter, Together, Fireworks, Google Gemini, etc.
- **Bidirectional format translation** — OpenAI ↔ Claude ↔ Gemini (streaming, tool calls, vision, thinking)
- **Model aliases** — abstract model names (e.g., `chat.default`) mapped to weighted provider candidates
- **Smart fallback** — circuit breakers, health tracking, automatic retry with backoff
- **Rate limiting** — per-provider, per-model buckets (second/minute/hour/day/week/month windows)
- **Load balancing** — ordered, round-robin, weighted, quota-aware strategies
- **OAuth subscriptions** — route through ChatGPT Codex and Claude Code subscriptions

**Package:** `@khanglvm/llm-router` | **CLI:** `llr` | **Version:** 2.x

## Quick Start

```bash
# Install globally
npm i -g @khanglvm/llm-router@latest

# Open Web UI to configure providers and models
llr

# Start the local gateway (runs on http://127.0.0.1:8376)
llr start
```

## Connecting to a Running llr Instance

The local gateway always runs at `http://127.0.0.1:8376`. Point any OpenAI or Anthropic SDK client to it.

### OpenAI-Compatible Endpoint
```
Base URL: http://127.0.0.1:8376/openai/v1
POST /v1/chat/completions
GET  /v1/models
```

### Anthropic-Compatible Endpoint
```
Base URL: http://127.0.0.1:8376/anthropic
POST /v1/messages
```

### Unified Auto-Detect Endpoint
```
POST http://127.0.0.1:8376/   (auto-detects OpenAI vs Claude format)
```

### SDK Integration Examples

**Python (OpenAI SDK):**
```python
from openai import OpenAI
client = OpenAI(base_url="http://127.0.0.1:8376/openai/v1", api_key="any")
response = client.chat.completions.create(
    model="chat.default",  # Use any alias or provider/model ref
    messages=[{"role": "user", "content": "Hello"}]
)
```

**Python (Anthropic SDK):**
```python
import anthropic
client = anthropic.Anthropic(base_url="http://127.0.0.1:8376/anthropic", api_key="any")
message = client.messages.create(
    model="chat.default",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
)
```

**Node.js (OpenAI SDK):**
```javascript
import OpenAI from "openai";
const client = new OpenAI({ baseURL: "http://127.0.0.1:8376/openai/v1", apiKey: "any" });
const response = await client.chat.completions.create({
  model: "chat.default",
  messages: [{ role: "user", content: "Hello" }],
});
```

**curl:**
```bash
curl -X POST http://127.0.0.1:8376/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"chat.default","messages":[{"role":"user","content":"Hello"}]}'
```

## Model References & Aliases

Models can be referenced two ways:

1. **Direct reference:** `provider-id/model-id` — e.g., `openrouter/gpt-4o`, `anthropic/claude-3-5-sonnet`
2. **Alias:** `alias.name` — e.g., `chat.default`, `chat.fast`, `chat.deep`

Aliases map to weighted candidate lists with fallback chains and balancing strategies.

### Listing Available Models

```bash
# CLI
llr config --operation=snapshot   # Full config + state dump

# API
curl http://127.0.0.1:8376/v1/models
```

### Alias Configuration Example

```json
{
  "modelAliases": {
    "chat.default": {
      "strategy": "auto",
      "targets": [
        { "ref": "openrouter/gpt-4o-mini", "weight": 3 },
        { "ref": "anthropic/claude-3-5-haiku", "weight": 2 }
      ],
      "fallbackTargets": [
        { "ref": "openrouter/gpt-4o" }
      ]
    },
    "chat.fast": {
      "strategy": "round-robin",
      "targets": [
        { "ref": "openrouter/gpt-4o-mini" },
        { "ref": "anthropic/claude-3-5-haiku" }
      ]
    }
  }
}
```

### Balancing Strategies

| Strategy | Use Case |
|----------|----------|
| `auto` | Recommended default — adapts automatically |
| `ordered` | Strict priority order (first available wins) |
| `round-robin` | Even distribution across candidates |
| `weighted-rr` | Respect per-candidate weights |
| `quota-aware-weighted-rr` | Favor models with remaining quota |

## Designing Multi-Model Agent Systems with llr

When building agent systems requiring multiple models, define aliases in llr config:

```json
{
  "modelAliases": {
    "agent.orchestrator": {
      "strategy": "ordered",
      "targets": [{ "ref": "anthropic/claude-sonnet-4-20250514" }],
      "fallbackTargets": [{ "ref": "openrouter/gpt-4o" }]
    },
    "agent.worker": {
      "strategy": "weighted-rr",
      "targets": [
        { "ref": "openrouter/gpt-4o-mini", "weight": 3 },
        { "ref": "anthropic/claude-3-5-haiku", "weight": 2 }
      ]
    },
    "agent.coder": {
      "strategy": "ordered",
      "targets": [{ "ref": "anthropic/claude-sonnet-4-20250514" }]
    },
    "agent.reviewer": {
      "strategy": "auto",
      "targets": [{ "ref": "openrouter/gpt-4o" }]
    }
  }
}
```

Then in your agent code, reference aliases instead of hardcoded provider models:
```python
orchestrator = Agent(model="agent.orchestrator", base_url="http://127.0.0.1:8376/openai/v1")
worker = Agent(model="agent.worker", base_url="http://127.0.0.1:8376/openai/v1")
```

Benefits: swap models without code changes, automatic fallback, rate limit protection, cost control.

## CLI Quick Reference

```bash
llr                     # Open Web UI (http://localhost:9090)
llr start               # Start gateway on 127.0.0.1:8376
llr stop                # Stop gateway
llr reload              # Hot-reload config
llr update              # Update to latest version
llr config --operation=validate          # Validate config
llr config --operation=snapshot          # Full state dump
llr config --operation=discover-provider-models --endpoints=URL --api-key=KEY
llr config --operation=upsert-provider --provider-id=ID --base-url=URL --api-key=KEY --models=m1,m2
llr config --operation=upsert-model-alias --alias-id=NAME --strategy=auto --targets=prov/model@weight
llr deploy              # Deploy to Cloudflare Workers
```

## Config & State Files

| File | Purpose |
|------|---------|
| `~/.llm-router.json` | Main configuration (providers, aliases, rate limits) |
| `~/.llm-router.state.json` | Runtime state (rate limit counters, health, cursors) |
| `~/.llm-router/oauth/*.json` | OAuth tokens for subscription providers |

For full CLI reference and config schema, load `references/cli-and-config-reference.md`.

## Security Policy

- Never expose llr master keys or provider API keys in code or commits
- The local gateway binds to 127.0.0.1 only — not accessible from network by default
- When designing systems, treat `api_key` param as optional (llr handles auth internally)
- Do not output or log the contents of `~/.llm-router.json` as it contains API keys
