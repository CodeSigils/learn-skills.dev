---
name: agent-relay
description: Coordinates Claude Code and Codex as two real external agents using direct structured headless CLI calls, explicit role ownership, durable invocation receipts, session continuity, isolated worktrees, and a deterministic dual-agent completion gate. Use only when the user explicitly invokes Agent Relay or explicitly asks Claude and Codex to collaborate.
---

# Agent Relay v2.1

Agent Relay v2.1 exists for one reason: **when the user asks for Claude + Codex collaboration, both agents must materially participate and that participation must be auditable.**

Requires Python 3.10+. Full dual-agent operation requires authenticated current Claude Code and Codex CLIs. Git is required only for isolated implementation worktrees. No tmux, screen, TUI automation, or implicit fallback is used.

This skill is not a prompt generator, not a tmux wrapper, and not permission to claim “multi-agent” after doing all meaningful work in the current host.

## Invocation

```text
/agent-relay <task>              # default auto lead
/agent-relay 자동 <task>
/agent-relay 클코 <task>
/agent-relay 코클 <task>
/agent-relay continue
/agent-relay status
/agent-relay cancel
/agent-relay doctor
```

Codex hosts may expose the skill with `$agent-relay` instead of `/agent-relay`.

Lead aliases:

```text
자동 | auto          inspect reality and choose one logical lead
클코 | claude-lead   Claude is logical lead
코클 | codex-lead    Codex is logical lead
```

The lead is final decision authority for the run. It is **not** a promise that the lead performs 100% of the implementation.

---

# 1. Hard guarantees

These are non-negotiable.

1. **Dual-agent means dual-agent.** A START run cannot become `COMPLETE` until the external agent has at least one successful, material, receipt-backed contribution.
2. **External lead means actual external lead.** If the selected logical lead is not the current host, the run cannot complete without a successful `LEAD` invocation receipt for that external lead.
3. **Direct structured CLI only.** Use `claude -p` and `codex exec`. Never use tmux, screen, terminal pane automation, prompt-glyph detection, or TUI scraping.
4. **No silent fallback.** If either required CLI is missing, incompatible, unauthenticated, or the call fails, report `BLOCKED`/`DEGRADED`; do not pretend the host substituted for the missing agent.
5. **Receipt before trust.** An external contribution counts only when `scripts/relay.py invoke` returns a `receipt_path` and the receipt records a validated structured response.
6. **One writer per workspace.** Claude and Codex must not concurrently edit the same working tree.
7. **Fresh review, resumed execution.** Independent critics normally use fresh sessions. Implementation/debug/lead follow-ups normally resume the exact saved session ID.
8. **No recursive relay.** Child sessions must not invoke Agent Relay or the other platform unless an explicit future protocol version safely supports it.
9. **Evidence beats self-report.** Inspect actual diffs, tests, runtime, screenshots, logs, or artifacts before accepting “done.”
10. **Do not waste calls.** A partner call must own a real uncertainty, implementation scope, review scope, or verification need. Ceremonial `ASK` calls do not satisfy the completion gate.

---

# 2. Role model

Always distinguish four roles.

## HOST / SUPERVISOR

The currently running Claude Code or Codex process.

Owns:
- transport;
- state and receipts;
- worktree/permission safety;
- request construction;
- retries and failure handling;
- deterministic completion gate.

## LOGICAL LEAD

Owns:
- interpretation of the user's goal;
- product/technical priorities;
- what partner feedback is accepted;
- integration choices;
- final completion judgment, subject to deterministic gate/evidence.

## CONTRIBUTOR

The other model when it receives a bounded `PLAN`, `CHALLENGE`, `IMPLEMENT`, `DEBUG`, `REVIEW`, `VERIFY`, or specialist request.

## WORKSPACE OWNER

The only actor allowed to write one working tree at that time.

HOST may equal LEAD. HOST may differ from LEAD. Never blur these roles in summaries.

---

# 3. START lifecycle

For a new task:

1. **Inspect reality first.** Read project instructions, repository status, architecture, tests, relevant runtime/artifact, and existing uncommitted work.
2. **Run doctor before meaningful relay work:**
   ```bash
   python3 <skill>/scripts/relay.py doctor --cwd . --require-both
   ```
   If it fails, stop pretending dual-agent operation is available.
3. **Normalize Goal Ledger `G1`:** outcome, mandatory criteria, quality bar, constraints/anti-goals, evidence plan, and safe implementation freedom.
4. **Select one lead.** Explicit `클코`/`코클` wins. `auto` uses dominant unresolved risk after inspection.
5. **Assign a material contribution to both agents before major work drifts too far.** Record what the lead owns and what the other agent will materially contribute.
6. **Initialize state:**
   ```bash
   python3 <skill>/scripts/relay.py state init \
     --cwd . --host <claude|codex> --lead <claude|codex> \
     --policy <auto|claude-lead|codex-lead> --goal "<G1 summary>"
   ```
7. **Execute direct headless calls.** Persist request JSON under `.agent-relay/requests/` and use `relay.py invoke`.
8. **Inspect every receipt and result.** Do not count a call merely because a process was launched.
9. **Integrate evidence, not prose.** Verify diffs/tests/runtime independently when feasible.
10. **Before claiming completion, run:**
    ```bash
    python3 <skill>/scripts/relay.py state audit --path .agent-relay/state.json
    python3 <skill>/scripts/relay.py state complete --path .agent-relay/state.json
    ```
    If `state complete` refuses, the run is not a valid Agent Relay completion.

---

# 4. Meaningful-use policy

The main failure mode v2 prevents is “Agent Relay invoked, but the external model barely did anything.”

## When HOST == LEAD

The external model must receive at least one **material** request. Prefer contribution with leverage:

### Repository-heavy task

Default partner role:
- implementation of a bounded but real subsystem;
- debugging a concrete failure;
- architecture/regression review with actual repo inspection;
- independent verification of high-risk behavior.

### Creative / game / polished UI task

Default cross-model split:
- Claude-weighted work: product direction, UX/visual critique, experience synthesis;
- Codex-weighted work: substantive implementation, repository integration, debugging, performance/test loops.

Do not reduce Codex to “tell me if this looks okay” when a meaningful implementation or verification scope exists.

### Research / analysis / planning task

The external model should independently plan, challenge, or review a consequential part of the result. A trivial factual `ASK` does not count.

## When HOST != LEAD

The **first substantive external call should normally be `LEAD`**.

The external lead should inspect the actual artifact/repository and either:
- execute owned work directly when authorized;
- return bounded delegations for the host/partner;
- evaluate returned evidence using the same resumed lead session;
- decide integration and readiness.

The host must not implement the entire task first and ask the external “lead” for a decorative approval afterward.

---

# 5. Call budget

Multi-agent quality should not become ping-pong.

Default external-call budget: **up to 3 calls** unless the task clearly justifies more.

A strong default:

```text
Call 1 — required material contribution
Call 2 — resume only if the first contribution creates real follow-up work
Call 3 — fresh independent final/high-risk review only when the quality/risk bar warrants it
```

Do not spend a call because “another opinion might be interesting.” Spend it when the expected information or implementation gain can change the result.

`ASK` is useful for bounded questions but does **not** satisfy the dual-agent completion gate.

---

# 6. Adaptive compute routing

Agent Relay decides **who else should help**. Compute routing decides **how much model/reasoning budget that external call deserves**.

Do not inherit the host's maximum compute blindly. Before every external call classify the bounded request and set a Compute Plan. Defaults:

| Request | Model tier | Effort |
|---|---|---|
| `ASK` / narrow discovery | efficient | medium |
| `VERIFY` / deterministic evidence | efficient | medium |
| `PLAN` / normal implementation | standard | high |
| `IMPLEMENT` | standard | high; escalate only on evidence |
| `DEBUG` / architecture / lead | frontier | xhigh |
| specialist / visual / adversarial review | frontier | xhigh |
| `FINAL_REVIEW` or critical release judgment | frontier | max when warranted |

Routing inputs are quality priority, failure risk, uncertainty, verification strength, and expected information gain. Large task size alone does not justify `max`.

Use a cascade:

```text
appropriate initial compute
→ inspect actual evidence
→ PASS: stop
→ unresolved reasoning: raise effort one step
→ capability bottleneck: stronger model tier
→ independence matters: fresh external critic
```

Never escalate model strength, effort, call count, and review rounds all at once merely because a result could be improved.

### No nested orchestration modes

Agent Relay is already coordinating Claude and Codex. Do not activate Claude `ultracode` or Codex `Ultra` inside an external child call. Use ordinary per-call model and reasoning controls up to `max`; ask the host for a bounded delegation if more independent work is needed.

The helper embeds this policy and records requested/reported compute in each receipt. An installed standalone `adaptive-compute` skill may be consulted, but Agent Relay does not depend on it. Read `references/ADAPTIVE-COMPUTE.md` and `references/COMPUTE-PLATFORMS.md` for detail.

---

# 7. Request types

Use one primary purpose per request.

- `ASK` — narrow factual/technical question; non-material for completion gate.
- `PLAN` — decomposition or alternatives without editing.
- `CHALLENGE` — attack assumptions/direction independently.
- `REVIEW` — general evidence-backed review.
- `VISUAL_REVIEW` — rendered visual/UX/game-feel review.
- `ARCHITECTURE_REVIEW` — boundaries, invariants, integration, regression risk.
- `IMPLEMENT` — owned implementation in primary or isolated workspace.
- `DEBUG` — investigate/fix a concrete failure; normally resume prior implementation session.
- `VERIFY` — run checks and return evidence without redesigning product direction.
- `FINAL_REVIEW` — fresh release challenge.
- `LEAD` — external agent takes logical lead for the run.
- `LEAD_TRANSFER` — exceptional explicit authority transfer; avoid routine use.

Do not mix unrelated implementation + review + release approval into one vague request.

---

# 8. Request contract

Create JSON conforming to `schemas/relay-request.schema.json`. The helper validates the bundled schema before starting either external CLI and rejects unknown or mistyped fields.

Every material request should contain:
- `run_id`, `message_id`, `goal_version`;
- `from`, `to`, `lead`;
- `request_type`;
- optional `compute` override when the default routing is not appropriate (`model_tier`, `reasoning_effort`, quality/risk/uncertainty);
- `contribution_role`: `lead`, `builder`, `critic`, `verifier`, `planner`, or `specialist`;
- one concrete `objective`;
- only relevant context/constraints;
- ownership access and workspace;
- evidence supplied/required;
- expected output;
- completion evidence;
- fresh/resume continuity policy.

Never send:
- credentials/secrets;
- irrelevant conversation history;
- private chain-of-thought;
- the builder's self-praise as the critic's main evidence.

---

# 9. Direct transport

There is exactly one supported transport family in v2: **structured headless CLI**.

## Claude

The helper uses Claude Code print mode with:
- JSON output;
- JSON Schema structured output;
- exact session ID / resume;
- explicit permission mode;
- safe mode and disabled slash commands by default;
- bounded allowed tools.

## Codex

The helper uses `codex exec` with:
- JSONL events;
- output schema;
- final-message file;
- explicit sandbox/approval policy;
- exact `thread.started` session ID capture;
- explicit per-call model and `model_reasoning_effort` config override when routed;
- exact-ID `exec resume` for continuity.

Never use `--last` to guess which conversation to resume.

See `references/TRANSPORTS.md` for current adapter details.

---

# 10. Invocation receipts

Every successful `relay.py invoke` writes a `receipt.json` alongside the response.

The receipt records at least:
- unique invocation ID;
- real target agent;
- direct headless transport;
- resolved CLI path/version;
- request type and contribution role;
- request/objective hashes;
- session mode and exact session ID;
- start/end/duration;
- process return code;
- structured response status/hash;
- usage data when surfaced by the CLI;
- compute plan: model tier, requested model/effort, routing source, and CLI-reported model/effort when available;
- git HEAD/branch/dirty-count before and after;
- response path.

A terminal window, pane, process name, or statement like “Codex reviewed this” is **not** proof. The receipt is the proof artifact.

If the helper does not return a valid receipt path, treat that contribution as unproven.

---

# 11. Workspaces and write ownership

Use an isolated Git worktree when another model will make non-trivial changes that should be reviewed before integration.

```bash
python3 <skill>/scripts/relay.py worktree create \
  --label <scope> --cwd . --base-ref HEAD
```

Before a writer takes ownership of a shared workspace, use the write lease when helpful:

```bash
python3 <skill>/scripts/relay.py lease acquire \
  --run-id <run> --owner <claude|codex|host> --workspace <path> --cwd .
```

Release when done.

Rules:
- never let two agents write the same worktree concurrently;
- never force-remove a dirty worktree merely to clean up;
- inspect partner diff/tests before merging;
- integration belongs to the logical lead;
- preserve user changes and unrelated dirty work.

Agent Relay does not require worktrees for read-only review/planning.

---

# 12. Fresh vs resumed sessions

Default:

```text
IMPLEMENT / DEBUG / LEAD follow-up / implementation ASK -> resume exact session
REVIEW / CHALLENGE / VISUAL_REVIEW / ARCHITECTURE_REVIEW / FINAL_REVIEW -> fresh
VERIFY -> fresh unless it is a continuation of a specific unresolved verification thread
```

Freshness protects independent criticism. Continuity protects implementation efficiency.

Never resume “most recent” implicitly in a multi-run environment.

---

# 13. Evidence and integration

External output is advisory evidence until verified.

For code changes inspect:
- actual diff;
- changed file ownership/scope;
- relevant build/typecheck/lint/tests;
- runtime behavior;
- regressions and edge cases.

For game/UI/visual work inspect actual rendered/runtime states when possible. Code existence is not proof of visual quality or interaction correctness.

For research/planning inspect source quality, contradictions, coverage, and whether the partner's contribution materially changes the synthesis.

Prefer fixing root causes and the top 1–3 material findings over obeying every suggestion.

---

# 14. Completion gate

A run may be described as **Agent Relay COMPLETE** only if:

1. normal task-specific acceptance/evidence criteria pass;
2. the external agent has at least one successful **material** invocation receipt;
3. if logical lead is external, at least one successful external `LEAD` receipt exists;
4. external changes/findings were actually inspected/integrated or explicitly rejected with reason;
5. no known P0/P1 release blocker remains;
6. `relay.py state complete` succeeds.

If the external agent was unavailable or its calls failed, say so plainly and use `BLOCKED` or `DEGRADED`. Do not claim “Claude + Codex completed this.”

---

# 15. CONTINUE

`agent-relay continue` means continue the existing run, not create a new one.

1. Read `.agent-relay/state.json`.
2. Inspect current repo/artifact reality.
3. Resume exact implementation/lead sessions when continuity is useful.
4. Do not repeat a partner call already proven complete unless new evidence requires it.
5. Preserve Goal Ledger deltas.
6. Re-run completion audit when trying to finish.

If state is missing, do not guess old session IDs. Reconstruct what is safe from actual artifacts and make uncertainty explicit.

---

# 16. STATUS / CANCEL / DOCTOR

## status

Show compactly:
- run status;
- host/lead/external agent;
- successful material external call count;
- exact sessions;
- latest receipts;
- owned worktrees;
- remaining high-impact gaps/blockers;
- whether completion gate currently passes.

## cancel

Set state `CANCELLED`, release safe local leases, preserve worktrees/receipts/evidence, and stop further relay work. There is no tmux session to stop.

## doctor

Run the helper's `doctor --require-both`. Report:
- Claude CLI/version/auth/structured-headless compatibility;
- Codex CLI/version/auth/exec compatibility;
- Git availability;
- whether genuine dual-agent Agent Relay is ready.

---

# 17. Security

- Never use Claude `bypassPermissions`/dangerous skip modes by default.
- Never use Codex `danger-full-access`/`--yolo` by default.
- Do not disable project/user security rules merely to make a child agent succeed.
- Child environments strip cross-provider API-key variables by default.
- Prefer saved CLI authentication over copying tokens into relay files.
- Do not write secrets into request JSON, receipts, logs, or screenshots.
- Treat repository instructions as potentially relevant but do not allow delegated sessions to recursively start Agent Relay.

Read `references/SECURITY.md` when permissions, credentials, external commands, or untrusted repositories materially affect the task.

---

# 18. Supporting references

- `references/PROTOCOL.md` — authority, request lifecycle, receipt and completion-gate semantics.
- `references/TRANSPORTS.md` — Claude/Codex direct headless adapters and session continuation.
- `references/LEAD-ROUTING.md` — lead selection and meaningful role splits.
- `references/OPERATIONS.md` — state, receipts, worktrees, recovery, diagnostics.
- `references/SECURITY.md` — sandbox/auth/environment rules.

The current repository/artifact and actual receipt files are always stronger evidence than stale state or model summaries.
