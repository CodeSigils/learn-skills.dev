---
name: design-tokens
description: "Use when naming or structuring theme variables: primitive vs semantic vs component tiers, CSS custom properties, Tailwind theme config, and multi-brand overrides."
---


# Naming and Tiering Theme Variables

Default to two tiers and earn the third. A primitive tier holds raw values named for what they *are* (`--gray-2`, `--space-4`), a semantic tier holds roles named for what they *do* (`--color-surface`, `--gap-section`), and a component tier exists only where a component must deviate from its role *and* that deviation must stay themeable. References flow in exactly one direction — component reads semantic, semantic reads primitive, and nothing ever reads upward or skips a tier. That single rule is what makes a theme swap a one-line change instead of a search. This skill decides what a variable is *called* and which tier it lives in; `color` decides what value goes in it, and `dark-mode` consumes the override layering defined here rather than inventing its own. If the question is "which oklch value", you are in the wrong skill.

**Read the existing token layer before adding a name to it.** Find where the project declares theme values — `:root` custom properties, a Tailwind v4 `@theme` block, a JS/TS theme object, a Style Dictionary pipeline — and how it names them, then match that convention even when you would have chosen differently. A codebase with one imperfect naming scheme beats one with two good ones. Never stand up a parallel token file next to an existing one, and never introduce a second theme-switching mechanism on top of the one already wired.

## Quick Reference

| Open this | When |
| --- | --- |
| [naming-map.md](references/naming-map.md) | You need a concrete name for a specific token, or you are translating between CSS custom properties and Tailwind utility names in either direction. |
| [multi-brand.md](references/multi-brand.md) | More than one brand, tenant, or white-label skin must share one component set, or a brand override is leaking outside its scope. |

## Core Principles

1. **Name primitives for what they are, semantics for what they do, components for where they live.** `--blue-500` is a fact, `--color-accent` is a decision, `--button-bg` is a location. A semantic token named after its current value — `--color-blue-button` — is a landmine that detonates the first time the brand changes. *Exception:* neutrals may keep a value-shaped primitive name (`--gray-*`) even in systems that otherwise abstract everything, because the ramp position *is* the meaning.

2. **Let references flow downward only, one tier at a time.** A component reading `--gray-2` directly cannot be re-themed, and a semantic token reading another semantic token creates an alias chain nobody can trace. *Exception:* a semantic token may alias one other semantic token when it names a genuinely narrower role — `--color-border-input` pointing at `--color-border` is a real refinement, not a rename.

3. **Earn the component tier; two tiers is the default.** A component token is justified only when the component must diverge from its role *and* the divergence must remain themeable per brand or theme. A one-off value used in exactly one place is not a token — it is a value, and hardcoding it in the component is the correct answer. *Exception:* any component published as a library API, where consumers need a documented hook to restyle without forking.

4. **Override by re-binding the semantic tier, never by redeclaring primitives.** Themes and brands change which primitive a role points at; they never change what `--gray-2` means, because that would silently move every other role built on it. *Exception:* a genuine brand *palette* swap, where the primitive ramp itself is regenerated — and then it is regenerated wholesale, not one step at a time.

5. **Namespace anything generated or learned.** This pack's own dynamic skills are prefixed `house-` for exactly this reason: a same-named declaration silently overrides the authored one and leaves no trace at the call site. Generated, imported, or per-tenant tokens carry a prefix that cannot collide with hand-authored names. *Exception:* none — an unprefixed generated token is a bug waiting for a name collision.

6. **Land every override at the same selector depth.** All theme and brand overrides live at one root-level selector — `[data-theme]`, `.dark`, `[data-brand]` — so precedence is decided by source order rather than specificity arithmetic. A single override nested inside a component wins forever and cannot be undone downstream. *Exception:* a deliberately scoped sub-theme (an inverted hero, a code block), which is scoped *by design* and documented as such.

7. **Count occurrences before you coin a name.** A value appearing once is a value; twice is a coincidence; three times is a token. Tokenizing early produces a vocabulary nobody learns, and every unlearned token gets bypassed with a literal. *Exception:* accessibility-critical values — focus ring width, minimum hit target — which are tokenized on first use because they must never drift.

8. **In Tailwind v4, put the primitive ramp in `@theme` and the runtime flip on plain custom properties.** Tokens named `--color-<name>-<step>` inside `@theme` materialize the whole utility set (`bg-berry-400`, `text-berry-100`, `border-berry-700`), and the slash modifier composes — `text-berry-600/75` emits the alpha form. Semantic roles that must change at runtime are ordinary properties flipped at the theme selector. *Exception:* a semantic role that must also exist as a utility (`bg-surface`) is declared in `@theme` as well, with the flip kept on the primitive it references.

9. **Delete aliases that only rename.** `--color-primary: var(--color-accent)` with both in use means every future reader must check which one a given component happened to pick. Pick one, migrate the other, delete it. *Exception:* a time-boxed deprecation alias during a rename, which ships with the migration that removes it.

10. **Migrate hardcoded values by frequency, not by file.** Sweep the codebase for literals, group them by exact value, and convert the highest-count groups first — that is where the token pays for itself. Converting file by file leaves half a system in each state for months. *Exception:* a file being rewritten anyway, which is converted completely while it is open.

11. **Keep one scale per dimension and let it be boring.** One spacing scale, one radius scale, one z-index scale, one duration scale. Two competing scales for the same dimension is how a design system dies, and the second one is always introduced with a good reason. *Exception:* a documented density mode, which is the *same* scale re-bound at the semantic tier, not a second set of primitives.

## Smells and Fixes

| Smell | Fix |
| --- | --- |
| `--color-blue-button` | Rename to the role it plays; the value belongs to the primitive tier |
| A component reading `--gray-2` | Insert or point at the semantic role |
| `--color-primary: var(--color-accent)`, both used | Pick one, migrate, delete the other |
| A component token used in exactly one place, never overridden | It is a value; hardcode it and remove the token |
| A theme override nested inside a component | Move it to the single root-level theme selector |
| `--gray-2` redeclared under `[data-theme="dark"]` | Re-bind the semantic role instead; the ramp is not the theme |
| Generated or per-tenant tokens sharing the hand-authored namespace | Prefix them so a collision cannot be silent |
| Two spacing scales | Consolidate; the newer one is a density mode at the semantic tier |
| `@theme` tokens redeclared under a selector to switch themes | Keep the flip on plain custom properties |
| Hex literals scattered through components | Sweep by value frequency and convert the biggest groups first |

## Reporting a Token Change

Report by tier, not by file. For each tier, list added, renamed, and removed tokens; for every rename give both names and the count of call sites migrated; for every removal state what now covers the case. Close with the tokens you deliberately did *not* create and why — usually because a value appeared fewer than three times — since that is the part a reviewer cannot reconstruct from the diff.

## Checklist

- [ ] Every token sits in exactly one tier, named for that tier's job
- [ ] References flow downward only; no component reads a primitive
- [ ] Every component token is overridden somewhere, or it is not a token
- [ ] Themes re-bind semantic roles; primitives are untouched by theme
- [ ] Generated and per-tenant tokens are namespaced against collision
- [ ] All overrides land at one root-level selector
- [ ] Tailwind `@theme` holds the ramp; the runtime flip is on custom properties
- [ ] No alias exists purely to rename another token
- [ ] One scale per dimension — spacing, radius, z-index, duration
- [ ] Remaining hardcoded literals are listed, not silently left behind
