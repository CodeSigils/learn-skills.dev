---
name: substrate
description: >
  Use when working with ELPS Lisp code, substrate phylum code, or .lisp files.
  Provides hover docs, go-to-definition, find-references, diagnostics, performance
  analysis, eval, test, and formatting for ELPS code with full substrate builtin
  awareness (cc:*, statedb:*, sidedb:*, crypto:*, router:*). Also provides the
  complete shirotester CLI for linting, debugging, REPL, and test execution.
metadata:
  short-description: ELPS/substrate development toolkit via shirotester MCP
  author: luthersystems
version: 1.0.0
---

# Substrate -- ELPS Development Toolkit

[Luther Enterprise](https://enterprise.luthersystems.com/) is Luther Systems' platform for building and operating regulated, auditable business processes. **Substrate** is the core runtime of Luther Enterprise -- an execution environment for business logic written in [ELPS](https://github.com/luthersystems/elps) (a Lisp dialect). Business logic modules are called **phyla** (singular: phylum) -- packages of `.lisp` files that define endpoints and business rules.

**shirotester** is the development toolkit for substrate. It provides an MCP server, language server, semantic linter, performance analyzer, debugger, REPL, test runner, and documentation browser -- all with full awareness of substrate's built-in packages (`cc:*`, `statedb:*`, `sidedb:*`, `crypto:*`, `router:*`, etc.).

### Resources

- [Luther Enterprise](https://enterprise.luthersystems.com/) -- the platform substrate powers
- [Documentation](https://docs.luthersystems.com) -- Luther Enterprise docs
- [ELPS Language](https://github.com/luthersystems/elps) -- the Lisp dialect
- [Substrate](https://github.com/luthersystems/substrate) -- the core runtime
- [VS Code Extension](https://marketplace.visualstudio.com/items?itemName=LutherSystems.substrate) -- syntax highlighting, LSP, debugging
- [npm: @luthersystems/shirotester](https://www.npmjs.com/package/@luthersystems/shirotester) -- install via npx
- [shirotester CLI docs](https://github.com/luthersystems/substrate/blob/main/cmd/shirotester/README.md)

## VS Code Extension

A companion [VS Code extension](https://marketplace.visualstudio.com/items?itemName=LutherSystems.substrate) provides the full IDE experience:

- Syntax highlighting for ELPS with substrate-specific forms (`defendpoint`, `route-success`, `route-failure`)
- Language server via `shirotester lsp` with full substrate builtin resolution
- DAP debugger via `shirotester debug` with breakpoints, stepping, and statedb inspection
- ELPS source formatting via `shirotester fmt`

Install: search "Substrate" in the VS Code marketplace or run `ext install LutherSystems.substrate`.

The MCP skill and VS Code extension are complementary -- the skill brings substrate intelligence to any AI coding tool, the extension brings it to VS Code.

## MCP Server

shirotester includes an MCP server that runs locally via stdio. No API keys, authentication, or remote servers required -- everything runs on your machine.

### If the MCP server is not connected

Before using substrate tools, check if the `shirotester` MCP tools (like `hover`, `diagnostics`) are available. If not, add the MCP server:

**Claude Code:**

```bash
claude mcp add shirotester -- npx -y @luthersystems/shirotester mcp --workspace-root .
```

**Codex:**

```bash
codex mcp add shirotester -- npx -y @luthersystems/shirotester mcp --workspace-root .
```

**Cursor:** Open Settings > MCP > Add new MCP server > paste:

```json
{
  "mcpServers": {
    "shirotester": {
      "command": "npx",
      "args": ["-y", "@luthersystems/shirotester", "mcp", "--workspace-root", "."]
    }
  }
}
```

**Windsurf:** Add via Windsurf MCP settings with the same config as Cursor.

**Antigravity:** Open "..." menu > MCP Servers > Manage MCP Servers > View raw config > add:

```json
{
  "mcpServers": {
    "shirotester": {
      "command": "npx",
      "args": ["-y", "@luthersystems/shirotester", "mcp", "--workspace-root", "."]
    }
  }
}
```

## MCP Tool Catalog

| Tool | Description |
|------|-------------|
| `hover` | Hover documentation for a symbol at a position |
| `definition` | Go-to-definition for a symbol |
| `references` | Find all references to a symbol |
| `diagnostics` | Semantic diagnostics (errors, warnings) for a file or workspace |
| `call_graph` | Call graph analysis for a function |
| `hotspots` | Identify performance hotspots in the codebase |
| `perf_issues` | Detect performance anti-patterns (PERF001-PERF004) |
| `eval` | Evaluate an ELPS expression in a shiro environment |
| `test` | Run ELPS unit tests |
| `doc` | Browse runtime documentation for packages and symbols |
| `format` | Format ELPS source code |
| `lint` | Semantic linting with cross-file symbol resolution |
| `workspace_symbols` | Search for symbols across the workspace |
| `document_symbols` | List symbols in a specific file |
| `describe_server` | Describe the MCP server capabilities |

## Substrate & ELPS Concepts

### What is a Phylum?

A **phylum** is a package of `.lisp` files that define business logic endpoints and rules. Phyla are written in ELPS and run inside the substrate execution environment, which provides built-in packages for state management, routing, cryptography, and external service integration.

### Key ELPS Concepts

- **Packages**: Code is organized into packages with `(in-package 'my-service)` and `(use-package 'router)`
- **Endpoints**: Business logic entry points defined with `(defendpoint "method-name" (params) ...)`
- **Responses**: Endpoints return results via `(route-success result)` or `(route-failure error)`

### Substrate Packages

| Package | Purpose |
|---------|---------|
| `router` | Endpoint registration (`defendpoint`, `route-success`, `route-failure`) |
| `statedb` | State database operations (get, put, range queries, pagination) |
| `utils` | Crypto, serialization, validation helpers |
| `sidedb` | Private data collections |
| `connector` | External service integration |
| `batch` | Async batch operations |
| `cc` | Core chaincode context (logging, transaction info) |

### Typical Phylum Structure

```lisp
(in-package 'my-service)
(use-package 'router)
(use-package 'utils)
(use-package 'statedb)

(set 'version "1.0.0")

(defendpoint "create-item" (params)
  (let* ((id (generate-id))
         (item (sorted-map "id" id
                           "name" (get params "name")
                           "created" (cc:timestamp))))
    (statedb:put id item)
    (route-success item)))

(defendpoint "get-item" (params)
  (let ((item (statedb:get (get params "id"))))
    (if item
        (route-success item)
        (route-failure "not found"))))
```

## shirotester CLI

The MCP server exposes a subset of shirotester's capabilities. The full CLI includes additional tools, all available via `npx @luthersystems/shirotester <command>`:

| Command | Description |
|---------|-------------|
| `mcp` | MCP server over stdio (what this skill configures) |
| `lint` | Semantic linting with cross-file symbol resolution and substrate builtins |
| `analyze` | Call-graph performance analysis with text, JSON, SARIF, or Mermaid output |
| `debug` | DAP debugger with breakpoints, stepping, and statedb inspection |
| `repl` | Interactive ELPS REPL with full substrate builtins |
| `lsp` | Language Server Protocol server (stdio or TCP) |
| `fmt` | Format ELPS source files |
| `unit-tests` | Run `*_test.lisp` unit tests in a shiro environment |
| `functional-tests` | Run YAML-defined RPC test scenarios |
| `doc` | Runtime documentation browser for all packages and symbols |
| `version` | Print version |

Examples:

```bash
npx @luthersystems/shirotester lint ./phylum
npx @luthersystems/shirotester analyze --format sarif ./phylum
npx @luthersystems/shirotester doc statedb
npx @luthersystems/shirotester unit-tests ./phylum
```

## Deep Dive with `doc`

Use the `doc` MCP tool or CLI for runtime documentation of any package or symbol:

- `doc` -- list all available packages
- `doc cc` -- show all exports in the `cc` package
- `doc statedb:get` -- show documentation for a specific symbol
- `doc router:defendpoint` -- show endpoint registration docs

The `doc` tool resolves all substrate builtins, including Go-registered functions that are invisible to standalone ELPS tools.

For comprehensive language and platform guidance, see the [ELPS repo](https://github.com/luthersystems/elps) and [substrate CLAUDE.md](https://github.com/luthersystems/substrate/blob/main/CLAUDE.md).
