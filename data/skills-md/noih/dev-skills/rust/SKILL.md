---
name: rust
description: Rust development conventions and best practices. Use when writing any Rust code.
user-invocable: false
---

# Rust Conventions

## Naming Conventions (RFC 430)

| Item | Style | Example |
|------|-------|---------|
| Crates | `snake_case` | `my_crate` (hyphens in Cargo.toml map to underscores) |
| Modules | `snake_case` | `mod auth_handler;` |
| Types (struct, enum, trait) | `PascalCase` | `HttpRequest`, `ParseError` |
| Functions, methods | `snake_case` | `fn read_file()` |
| Local variables | `snake_case` | `let user_count = 0;` |
| Constants, statics | `SCREAMING_SNAKE_CASE` | `const MAX_RETRIES: u32 = 3;` |
| Type parameters | Short `PascalCase` | `T`, `K`, `V`, `E` |
| Lifetimes | Short lowercase | `'a`, `'de` |

The compiler warns on violations — treat these warnings as errors.

### Conversion method prefixes

Follow the standard library conventions:

| Prefix | Meaning | Ownership | Example |
|--------|---------|-----------|---------|
| `as_` | Cheap reference-to-reference | Borrows `&self` | `as_str()`, `as_bytes()` |
| `to_` | Expensive conversion | Borrows `&self` | `to_string()`, `to_vec()` |
| `into_` | Ownership-consuming conversion | Takes `self` | `into_inner()`, `into_vec()` |
| `from_` | Constructor from another type | Associated fn | `String::from_utf8()` |
| `try_` | May fail (returns `Result`) | Varies | `try_from()`, `try_into()` |

## Ownership & Borrowing

- Prefer borrowing (`&T`, `&mut T`) over cloning. Only `clone()` when ownership transfer is genuinely needed
- Prefer `&str` over `&String`, `&[T]` over `&Vec<T>` in function parameters — accept the most general form
- Use `Cow<'_, str>` when a function sometimes needs to allocate and sometimes doesn't
- Avoid returning references to local data — return owned types from public API boundaries

## Error Handling

- **`Result<T, E>` everywhere**: Use `Result` for all operations that can fail. Reserve `panic!` for truly unrecoverable states (violated invariants, programmer bugs)
- **`thiserror`** for libraries: Define typed error enums with `#[derive(Error)]` so callers can match on variants
- **`anyhow`** for applications: Use `anyhow::Result` in binaries and top-level application code where error variant matching isn't needed
- **`?` operator**: Propagate errors with `?`. Avoid manual `match` on `Result` just to re-wrap or return
- **`unwrap()` / `expect()`**: Only in tests, examples, or when the invariant is provably guaranteed. Prefer `expect("reason")` over bare `unwrap()` so panics are self-documenting

## Type Safety

- **Newtype pattern**: Wrap primitive types to prevent misuse — `struct UserId(u64)` instead of raw `u64`
- **Enums over booleans**: Prefer `enum Visibility { Public, Private }` over `is_public: bool` when the meaning isn't obvious
- **Make invalid states unrepresentable**: Model states as enums so the compiler prevents illegal transitions
- **`#[must_use]`**: Add on functions whose return value should not be silently ignored

## Trait Design

- Use traits for abstraction boundaries; prefer generics (`impl Trait` / `<T: Trait>`) for static dispatch, trait objects (`dyn Trait`) for dynamic dispatch
- Implement standard traits when appropriate: `Display`, `Debug`, `Clone`, `PartialEq`, `Default`, `From`/`Into`
- Derive what you can: `#[derive(Debug, Clone, PartialEq, Eq, Hash)]` — only implement manually when custom behavior is needed

## Pattern Matching

- **Exhaustive matching**: Prefer `match` over `if let` chains when there are more than two variants — the compiler catches missing cases
- **Avoid wildcard catch-all** (`_`) on enums unless intentional — adding a new variant should trigger a compile error, not silently fall through
- **Destructure in `match` arms**: Extract fields directly — `Err(e) => ...` not `Err(err) => { let e = err; ... }`
- **`if let`**: Use for single-variant checks — `if let Some(v) = opt { ... }`. For two variants, `match` is clearer

## Iterators

- **Prefer iterator chains** over manual `for` loops with mutable accumulators: `.filter().map().collect()` is idiomatic and often optimized equally
- **Avoid `collect()` mid-chain**: Chain iterators lazily; only `collect()` at the end when you need the final collection
- **Use `iter()` / `iter_mut()` / `into_iter()`** intentionally — borrowing vs consuming the collection

## Smart Pointers

| Type | Use when |
|------|----------|
| `Box<T>` | Heap allocation needed: recursive types, large values, trait objects (`Box<dyn Trait>`) |
| `Rc<T>` | Multiple owners in single-threaded context (rare — question if the design needs it) |
| `Arc<T>` | Multiple owners across threads |
| `Cow<'a, T>` | Sometimes borrowed, sometimes owned — avoids unnecessary clones |

- Default to stack allocation. Only `Box` when the compiler requires it or the value is too large for the stack
- `Rc`/`Arc` often signal a design issue — consider if ownership can be restructured first

## Modules & Visibility

- **Default to private**: Everything is private by default. Only expose what's needed
- **`pub(crate)`**: Prefer over `pub` for items used across modules within the crate but not exported to consumers
- **`pub(super)`**: For items shared with the parent module only
- **Module file layout**: Prefer `foo.rs` + `foo/bar.rs` (Rust 2018+) over the older `foo/mod.rs` style
- **Re-exports**: Use `pub use` in `lib.rs` to create a clean public API surface, even if the internal module structure is different

## Async & Concurrency

- **Don't block the runtime**: Never call blocking I/O or CPU-heavy code in an async context. Use `spawn_blocking` for these
- **Shared state**: Use `Arc<Mutex<T>>` or `Arc<RwLock<T>>` judiciously; prefer message passing (`mpsc`, `oneshot` channels) when data flows in one direction
- **Cancellation safety**: Futures can be dropped at any `.await` point. Don't hold locks across `.await` — acquire, use, and release within a synchronous block
- **`Send` + `Sync`**: Understand the bounds. Async tasks spawned with `tokio::spawn` require `Send`. If a type isn't `Send`, restructure or use `spawn_local`

## Testing

- **Unit tests**: Place in a `#[cfg(test)] mod tests` block at the bottom of the same file
- **Integration tests**: Place in the `tests/` directory at the crate root. Each file is compiled as a separate crate — they test the public API
- **Doc tests**: Code blocks in `///` doc comments are compiled and run as tests. Keep them simple and focused
- **`#[should_panic]`**: Use for tests that verify a `panic!` occurs — include `expected = "message"` to avoid false positives
- **Test naming**: `snake_case` describing the scenario — `fn rejects_empty_input()`, not `fn test_1()`
- **Assertions**: Prefer `assert_eq!` / `assert_ne!` over `assert!(a == b)` — the error message shows both values on failure

## Money (Decimal)

- Use `rust_decimal` crate for all monetary calculations — never use `f32`/`f64` for money (floating-point precision issues)
- Use `rust_decimal_macros` with `dec!()` macro for literals: `dec!(19.99)`
- Serialize with `#[serde(with = "rust_decimal::serde::str")]` to ensure JSON transmits as string, avoiding precision loss

## JSON Serialization

- `Option<T>` serializes as `null` by default. Use `#[serde(skip_serializing_if = "Option::is_none")]` when an API contract requires omitted absent fields

## Tooling

- **`cargo fmt`**: Format all code. Don't override `rustfmt` defaults without team consensus
- **`cargo clippy`**: Run with `-- -D warnings` to treat lints as errors. Fix the lint, don't `#[allow]` it unless there's a documented reason
- **`cargo audit`**: Check dependencies for known vulnerabilities
- **`cargo doc --open`**: Verify documentation renders correctly

## Performance

- Leverage zero-cost abstractions — iterators, generics, and traits compile to the same code as hand-written loops
- Avoid unnecessary heap allocations: prefer `&str` over `String`, `&[T]` over `Vec<T>` when ownership isn't needed
- Use `serde` efficiently: `#[serde(skip)]` for derived fields, `#[serde(rename_all = "camelCase")]` instead of per-field renames
- Profile before optimizing: use `cargo bench`, `criterion`, or `flamegraph`. Don't guess where the bottleneck is
