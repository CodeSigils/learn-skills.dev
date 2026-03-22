---
name: agent-security-audit
description: "Audits AI agent projects for security risks in prompts, tools, memory, RAG, and permissions. Use when: the user asks to review agent security, harden an agentic system, check for prompt injection risks, audit tool permissions, or secure an AI assistant before deployment. Do NOT use for: projects with no agentic components, runtime red teaming, or exploit generation."
---

# Agent Security Audit

Security audit skill for AI agent projects. Scans your agentic codebase for
AI agent risks — prompt injection, tool abuse, memory poisoning, RAG vulnerabilities,
permission sprawl, and multi-agent trust gaps — then interprets findings in context and
delivers a structured report with actionable mitigations aligned to OWASP LLM Top 10.

## Workflow

Copy this checklist and track progress:

```
Audit Progress:
- [ ] Step 1: Run the static audit script
- [ ] Step 2: Review the project profile and agentic level
- [ ] Step 3: Filter false positives using project context
- [ ] Step 4: Classify real risks vs. weak signals
- [ ] Step 5: Read the report template and write the report
```

**Step 1: Run the audit script**

Run the [audit script](./scripts/agent_security_audit.py) on the target project.
Requires **Python 3.10+** (stdlib only, no dependencies).

```bash
python ./scripts/agent_security_audit.py <project-path> --format json
```

Options:

- `--format json` for structured output, `--format text` for human-readable
- `--json <output-file>` to save the JSON report to a file
- `--exclude <dir1,dir2>` to skip directories (e.g. `--exclude node_modules,.venv`)
- `--max-file-size <bytes>` (default: 1500000)

Exit codes:

- `0` — No critical or high severity findings
- `1` — Critical or high severity findings detected
- `2` — Error (e.g. target path does not exist)

**Step 2: Review the project profile**

The script returns JSON with `profile.agent_context` showing:

- `agentic_level`: how agentic the project is (high/medium/low)
- `frameworks_detected`: which agent frameworks are used
- `signals_detected`: what agentic patterns exist (prompts, tools, memory, RAG)

Use this to understand the agent's architecture before evaluating findings.

**Step 3: Filter false positives**

The script uses heuristics. Treat findings as signals, not verdicts. Filter out:

- Generic code patterns that are safe in context (e.g. `open()` for config files)
- Patterns in test files or documentation
- Framework internals that are expected behavior

**Step 4: Classify real risks**

For each remaining finding, determine:

- Is this a real risk, potential concern, or weak signal?
- What is the blast radius if exploited?
- Does the current architecture already mitigate it?

Consult [reference/owasp-llm-top-10.md](reference/owasp-llm-top-10.md) to map
each finding to the corresponding OWASP LLM risk (LLM01–LLM10).

**Step 5: Write the report**

Read the [report template](./report-template.md) and follow its structure
exactly for the final report. Every section and table format defined in the
template must appear in the output.

Before writing, review [examples/sample-output.json](examples/sample-output.json)
to calibrate the expected tone, detail level, and structure.

## Agent-specific risks to prioritize

Focus on these over generic code issues:

- **Prompt injection**: external content reaching system prompts without boundaries
- **Tool abuse**: tools with write/delete/execute lacking validation or confirmation
- **Memory poisoning**: persistent memory written without sanitization
- **RAG injection**: retrieved content injected into prompts without delimiters
- **Output trust**: model output consumed as instructions without validation
- **Permission sprawl**: agent with broader tool access than needed
- **Missing human-in-the-loop**: destructive operations without confirmation
- **Multi-agent trust**: one agent delegating to another without boundary checks

## Large projects

When the target project is large, the JSON output may exceed practical context
limits. Use these strategies:

**Triage before full scan**

1. Run the script first to get the JSON output.
2. Check `summary.total`. If findings exceed ~50, focus the report on
   `critical` and `high` severity findings only. Mention the medium/low
   count but don't enumerate them.
3. If the output is still too large, re-run with `--exclude` to skip
   non-core directories (e.g. `--exclude tests,docs,examples,scripts`).

**Prioritization heuristic**

- Focus on `production` context findings. Deprioritize `test`, `docs`, and
  `example` context unless the user specifically asks about them.
- Agent-specific rules (`AGT*`) are more valuable than general rules (`SEC*`,
  `H*`). When trimming, keep `AGT*` findings and summarize the rest.
- If multiple findings share the same `rule_id` and `category`, group them
  ("AGT001 found in 12 files") instead of listing each one.

**Splitting the audit**

For monorepos or projects with multiple agents, audit each agent directory
separately rather than scanning the whole repo at once:

```bash
python ./scripts/agent_security_audit.py <project-path>/agent-a --format json
python ./scripts/agent_security_audit.py <project-path>/agent-b --format json
```

Merge the profiles and findings in the report, noting which agent each one
belongs to.

## Architecture review (no source files)

If the project source is not available, perform a conceptual review based on the
architecture described by the user. Ask about: which tools the agent has, how
prompts are constructed, whether memory persists, what external data feeds into
the agent, and what destructive actions are possible.

Still follow the [report template](./report-template.md) structure for the
output, noting that findings are based on the described architecture rather than
scanned code.

## References

**Report template**: [report-template.md](report-template.md) — Required report
structure. Every section and table format must appear in the final output.

**Taxonomy**: [reference/taxonomy.md](reference/taxonomy.md) — Severity levels,
surfaces, categories, and script JSON output schema.

**Example output**: [examples/sample-output.json](examples/sample-output.json) —
Sample JSON report showing the expected structure, tone, and detail level.
Use as calibration reference when writing reports.

**OWASP LLM Top 10**: [reference/owasp-llm-top-10.md](reference/owasp-llm-top-10.md) —
OWASP Top 10 for LLM Applications (2025). Maps audit categories to
industry-standard LLM risks. Use to contextualize findings against OWASP.
Source: https://genai.owasp.org/llm-top-10/
