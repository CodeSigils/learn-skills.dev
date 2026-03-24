---
name: pi-coding-agent-sdk
description: Understand and build with the @mariozechner/pi-coding-agent SDK from pi-mono. Use when a request is about the pi SDK or pi-mono SDK, especially createAgentSession, DefaultResourceLoader, AuthStorage, ModelRegistry, SessionManager, SettingsManager, built-in or custom tools, extensions, prompt templates or slash commands, AGENTS context loading, sessions, run modes, or tracing where SDK behavior lives in pi-mono source.
---

# Pi Coding Agent SDK

## Overview

Use this skill to explain the public `@mariozechner/pi-coding-agent` SDK, choose the right example or API surface, and build integrations that stay on exported APIs first.

Default to the public docs, examples, and `packages/coding-agent/src/index.ts`. Use source-level tracing only when the docs are ambiguous, incomplete, or the user explicitly asks where behavior lives in pi-mono.

If the task is about `pi install`, package manifests, distribution, or publishing a Pi package, use `pi-package-creator` instead of stretching this skill.

## Task Routing

- Read `references/surface-and-examples.md` for public exports, example selection, and “what should I import?”
- Read `references/resource-loading-and-context.md` for `DefaultResourceLoader`, discovery rules, `AGENTS.md`, skills, prompts, and extension loading paths.
- Read `references/tools-extensions-and-prompts.md` for built-in tools, tool factories, `customTools`, extension-registered tools, prompt templates, slash-command behavior, and extension API boundaries.
- Read `references/models-settings-sessions.md` for `AuthStorage`, `ModelRegistry`, `SettingsManager`, `SessionManager`, events, and run modes.
- Read `references/source-crosswalk.md` only when the docs/examples are not enough or the user asks where the SDK is implemented in pi-mono.

## Default Workflow

1. Start with the public surface:
   `packages/coding-agent/docs/sdk.md`, `packages/coding-agent/examples/sdk/README.md`, the relevant example file, and `packages/coding-agent/src/index.ts`.
2. Confirm the exported API before recommending imports or code shape. Do not suggest non-exported internals as a normal integration path.
3. Use the closest example as the starting pattern before inventing a new structure.
4. Distinguish clearly between:
   documented behavior from docs/examples,
   exported API confirmed from `src/index.ts`,
   and inferences from lower-level source files.
5. Prefer public API code in implementations. Use lower-level source only for explanation, debugging, or repo navigation.
6. If the question broadens into monorepo architecture, explain that `packages/coding-agent` is the SDK surface and use `references/source-crosswalk.md` to map deeper layers.

## Gotchas

- Prebuilt tool instances such as `readTool` and `bashTool` resolve paths from `process.cwd()`. If a caller sets a custom `cwd` and also passes explicit `tools`, switch to the factory functions such as `createReadTool(cwd)` or `createCodingTools(cwd)`.
- Passing a custom `ResourceLoader` changes resource discovery. `cwd` and `agentDir` still matter for session naming and tool path resolution, but they no longer drive skills, prompts, themes, or extension discovery unless the loader does so.
- `session.prompt()` throws during streaming unless the caller supplies `streamingBehavior`. Use `steer()` or `followUp()` directly when that is clearer.
- The docs and examples use `prompt templates` and `slash commands` for the same user-facing surface. Treat file-based prompt templates as slash-command content expansion.
- The example README names `08-slash-commands.ts`, but the current file in the repo is `08-prompt-templates.ts`. Prefer the real file path over the README label.
- `customTools` is still a public SDK option even though `examples/sdk/06-extensions.ts` frames extensions as the main system for registering reusable tools. Use `customTools` for inline programmatic integrations and extensions for reusable, discovery-driven behavior.

## Reference Map

- `references/surface-and-examples.md`
  Use first for public API questions and example routing.
- `references/resource-loading-and-context.md`
  Use for discovery, loader overrides, `AGENTS.md`, and context assembly.
- `references/tools-extensions-and-prompts.md`
  Use for tools, extensions, commands, prompt templates, and related API tradeoffs.
- `references/models-settings-sessions.md`
  Use for auth, models, settings, session persistence, events, and run modes.
- `references/source-crosswalk.md`
  Use for source tracing, adjacent pi-mono packages, and optional local `pi-extensions` examples.
