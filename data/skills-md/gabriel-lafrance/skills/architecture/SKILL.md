---
name: architecture
description: >-
  Shape scalable code: domain services with public APIs, strong primitives
  inside deep modules, simple entry points, clear folders, write-path data
  design. Dual skill: agent picks standalone vs flow via variants.md. Use when
  adding features, splitting logic, designing data/reads, or about to dump
  files / duplicate domain logic. User must invoke.
disable-model-invocation: true
---

# Architecture

**Ask style:** [../pack-shared/asking.md](../pack-shared/asking.md) · **Variants:** [../pack-shared/variants.md](../pack-shared/variants.md)

## Variant

Choose **exactly one** per [variants.md](../pack-shared/variants.md) — never both:

- Standalone fits → Read [standalone.md](standalone.md) only
- Flow fits → Read [flow.md](flow.md) only
- Missing `standalone.md` or `flow.md` → matching missing-variant message; do not invent process
- If `variants.md` itself cannot be Read → still pick from the bullets above; do not stop
