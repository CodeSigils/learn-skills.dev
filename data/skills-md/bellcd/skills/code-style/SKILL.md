---
name: code-style
description: Use when writing or reviewing code of any kind, or installing a package.
---

# Code Style

Rules phrased "in general" or "prefer" are strong defaults. Deviate only for a specific reason, and point out why to the user.

Load only the reference files relevant to the current task:

- [GENERAL.md](GENERAL.md): applies to all languages
- [JAVASCRIPT.md](JAVASCRIPT.md)
- [TYPESCRIPT.md](TYPESCRIPT.md)
- [REACT.md](REACT.md)
- [NPM.md](NPM.md)
- [TESTING.md](TESTING.md)
- [PLAYWRIGHT.md](PLAYWRIGHT.md)

## Security (always applies)

- Never read unencrypted `.env` files. When you need a value, ask for it, or trace the variable's usage through code, CI config, and `config.toml` instead.
- Avoid logging HTTP request/response headers. They often contain secrets.
