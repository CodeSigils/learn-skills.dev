---
name: gemini
description: "Build, migrate, and optimize Gemini API and Gemini CLI workflows. TRIGGER when: user mentions Gemini API, Google GenAI SDK, `google-genai`, `@google/genai`, Gemini CLI, `GEMINI.md`, Gemini function calling, structured outputs, thinking, thought signatures, context caching, Live API, Google AI Studio, Vertex AI Gemini usage, or migrating from legacy `google-generativeai` / `@google/generative-ai`. SKIP: non-Google provider work with no Gemini angle, ordinary coding with no Gemini integration, or generic agent customization that belongs to Windsurf/Copilot/Codex instead."
---

# Building with Gemini

Use this skill for two main categories:

1. **Gemini API / SDK application code**
2. **Gemini CLI customization and workflow setup**

Treat them separately unless the user explicitly wants both.

## Hard Rules

- For new Gemini API work, use the **Google GenAI SDK** unless the user explicitly asks for raw REST.
- Do not start new code on legacy SDKs like:
  - `google-generativeai`
  - `@google/generative-ai`
- If the repo already uses a legacy Gemini SDK and the user asked for a patch, work with the existing code first, then offer a migration path.
- Do not guess exact model names, preview status, or feature support when those facts matter. Verify from official Gemini docs.
- Prefer **stable, non-preview models** unless the feature is preview-only or the user explicitly asked for preview.

## First Classify the Request

### 1. Gemini API Integration

Use this when the user wants:

- app code using Gemini
- tool / function calling
- structured outputs
- multimodal requests
- file upload
- chats
- embeddings
- caching
- thinking controls
- Live API / realtime behavior

### 2. Gemini CLI

Use this when the user wants:

- terminal agent setup
- `GEMINI.md`
- custom context
- non-interactive CLI execution
- JSON / stream output modes
- CLI-based automation
- MCP in Gemini CLI

### 3. Migration

Use this when the user wants to migrate from:

- `google-generativeai` -> `google-genai`
- `@google/generative-ai` -> `@google/genai`
- older model assumptions -> current Gemini 2.5 / 3 patterns

## Default Stack

Unless the user asks otherwise:

- Python: `google-genai`
- JavaScript / TypeScript: `@google/genai`
- Go: `google.golang.org/genai`
- Java: official Google GenAI SDK
- Unsupported language or shell-first use case: REST examples

Prefer the **central client object** style from the modern SDKs instead of older per-model object patterns.

## Language Detection

Infer the project language from repo files:

- `*.py`, `requirements.txt`, `pyproject.toml` -> Python
- `*.ts`, `*.tsx`, `package.json`, `tsconfig.json` -> TypeScript
- `*.js`, `*.jsx` with no TS -> JavaScript
- `*.go`, `go.mod` -> Go
- `*.java`, `pom.xml`, `build.gradle` -> Java

If multiple languages exist, anchor on the target file or the language named by the user.

## Model Selection Guidance

- Prefer stable non-preview Gemini models unless the task needs a preview-only feature.
- If the user asks for "best quality," verify the current model table before hardcoding a model.
- If the user asks for low-latency or cost-sensitive work, choose a flash-tier model only after confirming that the accuracy tradeoff is acceptable.
- If the user asks for exact latest model names or capabilities, verify them from official docs first.

## Thinking Guidance

Gemini uses different thinking controls depending on the model family.

### Gemini 3

- Prefer `thinkingLevel`
- use it to tune latency vs reasoning depth
- do not assume "thinking off" exists in the same way across models

### Gemini 2.5

- use `thinkingBudget` when budget-level control is required

### General Rule

- If the user wants the strongest reasoning, keep thinking enabled and choose the right model family first.
- If latency matters, lower the thinking setting rather than blindly downgrading the whole architecture.

## Thought Signatures

This matters whenever function calling and some multi-turn workflows are involved.

- Preserve thought signatures exactly when the model returns them.
- For Gemini 3, thought signatures may appear more broadly.
- For function calling, returning the signature in the right place is required for the next turn to work correctly.
- If using the official Google GenAI SDK and not manually rewriting history, the SDK handles most of this.

Do not strip signatures out of conversation history if you are replaying turns manually.

## Function Calling Guidance

Use Gemini function calling when the model needs to trigger external actions or fetch external data.

Modes include:

- `AUTO`
- `ANY`
- `NONE`

Use:

- `AUTO` for most agentic app flows
- `ANY` when every response must be a tool call
- `NONE` when temporarily disabling tool usage

Keep tool schemas narrow, explicit, and operationally useful.

## Structured Outputs Guidance

Use structured outputs when the final answer must be machine-readable.

Best practices:

- define tight JSON Schema
- use specific types and enums where possible
- keep schemas shallow unless deeper nesting is necessary
- validate the output in application code even when the format is guaranteed

Use structured outputs for:

- extraction
- classification
- downstream automation
- database writes
- strongly typed app contracts

Use function calling instead when the model needs to **act**, not just format the final answer.

## Caching Guidance

Gemini supports both implicit and explicit caching patterns.

Use caching when:

- large prefixes repeat
- the same files or long instructions are sent repeatedly
- cost and latency matter across many requests

Avoid premature caching complexity if the workload is small or one-off.

If the user needs guaranteed savings or explicit lifecycle control, use explicit caching. If they just want better hit chances on repeated prefixes, the model family's implicit caching behavior may already help.

## Files, Multimodality, and Long Context

Use Gemini when the task benefits from:

- image / video / audio / PDF inputs
- very long context
- code execution or search-grounded flows

When reusing files across requests, prefer the official file upload flow instead of re-sending raw content every time.

## Gemini CLI Guidance

Use Gemini CLI when the user wants a terminal-native agent rather than embedding Gemini inside an app.

Typical CLI features to leverage:

- `GEMINI.md` for persistent project context
- interactive repo work
- non-interactive prompts
- JSON or streaming JSON output for scripts
- MCP support

### `GEMINI.md`

Use `GEMINI.md` for durable project guidance:

- architecture notes
- coding conventions
- build/test commands
- repository quirks
- preferred workflows

Keep it concise, specific, and operationally useful. Do not turn it into a novel.

### CLI Automation

Prefer CLI non-interactive mode when the user wants:

- shell scripts
- CI tasks
- structured machine-readable output

If the output will be parsed by another program, use JSON output modes rather than scraping plain text.

## Migration Guidance

When migrating old Gemini code:

### Python

- `google-generativeai` -> `google-genai`

### JavaScript / TypeScript

- `@google/generative-ai` -> `@google/genai`

Migration usually includes:

- moving to a central client object
- updating method names
- updating file/caching service calls
- revisiting model names
- revisiting thinking controls

Do not do a superficial import rename only. Update the calling pattern properly.

## Authentication Guidance

Pick the auth route that matches the deployment:

- API key for Gemini API / Google AI Studio style usage
- Vertex AI configuration for enterprise Google Cloud deployments
- Gemini CLI sign-in flow or API-key-based auth depending on environment

Do not conflate Gemini API keys with Vertex configuration or CLI sign-in.

## Reference Files

Read only the files needed for the current task:

- `references/sdk-and-migration.md` -> modern SDK choices and migration rules
- `references/models-thinking-and-caching.md` -> model choice, thinking controls, thought signatures, caching
- `references/tooling-and-structured-output.md` -> function calling vs structured outputs
- `references/gemini-cli.md` -> Gemini CLI, `GEMINI.md`, scripting, and CLI usage

## Reading Guide

Only read the official docs relevant to the task:

### New Gemini app code

Read:

- SDK downloads / libraries
- quickstart
- function calling
- structured outputs
- model docs
- `references/sdk-and-migration.md`
- `references/tooling-and-structured-output.md`

### Thinking / advanced reasoning

Read:

- thinking guide
- thought signatures guide if tools are involved
- `references/models-thinking-and-caching.md`

### Repeated large context

Read:

- context caching
- `references/models-thinking-and-caching.md`

### Legacy code migration

Read:

- migration to Google GenAI SDK
- `references/sdk-and-migration.md`

### Gemini CLI customization

Read:

- Gemini CLI docs / repo docs for `GEMINI.md`, command modes, and scripting
- `references/gemini-cli.md`

## Implementation Heuristics

- If the request is app integration, patch real source files to use the official modern SDK.
- If the request is a repo-wide Gemini CLI behavior change, add or edit `GEMINI.md`.
- If the request is migration, update both imports and call structure.
- If the request needs typed downstream consumption, use structured outputs or function calling deliberately instead of loose prose parsing.

## Anti-Patterns

Do not:

- start new projects on legacy Gemini SDKs
- guess model IDs or preview status
- ignore thought signatures when manually replaying tool turns
- use function calling when structured outputs alone would solve the problem
- use structured outputs when the model needs to call a real external tool
- turn `GEMINI.md` into a dumping ground for every project note

## Final Checklist

Before you finish:

- Did you use the modern Google GenAI SDK for new code?
- Did you distinguish Gemini API work from Gemini CLI customization?
- Did you preserve or account for thought signatures where needed?
- Did you choose the right mechanism between function calling and structured outputs?
- Did you verify unstable model/version facts if they mattered?
