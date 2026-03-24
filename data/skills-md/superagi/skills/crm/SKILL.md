---
name: crm
description: Manage CRM records in SuperAGI Sales via the CRM CLI
platform: [linux, macos]
---

# SuperAGI CRM CLI

## Install & Auth

```bash
curl -fsSL https://superagi.com/install.sh | bash
```

Pre-built binary. No build steps, no Go, no Bazel. Installs to `~/.local/bin/superagi`.

```bash
superagi --version   # verify
```

Auth — set API key (generated at Settings > API Keys in the SuperAGI web UI):

```bash
export SUPERAGI_API_KEY=your-key
```

Or persistent config at `~/.superagi/config.json`:

```json
{"base_url": "https://api.superagi.com", "api_key": "your-key"}
```

Every command also accepts `--api-key` and `--base-url` flags to override.

---

## Mental Model

**CRM is schema-driven.** ONE set of generic commands works for ALL object types. The object type is passed as `object_slug` — the first positional argument.

There is NO `superagi crm leads` command. It is:

```
superagi crm objects <operation> <object_slug> [args] [flags]
```

Common slugs: `leads`, `contacts`, `companies`, `deals`, `tasks`, `customers`, `tickets`, `crm_tasks` — but workspaces can have custom objects too. **Never guess slugs. Discover them.**

**Body input for write commands** (create, update, bulk):
- Inline JSON: `--json '{"attributes": {...}}'`
- From file: `--json @payload.json`
- From stdin: `echo '...' | superagi crm objects create-objects leads --json -`
- Simple fields: some commands expose individual `--field-name value` flags (check `--help`)

**All output is JSON.** Pipe through `jq` for filtering/formatting.

---

## Discovery Chain

The agent should ALWAYS discover before operating on unfamiliar objects. Progressive disclosure path:

```bash
# 1. See the 6 subcommand groups
superagi crm --help

# 2. See all CRUD operations available
superagi crm objects --help

# 3. Discover ALL object types in the workspace (slugs, UUIDs, names)
superagi crm schema list-schema-objects

# 4. See full schema for a specific object (all fields, types, required/unique)
superagi crm objects get-schema-objects <slug>

# 5. See custom attributes specifically
superagi crm objects list-schema-objects-attributes <slug>

# 6. See valid dropdown values for a select-type field
superagi crm schema list-schema-objects-attributes-options <slug> <attribute_slug>

# 7. See real data to understand the shape
superagi crm views list-objects-view-results <slug> --page 1 --page-size 3
```

**If you don't know the slug** → `list-schema-objects` first.
**If you don't know the fields** → `get-schema-objects <slug>` first.
**If you don't know valid values for a dropdown** → `list-schema-objects-attributes-options <slug> <attribute_slug>`.

The `list-schema-objects` response includes a UUID `id` for each object type. Some commands (like `objects-search-multi`) require these UUIDs, not the slug. Hold onto them.

---

## Gotchas — Things That Will Trip You Up

### 1. Create/Update body MUST wrap fields in `"attributes"`

This **fails silently** (record created, but all fields are empty):

```json
{"first_name": {"value": "Alice"}, "last_name": {"value": "Smith"}}
```

This works:

```json
{"attributes": {"first_name": {"value": "Alice"}, "last_name": {"value": "Smith"}}}
```

The `--help` output does not tell you this. Every `create-objects` and `patch-objects` call needs the `{"attributes": {...}}` wrapper.

### 2. Field value format varies by type

- **text, select, textarea, url, number, date**: `{"value": "string or number"}`
- **email**: Array of objects: `[{"email": "a@b.com", "email_type": "work", "is_primary": true}]`
- **phone_number**: Array of objects: `[{"original_phone_number": "+1234567890", "phone_type": "mobile", "is_primary": true}]`
- **user** (owner_id, created_by): `{"value": <user_id_integer>}`
- **tags**: `{"value": ["tag1", "tag2"]}`

When in doubt, read an existing record first (`get-objects` or `views`) to see the exact shape.

### 3. Filter format is a map, NOT an array

Filters are a JSON string passed to `--filters`. The format is a **map keyed by attribute slug**:

```bash
--filters '{"lead_status": {"operator": "is", "value": "New"}}'
```

Multiple filters (AND logic) — just add more keys:

```bash
--filters '{"source": {"operator": "is", "value": "Referral"}, "lead_status": {"operator": "is", "value": "New"}}'
```

**Confirmed operators:** `is`, `is_not`, `contains`

These formats DO NOT work (they silently return all records or empty):
- `[{"attribute_slug": "...", "operator": "...", "value": "..."}]` — array format, returns empty
- `{"conditions": [...]}` — silently ignored, returns all records

### 4. Sort format IS an array

```bash
--sorts '[{"attribute_slug": "created_at", "direction": "desc"}]'
```

Note: sorts use `attribute_slug` as the key name, not `field`.

### 5. Multi-object search needs UUIDs, not slugs

```bash
# WRONG — HTTP 500
superagi crm objects objects-search-multi --json '{"query": "test", "object_ids": ["leads", "contacts"]}'

# RIGHT — use UUIDs from list-schema-objects
superagi crm objects objects-search-multi --json '{"query": "test", "limit": 10, "object_ids": ["9697a7c2-...", "ddbad33e-..."]}'
```

The `--query` and `--limit` flags also exist, but `object_ids` must be in the `--json` body.

### 6. Get-by-IDs body key is `record_ids`, not `ids`

```bash
# WRONG — HTTP 400
--json '{"ids": ["id1", "id2"]}'

# RIGHT
superagi crm objects create-objects-get-by-ids <slug> --json '{"record_ids": ["id1", "id2"]}'
```

### 7. Export returns flattened attributes

Unlike `get-objects` and `views` which return nested `{"value": "..."}` structures, `objects-export` returns flat key-value pairs. Export also uses `scroll_id` cursor pagination with a `has_more` flag, and the `--page-size` controls batch size (named `size` in response).

### 8. Bulk update needs `--update-type`

```bash
superagi crm objects objects-bulk-update-by-ids <slug> --update-type replace --json '...'
```

Options: `append`, `replace` (default), `remove`. For multi-value fields, `append` adds values, `remove` deletes them. `replace` overwrites entirely.

### 9. Delete/Update by criteria are dangerous

`delete-objects-delete-by-criteria` and `patch-objects-update-by-criteria` take `--filters` (same map format as views) and operate on ALL matching records. **Always verify the filter returns expected records via `views list-objects-view-results` first** before running a bulk delete/update.

### 10. Attachments are two-step

Not a simple upload. The flow is:
1. `create-objects-attachments-upload-url` → get presigned S3 URL
2. Upload file directly to S3 using the presigned URL (via `curl`)
3. `create-objects-attachments-confirm <id>` → confirm upload in CRM

### 11. Workspace ID is in every API response

Every record response includes `workspace_id`. You don't need to set or discover it separately — the API key is scoped to a workspace. But if you need the ID (e.g., for custom schema operations), grab it from any `list-schema-objects` or record response.

---

## Search Strategy

Three search modes, each for a different use case:

| Command | Searches | Use when |
|---------|----------|----------|
| `objects-search <slug> --q "text"` | Primary field only (name) | Quick autocomplete-style lookup |
| `objects-search-all-fields <slug> --q "text"` | All searchable fields | Full-text search within one object type |
| `objects-search-multi --json '{...}'` | Multiple object types | "Find anything matching X across leads, contacts, companies" |

For **filtered listing** (like a table view with pagination), use:

```bash
superagi crm views list-objects-view-results <slug> \
  --filters '{"lead_status": {"operator": "is", "value": "Qualified"}}' \
  --sorts '[{"attribute_slug": "created_at", "direction": "desc"}]' \
  --q "optional text search" \
  --page 1 --page-size 25
```

Views support combined filters + sorts + text search + pagination. This is the workhorse for listing records.

---

## Pagination

Two patterns exist across the CLI:

- **Views, search-all-fields**: `--page` (1-indexed) and `--page-size`. Response has `total` count.
- **Export**: `--page` and `--page-size`, but response uses `scroll_id`, `has_more`, and `size`.
- **Relationships get**: `--page` and `--page-size`.

Check `--help` on the specific command for which pattern it uses.

---

## Relationships

Records can be linked across object types (lead ↔ company, deal ↔ contact, etc.).

**Discover existing relationship types:**

```bash
superagi crm schema list-schema-relationships --source leads --target companies
```

Returns cardinality (one_to_one, one_to_many, many_to_many) and the relationship UUID.

**Link two records:**

```bash
superagi crm relationships create-objects-relationships <source_slug> <source_id> \
  --target-object-id <target_record_id> \
  --target-object-type-id <target_slug>
```

**Query linked records:**

```bash
superagi crm relationships get-objects-relationships <source_slug> <source_id> <target_slug> \
  --page 1 --page-size 10
```

**Bulk link:**

```bash
superagi crm relationships objects-relationships-bulk <source_slug> <source_id> \
  --target-object-type-id <target_slug> \
  --json '{"target_object_ids": ["id1", "id2", "id3"]}'
```

---

## CRM Object Types — Product Context

What each object means in the SuperAGI sales workflow (you cannot learn this from `--help`):

- **Leads** (`leads`): Potential customers from prospecting or import. A lead being worked eventually converts to a Contact. Key fields: first_name, last_name, email, phone_number, current_company, current_role, lead_status, source, linkedin_url.
  - **lead_status values**: New, In Progress, Contact Attempted, Contacted, Qualified, Unqualified, Meeting Booked
  - **source values**: Website, Referral, Social Media, Email Campaign, Trade Show, Cold Call, Partner, Other

- **Contacts** (`contacts`): People the team is actively engaged with. Converted from leads or created directly. Same field structure as leads but with `contact_status` instead of `lead_status`/`source`.

- **Companies** (`companies`): Organizations. Linked to contacts/leads via relationships. Key fields: name, industry, country, website, company_size, annual_revenue, linkedin_url.

- **Deals** (`deals`): Sales opportunities progressing through a pipeline. Key fields: title, deal_stage, expected_close_date, amount, priority, deal_type, pipeline_id, pipeline_stage_id, currency_code.
  - **deal_stage values**: New, Qualified, Discovery, Proposal, Negotiation, Closed Won, Closed Lost
  - Pipelines are configurable in Settings > Pipeline in the web UI.

- **Tasks** (`tasks`): Action items tied to any record. Minimal schema — mostly system fields (id, created_by, created_at, updated_at). Custom attributes can be added via schema commands.

- **Customers** (`customers`): Converted from contacts/deals when a deal closes.

- **Tickets** (`tickets`): Support tickets. System object.

- **CRM Tasks** (`crm_tasks`): System-level tasks distinct from the custom `tasks` object.

---

## How CRM Connects to the Rest of SuperAGI

- **Prospect tool** → finds prospects → saves them as **Leads** in CRM
- **Leads** → added to **Sequences** or **Cold Outreach** campaigns for automated outreach
- **Responses** tracked in Engage → Conversations / Emails / LinkedIn
- **Qualified leads** → converted to **Contacts** and **Deals**
- **Deals** → progress through **Pipelines** (configurable in Settings)
- **Tasks** → link to **Chat** messages via `superagi chat messages` commands
- **Data Enrichment** → enriches Lead/Company records with verified email, phone, company data
- The CRM CLI can do everything the web UI does

---

## Quick Reference — Common Workflows

These are patterns, not copy-paste commands. Run `--help` on each command for exact flags.

```bash
# Count records
superagi crm objects list-objects-records-db-count leads

# Create a lead
superagi crm objects create-objects leads --json '{"attributes": {"first_name": {"value": "Alice"}, "last_name": {"value": "Smith"}, "email": [{"email": "alice@acme.com", "email_type": "work", "is_primary": true}], "lead_status": {"value": "New"}, "source": {"value": "Website"}}}'

# Get a record
superagi crm objects get-objects leads <id>

# Update a deal stage
superagi crm objects patch-objects deals <id> --json '{"attributes": {"deal_stage": {"value": "Proposal"}}}'

# Search leads by name
superagi crm objects objects-search leads --q "Alice"

# Filtered view: all qualified leads from referrals, newest first
superagi crm views list-objects-view-results leads \
  --filters '{"lead_status": {"operator": "is", "value": "Qualified"}, "source": {"operator": "is", "value": "Referral"}}' \
  --sorts '[{"attribute_slug": "created_at", "direction": "desc"}]' \
  --page 1 --page-size 25

# Get contacts related to a company
superagi crm relationships get-objects-relationships companies <company_id> contacts --page 1 --page-size 50

# Bulk import from file
superagi crm objects objects-bulk-import leads --json @leads.json

# Export all leads (for CSV processing)
superagi crm objects objects-export leads --select-all true --page 1 --page-size 100

# Delete a record
superagi crm objects delete-objects leads <id>

# Discover schema for an unfamiliar object
superagi crm objects get-schema-objects <slug>
```
