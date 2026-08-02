---
name: personwise-create-course
description: Create, refine, resume, publish, or query polished PersonWise courses from topics, text, PDF/PPTX/DOCX/Markdown/TXT documents, or reference images through the paired OAuth MCP. Use for staged course authoring, source-grounded lessons, slide and narration review, visual QA, presenter selection, layout configuration, link sharing, or Topics review submission.
license: MIT
---

# Create a PersonWise course

Use the PersonWise Course Creation MCP as a staged authoring system. Produce one durable,
ordinary PersonWise course per create call, review it at its stable checkpoints, and finish the
result authorized by the user's OAuth connection.

This Skill is an optional quality playbook. The PersonWise MCP is complete and usable without this
Skill, and Skill presence or version must never gate an MCP operation.

On first use, install a missing PersonWise MCP with the current host's native supported MCP
install/add mechanism. Treat setup as an ordinary part of the requested course task, not as a
manual prerequisite for the user. Prefer the dependency metadata in `agents/openai.yaml` when the
host consumes it; otherwise invoke the host's official mechanism available to the Agent. Do not
manually edit or guess the host's backing configuration when a native mechanism exists. Then start
OAuth immediately; the user participates only in browser consent, and the Agent resumes the task.
If the browser completes consent but the Agent is not resumed, recover once with the complete
loopback callback URL procedure in
[references/connection-and-auth.md](references/connection-and-auth.md); never extract codes or
tokens.

## Read the relevant references

Before a mutating course task:

1. Read [references/course-design.md](references/course-design.md) completely.
2. Read [references/course-archetypes.md](references/course-archetypes.md) completely.
3. Read [references/workflow.md](references/workflow.md) completely.
4. Read [references/visual-quality.md](references/visual-quality.md) completely when the request
   uses images or the current Agent can consume MCP image/resource content.

Read [references/connection-and-auth.md](references/connection-and-auth.md) completely when the
MCP is absent, OAuth is incomplete, capability readiness is unproven, or authorization has
failed. For a query-only request, read connection/auth and the query section of `workflow.md`.

## Verify the MCP capability first

Before any credit-consuming action, read `personwise://course-agent/capabilities` or call
`get_course_agent_capabilities`.

Require all of the following:

- resource `https://mcp.personwise.ai/mcp`;
- a compatible MCP `contract_version`;
- every tool needed for the requested workflow in `supported_tools`;
- the relevant upload/image capability for any requested document or visual operation.

Stop before creation only when the MCP contract major is incompatible or a tool required for the
requested workflow is absent. Never compare, require, or upgrade a Skill version. If the MCP itself
is missing, use the bundled connection reference; do not send the user to a separate installation
site.

## Default to authorized end-to-end production

An explicit request to create a course authorizes the ordinary stages needed to complete that
course within the active OAuth grant. Unless the user reserves a manual checkpoint or requests a
narrower result, proceed autonomously through:

- blueprint and source-boundary selection;
- one durable create and source processing;
- Outline, Page text, and Narration review and objective corrections;
- Reference or Pin attachment when supplied;
- image generation and the capability-aware visual branch;
- presenter, Voice, and layout configuration;
- first publish and the user-requested final target;
- completion verification.

Do not repeatedly ask the user to approve internal checkpoints or ordinary course capabilities.
The OAuth connection grants the complete ordinary course workflow, but it is not authority to
exceed the user's request. A requested draft or private result stays draft or private. A normal
omitted target resolves to link-accessible and noindex.

Stop for user input only when a real blocker remains: required OAuth authorization, insufficient
course credit, an unrecoverable or missing source, a material product choice with multiple valid
outcomes, an explicitly reserved review point, or an irreversible action outside this public tool
surface.

## Classify the request

Choose one primary lane:

- **Topic-led or supplied-text course:** use `knowledge_source_mode=open`; place the durable compact
  constitution in `topic` and use `content` only when aligned long-form input is needed.
- **Strict document-grounded course:** use `materials_only`, declare the exact retained document
  count, upload all documents, and wait for canonical processing before generation.
- **Source-assisted research:** use `open` with documents when supplied facts should anchor the
  lesson but permitted model knowledge may supplement them.
- **Resume or repair:** inspect the existing run and course before mutation. Continue only from its
  fresh `allowed_actions`.
- **Refine:** fetch a fresh authoring snapshot, preserve slide count/order, and change only existing
  `title`, `key_points`, `page_text`, or `script` fields while unpublished.
- **Query:** search bounded metadata with `list_courses`; use `get_course` or
  `get_authoring_snapshot` only when needed and authorized.

For multiple courses, create one durable run per course. Full course access does not turn one call
into an unbounded batch or bypass credits, concurrency, and rate limits.

## Drive the production sequence

### 1. Build the blueprint

Record a secret-free blueprint containing:

- learner, outcome, course class, teaching archetype, language, and factual authority;
- earned page count and page-by-page teaching arc;
- visual system, diagram/table/image jobs, spoken style, and exclusions;
- presenter/Voice brief;
- requested final target: `draft`, `private`, `link`, or explicitly authorized `topics_review`.

Use `course-design.md` and `course-archetypes.md`; do not force unrelated subjects into the same
template.

### 2. Start one orchestrated durable run

When capabilities report `supports_orchestrated_creation=true`, use `start_course_creation` with a
stable non-secret idempotency key. Explicitly declare the current Agent's real
`visual_review_capability` as `multimodal` or `none`; never infer or overstate it. The server owns
the slow Outline, Narration, image, configuration, CDN, publish, and distribution stages. A normal
tool call returns quickly; use `get_run` no earlier than its `poll_after_seconds` guidance.

The server pauses for Agent review at `outline_ready` and `script_ready`. These are not mandatory
human confirmation gates: inspect, make objective corrections if needed, then call `advance_run`
once with the fresh revision. A multimodal run also pauses at `image_ready`; a non-vision run
automatically continues and records `visual_review_status=not_performed` with its reason.

Use legacy `create_course` only when the connected contract does not advertise orchestrated
creation. In that fallback, follow the bounded legacy sequence in `workflow.md`.

Never chain two mutating calls. A mutation result, including one that returns a new revision, does
not replace the required fresh reads before the next mutation.

For document inputs, use `request_upload_ticket` and `get_upload_status`. The remote server cannot
read a local path. Use the returned machine handoff when the host can transmit bytes; otherwise let
the user complete the returned PersonWise browser action. Do not expose ticket secrets or private
file contents in the run ledger.

### 3. Review staged content

At `outline_ready`, inspect every title and Key-point set for one clear teaching job, progression,
coverage, factual support, and non-repetition. Apply the smallest objective corrections with
`update_slides`, then fetch a fresh snapshot and revision.

Approve the reviewed Outline once. The server then generates Page text and Narration durably; do
not issue per-page mutations. Poll according to `poll_after_seconds`. At `paused / script_ready`,
review every aligned set:

```text
title + key_points -> what the page teaches
page_text          -> concise visible slide content
script             -> spoken explanation and transitions
```

Correct unsupported facts, source drift, contradictions, pedagogical failures, and brief
violations. Do not rewrite coherent model-authored choices merely to express taste.

Attach supplied Reference or Pin images only during the allowed `script_ready` window. Reconcile an
ambiguous upload before issuing another ticket.

### 4. Generate and review images

Advance from the freshest revision and poll with bounded backoff until every slide has canonical
image state and the run reaches `image_ready`.

- If the Agent can consume the MCP-native image content (or its protected-resource fallback), use
  `get_slide_review_sheet` in ordered batches of at most six, then use `get_slide_preview` only for
  a page needing closer inspection. Inspect every slide and every serious
  presenter candidate according to `visual-quality.md`. Correct content first, then regenerate the
  complete failed subset with concrete per-slide `slide_instructions`; do not blindly redraw.
  Re-inspect changed slides. After any content correction, call `get_run` and
  `get_authoring_snapshot` again before image regeneration; use that snapshot's revision.
- If the Agent cannot consume image content, continue from structured state without inventing
  observations. Record visual review as `not_performed`; this alone is not a publish blocker.

Use a reviewed replacement only when a human or vision-capable Agent genuinely reviewed the asset.

### 5. Configure and finish

The orchestrated path selects and validates the normal compatible presenter/Voice and completes
configuration. Use paginated `list_presenters`, `get_presenter_preview`, `select_presenter`, or
`update_course_configuration` only when the user supplied a concrete casting/layout requirement;
apply that choice at a review checkpoint before approving continuation.

After selection, re-read the run and authoring snapshot, then read configuration. Use
revision-checked `update_course_configuration` only for a requested layout change. Verify the
persisted presenter/Voice and layout values.

After the final Agent checkpoint, the server completes the stored grant-bounded target without
another Agent mutation:

- `draft`: leave unpublished;
- `private`: first-publish privately;
- `link`: first-publish, set link-only `unlisted`, and verify playability;
- `topics_review`: require explicit user intent and permission, link playability, then call
  submit the Topics review request. This does not approve distribution.

Never set direct platform-public visibility. Do not delete, transfer ownership, purchase credit,
republish an existing version, approve distribution, administer organizations, or use platform
administration through adjacent services.

## Preserve state and recover precisely

- Use one idempotency key for each new logical segment.
- Replay the same key only after an ambiguous response to the exact same payload.
- Never place two mutations back to back; complete the required fresh reads between them.
- Read fresh state before retry, advance, edit, upload reconciliation, image regeneration, config,
  publish, visibility, or review submission.
- Pass the current `expected_revision` to revision-bound operations.
- On a revision conflict, fetch a new snapshot and merge actual changes.
- Honor `Retry-After`; do not tight-loop or parallel-hammer one run.
- Use `retry_run` only when a fresh failed run allows `retry`.
- Use `cancel_run` cooperatively. `cancel_requested` is not terminal.
- Never modify durable run, source, image, project, or publication state outside declared MCP
  tools.

## Report completion evidence

Keep and return a secret-free record containing:

- course brief, knowledge mode, page count, requested and resolved target;
- run/project IDs and non-secret idempotency keys;
- source filenames, checksums, and canonical statuses;
- Outline and Page text/Narration review results and revision history;
- image readiness, visual-review status (`completed`, `partial`, or `not_performed`), corrections,
  and regenerated indexes;
- presenter/Voice and configuration evidence without invented identity claims;
- exact final run/checkpoint/publication/visibility/playability state;
- public and embed URLs only when the course reports `playable=true`;
- Topics review state only when requested.

Do not equate an allocated shell with a created project, queued images with image readiness, a
publish request with publication, or a slug with a playable course.
