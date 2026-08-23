---
name: jetpack-compose
description: >
  Jetpack Compose engineering conventions. Use together with the `kotlin` skill.
---

# Libraries

- Prefer official Jetpack Compose and AndroidX libraries.
- Use Navigation3 as navigation library.
- Use Room 3 exclusively for local database storage.

# Structure

Use different hierarchy strategies for UI and non-UI code.

- **Layer-first for non-UI code.** Top-level packages represent architectural layers such as `api`, `domain`, `database`, `platform`, and `utils`. Organize code within those layers by responsibility when needed.
- **Feature-first for UI code.** Organize UI around screens under `ui/page/`.
- **One screen = one package.** Never place multiple screens directly in the same screen package.
- A standalone screen lives at `ui/page/<screen>/`.
- A family or flow of related screens lives under a common group package, with each screen still having its own package: `ui/page/<group>/<screen>/`.
- A group package organizes related screens; it is not itself a screen package.
- Keep screen-owned code inside its screen package.
- Keep the primary `*View`, `*Model`, `*ViewModel`, and `*Route` directly in the screen package.
- When enough supporting code of one responsibility accumulates, group it into a focused screen-owned subpackage such as `component/`, `model/`, or another appropriately named package.
- Do not create subpackages preemptively. Keep the screen package flat until a meaningful group exists.
- Put code shared only by screens in the same group at their closest common group package, following the same responsibility-based structure.
- Put reusable cross-feature UI under `ui/component/`.
- Promote code to a broader package only when its ownership is genuinely broader.

# Screen architecture

Each screen package owns its screen architecture and screen-specific components.

Represent a screen with four primary pieces:

- `*View`: stateless UI containing the complete visual structure of the screen. Takes a screen-specific `*Model`, observable data required for rendering, and typed callbacks. Contains no business logic or navigation.
- `*Model`: complete immutable screen-specific UI state.
- `*ViewModel`: owns business operations, network requests, screen-specific persistent UI state, model updates, and dedicated Room observers. Keep Room-backed state separate from the screen Model.
- `*Route`: glue between ViewModel and View. Collects observable state, provides navigation/environment dependencies, owns effects, and connects callbacks.

Persistent UI state belongs to Model/ViewModel. Views may remember only transient rendering state such as animation, gesture, layout, or measurement state.

Keep navigation and external side effects at Route/ViewModel boundaries. Prefer typed callbacks into Views.

## Components

Treat each UI file as one independently understandable, testable, and previewable UI unit.

- Keep the complete screen layout cohesive inside its `*View`, even when the View becomes large.
- Do not extract private composables merely to reduce function or file size.
- Extract UI only when it has a distinct responsibility and deserves to become a real component.
- Extract components by responsibility, never merely by size.
- Put each screen-specific component in its own file under that screen's `component/` package.
- Put components shared only by screens in the same group under that group's `component/` package.
- Put reusable cross-feature components under `ui/component/`.
- Do not define multiple independent components in one file.

# Previews

Previews belong to the UI unit they demonstrate.

- Always keep previews in the same file as the View or component they preview.
- Place previews after the implementation.
- Never create separate preview files.
- Previews are part of the UI unit, not independent UI units; any number of previews may live beside their single View/component.
- Use multiple previews to cover meaningful visual and business states of that unit.
- Keep preview-only fixtures private and in the same file.
- Do not use a screen View preview as a Cartesian showcase of every state of its child components; preview those components in their own files.
- Name previews `Preview<ComposableName><State>`, omitting the `View` suffix from screen Views, e.g. `SettingsProfileView` → `PreviewSettingsProfileInitializing`.
- Use a project-wide preview theme wrapper providing `MaterialTheme` and required `CompositionLocal`s. Create one if absent.

# State and rendering

- ViewModel owns and exposes the data sources and Room observers required by the screen; Route performs Compose subscriptions to them.
- Leaf components must not own feature-level repository or Room subscriptions.
- Scope observers to the required domain and preserve stable state across recomposition. Avoid per-item observers unless explicitly required by the data source or ownership model.
- Keep gesture ownership at the container that owns the coordinate system; use parent-level hit testing when necessary.
- Preserve stable component identity. Key live data by stable IDs, not mutable snapshots.
- For continuous geometry such as time, use one canonical coordinate transform for rendering, items, hit testing, and boundaries.

# Data flow

For persistent backend data used by UI, prefer a local-first reactive flow:

`ViewModel → Network → Room Repository → Room Observer → Route → View`

Room is the source of truth for persistent backend data.

- ViewModel initiates network operations. Successful persistent results are written through the Room repository.
- Do not copy Room-backed data into the screen `Model`. Keep persisted data and ViewModel-owned UI state as separate state channels.
- ViewModel owns dedicated Room observers for the persisted data required by the screen. A screen may have one or several observers.
- Room observers may be parameterized when the observed query depends on current screen state or arguments.
- Each observer exposes a subscribable value backed by a repository `Flow`.
- Route subscribes to the screen `Model` and Room observers independently, then passes their current values into View.
- View receives plain prepared values and remains unaware of Room, repositories, and network access.
- Repositories expose convenient, purpose-specific `Flow`s rather than requiring ViewModel or UI code to assemble raw database state.
- Do not persist inherently transient data merely to satisfy this pattern.

# Room

Use a consistent structure for persisted types:

`DatabaseInterface → DatabaseModel / DatabaseEntity → Dao → Repository`

## Models

- Define a small `*DatabaseInterface` containing the value shared by database representations.
- `*DatabaseModel` represents the database-facing value outside Room.
- `*DatabaseEntity` is the Room entity and implements the same interface.
- Keep explicit conversion between DatabaseModel and DatabaseEntity.
- Use `kotlin.uuid.Uuid` for UUID identifiers.
- Keep the Room table name as `TABLE_NAME` on the entity.

## DAO

Keep DAOs focused on database operations.

Provide only operations required by the domain, commonly:

- singular and collection reads;
- `Flow` variants for observable reads;
- insert/update with `OnConflictStrategy.REPLACE`;
- singular and bulk deletion.

Prefer Room `Flow` queries for observable data rather than manually invalidating or refreshing cached state.

## Repository

Hide DAOs behind a repository.

- Repository APIs expose domain values, not Room entities.
- Convert entities at the repository boundary.
- Expose convenient typed `Flow`s already mapped into values useful to consumers.
- Keep Room-specific details inside the database layer.
- Treat a missing value as an explicit domain/database condition rather than leaking nullable Room results when absence is exceptional.
- Log meaningful database reads, writes, deletes, and Flow updates at debug/verbose level.

## Complex values

For complex serializable values stored as a single database field:

- Prefer a typed Room converter backed by CBOR serialization.
- Keep converters generic/reusable where practical.
- Reference actual Kotlin types rather than hardcoded type names.

# CompositionLocal

Use `CompositionLocal` for ambient, subtree-scoped presentation policy such as theme tokens, spacing, padding, borders, and component styling.

- Provide overrides at the nearest owner boundary.
- Provide stable defaults at the theme/root boundary.
- Do not use CompositionLocal for business state, persistent mutable state, callbacks, or ordinary data dependencies.
- Prefer explicit parameters when a value affects component behavior rather than ambient presentation.

# Theme

Prefer `MaterialTheme` for visual configuration.

Use project-specific overrides, typically through `CompositionLocal`, when MaterialTheme does not express the required component-level presentation policy.
