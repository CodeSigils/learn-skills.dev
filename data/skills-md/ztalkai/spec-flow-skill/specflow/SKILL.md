---
name: specflow
description: Author and govern authoritative Specs and the Project Glossary through the supported SpecFlow CLI.
compatible-cli: "@ztalkai/spec-flow-cli@0.1.0"
---

# SpecFlow

Use the official public CLI as the only SpecFlow operation boundary. Before any
authentication or resource command, check whether `specflow` is installed and, when
it is, run `specflow --version`.

- If `specflow` is not installed, run only this exact installation command. If
  installation fails, stop. Then run `specflow --version` again and require `0.1.0`:

```bash
npm install --global @ztalkai/spec-flow-cli@0.1.0
```

- If the installed version is different, stop and show the User that exact install
  command as the repair command. Do not run that repair command automatically or
  silently upgrade or downgrade an existing global installation.
- If the installed version is `0.1.0`, continue without running the install command or
  changing global state.
- Do not replace the pinned version with `latest`, a raw HTTP command, or a private
  copy. Do not update the Skill or CLI automatically.

Installing the Skill or CLI never starts authentication. Device Authorization remains
a separate, explicit User operation when SpecFlow access is actually needed.

Set the service origin once and use that same origin for authentication and every
resource command:

```bash
export SPEC_FLOW_API_URL="https://specflow.example"
specflow --server "$SPEC_FLOW_API_URL" auth login
specflow project list
```

The resulting independently revocable CLI Session belongs to the User. It carries
that User's current Role only within its approval-time Project scope. Always pass an
explicit `--project-id` after Project Creation or Discovery. Do not register an Agent
identity or request an Agent grant.

## Operating contract

- Use `specflow project list` before choosing a Project; never infer a hidden current
  Project.
- Archive or Restore only when the User's task requires that lifecycle change. Pass
  the opaque version returned by Project discovery or context, and reread deliberately
  after `Resource Changed` or an ambiguous transport outcome.
- Use the singular resource commands shown by `specflow --help`. Success is one JSON
  object on stdout. Diagnostics and the final Skill Error are NDJSON on stderr.
- Organize Capability and Spec resources, persist only bounded Source References, and
  edit Spec or Glossary Working Drafts through the logical CLI commands. Do not
  implement a collaboration protocol or connect to the collaboration gateway.
- Use `proposal create-spec` or `proposal create-glossary` only when preview-before-apply
  is useful. Bind it to the exact logical baseline you read, report only available
  Agent revision/model and Source Reference IDs, and use `proposal list`, `apply`, or
  `discard` as independent resource operations. Direct `spec edit` and `glossary edit`
  remain the default and may report the same bounded provenance fields.
- Treat `Resource Changed` from Proposal apply as a protected Human edit: reread the
  Working Draft and Proposal, then require deliberate conflict resolution. Never
  convert it into a blind direct edit or silently recreate the Proposal.
- Apply the current Project Role to Finding and Membership operations. Never attempt
  to turn a Permission Denied result into broader authority.
- Before any Spec Publish or Rollback, request explicit User confirmation immediately before
  invoking the command. Apply the same rule before any Glossary Publish or Rollback.
  The CLI accepts no confirmation proof: never claim that SpecFlow verified or recorded confirmation.
- Read external sources with the Agent's own authorized tools. You must never request, read, or store external source credentials in SpecFlow, and do not send external source bodies to SpecFlow.
- Perform one resource operation at a time. The Skill is not a task workflow,
  orchestration service, or durable Agent session.

## Stable failure recovery

Handle the final `error.reason` exactly:

- `Authentication Failed`: stop and ask the User to authenticate again.
- `Project Not Accessible`: stop; do not probe the Project with another identifier.
- `Permission Denied`: stop; the current User Role does not allow the operation.
- `Resource Not Found`: reread the selected Project directory or resource identity.
- `Resource Changed`: reread the resource before deliberately reapplying the User's
  intent with its new opaque version.
- `Invalid Operation`: correct the domain input; never auto-restore, auto-publish, or
  bypass the stated rule.
- `Temporary Failure`: retry only when `retryable` is true, and honor `retryAfter` when
  present.

Disabled Users, revoked or expired Sessions, Role downgrade, Project Archive, and
stale expected versions are authoritative current-state failures. Do not reuse cached
authority or silently broaden the Session's Project scope.
