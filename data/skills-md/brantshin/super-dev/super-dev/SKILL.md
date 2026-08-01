---
name: super-dev
description: Vendor-neutral engineering harness for coding, bug fixes, refactors, debugging, tests, releases, and other multi-step software work. Use when an agent should keep a lightweight spec, define a Done Contract, isolate changes, checkpoint risky actions, validate outcomes with proportionate evidence, preserve user work, and leave recoverable state.
---

# Super Dev

Treat engineering as a controlled event loop. Move the work forward autonomously inside the user's stated scope, while keeping goals, authority, evidence, and recovery explicit.

## Core contracts

- **Restate first**: Restate the requested outcome, boundaries, and acceptance conditions before substantial work.
- **Goal as loop anchor**: Keep one current goal. Re-align after new evidence, scope changes, failures, or interruptions.
- **Spec before non-trivial implementation**: Create or update the smallest durable spec that can preserve decisions, scope, risks, and the Done Contract.
- **Authority is scoped**: The user's request authorizes normal, reversible local work inside the stated scope. Obtain a fresh checkpoint before destructive actions, external mutations, deployments, data changes, credential flows, or material scope expansion.
- **Isolate implementation**: Preserve existing work. Prefer a dedicated worktree for non-trivial Git changes when the repository supports it.
- **Done means proven**: Mark work complete only when every Done Contract item has current, relevant evidence.
- **Reverse sync**: Write verified outcomes, deviations, risks, and recovery state back to the task record.
- **Knowledge has boundaries**: Keep task execution state separate from reusable project knowledge and private user or system memory.

## Operating loop

1. **Read the project contract**
   - Read repository instructions and the smallest relevant context slice.
   - Identify the implementation repository, current branch, dirty state, project profile, and validation expectations.
   - Do not ingest every file or repository by default.

2. **Restate the task**
   - State the outcome, in-scope and out-of-scope work, current assumptions, and what will prove completion.
   - Resolve only ambiguities that would materially change the implementation or risk.

3. **Choose a task mode**
   - `zero`: Purely mechanical, reversible, single-point changes with no design decision or external effect.
   - `fast`: Small change; use a micro-spec and focused validation.
   - `standard`: Default for multi-file implementation, ordinary bugs, and refactors.
   - `deep`: Ambiguous, cross-module, architectural, destructive, security-sensitive, or long-running work.
   - Upgrade the mode when scope, uncertainty, or risk grows.

4. **Create the control artifacts**
   - For `fast`, write a compact micro-spec.
   - For `standard` or `deep`, maintain a feature spec and a visible lifecycle todo.
   - Define a short Done Contract with one evidence source per required outcome.
   - Read [spec-contract.md](references/spec-contract.md) for artifact fields and topology.

5. **Checkpoint before risk**
   - Summarize the current goal, exact targets, next actions, validation, and principal risk.
   - Continue without redundant approval for ordinary local steps already authorized by the request.
   - Stop for new authority before high-impact or externally visible actions.
   - Read [safety-contract.md](references/safety-contract.md) for the risk classes.

6. **Isolate and implement**
   - Preserve unrelated dirty and untracked files.
   - For non-trivial Git work, use the recorded worktree and branch roles in [worktree-contract.md](references/worktree-contract.md).
   - Change only explicit files and objects.
   - Never use broad staging as a shortcut.
   - Do not guess commands, identifiers, environment names, or success states.

7. **Validate proportionately**
   - Start with the cheapest evidence capable of falsifying the change.
   - Escalate from static checks to tests, integration, runtime, deployment, or user-visible verification as required by the project profile and Done Contract.
   - Distinguish command success, deployment success, system behavior, and user outcome.
   - Read [evidence-contract.md](references/evidence-contract.md) before claiming completion.

8. **Close out**
   - Update the spec with changes, evidence, deviations, deployment state, remaining risks, and the next recovery action.
   - Keep the status active if any Done Contract item is missing or weakly evidenced.
   - Scan for reusable project knowledge, but write it only when the project topology and authorization allow it.
   - When the repository maintains an LLM Wiki, route verified reusable knowledge through the installed `llm-wiki` companion. Otherwise record a project-sync candidate without inventing a new knowledge topology.
   - Read [project-sync-boundary.md](references/project-sync-boundary.md) for the privacy and knowledge rules.

9. **Report**
   - Lead with the actual outcome.
   - Name the evidence that proves it and any requirement that remains open.
   - Include changed artifact paths and the smallest useful next step.
   - Never inflate a partial milestone into task completion.

## Project profiles

Let the repository define its own delivery and validation path. Classify the project before implementation:

- **Local-only**: Local checks can satisfy completion.
- **Remote service**: Completion normally requires deployed behavior or an explicit remote-validation waiver.
- **Library or package**: Require consumer-facing compatibility evidence appropriate to the change.
- **Data or infrastructure**: Treat writes, migrations, credentials, and shared-state changes as high impact.
- **Multi-repository**: Record the active repository and change scope; checkpoint before crossing repository boundaries.

Read [project-profile.md](references/project-profile.md) for the required profile fields and validation mapping.

## Knowledge companion

Treat long-term project knowledge as part of the engineering system, but keep it separate from the active task state. The optional `llm-wiki` companion can initialize, ingest, query, and lint a repository-owned Markdown Wiki.

Do not make ordinary engineering work depend on that companion. If it is unavailable, the repository has no approved Wiki root, or the content is private or unverified, leave a project-sync candidate in the task record instead of writing knowledge opportunistically.

## Extension boundary

Keep this skill vendor-neutral. A project may provide adapters for version control, CI, deployment, logs, traces, databases, configuration, messaging, or runtime routing. Adapters must satisfy the generic evidence and authority contracts without weakening them.

Read [extension-contract.md](references/extension-contract.md) when integrating project-specific tools.

## Stop conditions

Stop and report the exact gap when:

- the target, authority, or acceptance condition is materially ambiguous;
- the requested action becomes destructive, external, or broader than authorized;
- the repository baseline is unsafe or unrelated user work cannot be preserved;
- the implementation contradicts the current spec or project contract;
- required credentials, coordinates, or verified tool usage are unavailable;
- repeated validation fails without producing a new hypothesis;
- evidence cannot distinguish the new result from stale or unrelated state;
- a Done Contract item remains unverified.

## Reference map

- [spec-contract.md](references/spec-contract.md): Micro-spec, feature spec, Done Contract, and closeout fields.
- [safety-contract.md](references/safety-contract.md): Authority, mutation classes, privacy, and stop gates.
- [worktree-contract.md](references/worktree-contract.md): Dirty-state preservation, branch roles, integration, and retention.
- [evidence-contract.md](references/evidence-contract.md): Evidence levels, freshness, attribution, and completion rules.
- [project-profile.md](references/project-profile.md): Project classification and validation paths.
- [project-sync-boundary.md](references/project-sync-boundary.md): Task state, project knowledge, and commit/privacy boundaries.
- [extension-contract.md](references/extension-contract.md): Vendor-neutral provider interfaces.
