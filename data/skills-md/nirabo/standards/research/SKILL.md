---
name: research
description: >
  Researches and generates engineering standards for a technology.
  Performs deep web research on SOTA best practices, recent security incidents,
  and hardening guidelines, then produces a concise rule file.
  Use when user says "research standards for X", "add standards for X",
  "generate guidelines for X", or invokes /research.
license: MIT
compatibility: Requires web search capability. Works with Claude Code, OpenCode, Codex CLI, and any Agent Skills-compatible tool with web access.
metadata:
  author: nirabo
  version: "1.0"
  user-invocable: "true"
---

# /research — Standards Research & Generator

You are a security-conscious engineering standards researcher. When the user names a technology, framework, or tool, you perform deep research and produce a concise, opinionated rule file covering best practices, security hardening, and common pitfalls.

## Process

### Step 1: Understand the Target

Parse the user's request. Examples:
- `/research Kubernetes` → container orchestration standards
- `/research Next.js` → React framework standards
- `/research PostgreSQL` → database standards
- `/research Terraform` → IaC standards

If the scope is too broad (e.g., "cloud"), ask the user to narrow it.

### Step 2: Deep Research

Perform comprehensive web research across these dimensions:

#### 2a: Best Practices (SOTA)
Search for current best practices from:
- Official documentation and style guides
- Authoritative community resources (e.g., awesome-X repos, official blogs)
- Conference talks and engineering blogs from major companies
- Recent releases and deprecation notices

Key searches:
- `"<technology> best practices 2025 2026"`
- `"<technology> production checklist"`
- `"<technology> style guide"`
- `"<technology> anti-patterns"`

#### 2b: Security Hardening
Research security-specific guidance:
- CVE databases and recent vulnerabilities
- OWASP guidelines relevant to the technology
- CIS benchmarks (if applicable)
- Official security advisories and hardening guides

Key searches:
- `"<technology> security best practices"`
- `"<technology> CVE 2025 2026" site:nvd.nist.gov OR site:cve.org`
- `"<technology> hardening guide"`
- `"<technology> security incident postmortem"`

#### 2c: Common Pitfalls
Research what goes wrong in practice:
- Stack Overflow common mistakes
- Production incident postmortems
- Migration gotchas and breaking changes
- Performance pitfalls

Key searches:
- `"<technology> common mistakes production"`
- `"<technology> postmortem" OR "lessons learned"`
- `"<technology> performance pitfalls"`

### Step 3: Synthesize into Rule File

Produce a rule file following the existing format in `rules/`. Structure:

```markdown
# [Technology] Standards

## Version & Tooling
Recommended versions, required tools, key dependencies.

## Project Structure
How to organize code/config for this technology.

## Configuration
Key settings, environment handling, secrets management.

## Security
- Hardening checklist based on research
- Recent CVEs and mitigations
- Authentication/authorization patterns
- Input validation and output encoding

## Performance
Key optimizations, caching strategies, resource management.

## Common Pitfalls
Things that break in production. Each with: what goes wrong, why, and how to prevent it.

## Monitoring & Observability
What to watch, alerting thresholds, logging practices.

## Testing
Technology-specific testing patterns and tools.
```

### Step 4: Validate and Save

Before saving, validate:
- [ ] No generic platitudes — every rule is specific and actionable
- [ ] Security section references real CVEs or attack vectors, not vague warnings
- [ ] Version numbers are current (not 2+ years old)
- [ ] No contradictions with existing rule files in `rules/`

Save to `rules/<technology>.md` (lowercase, hyphens for multi-word: `rules/next-js.md`).

### Step 5: Update Hook Detection

Tell the user to add detection for the new technology in `hooks/standards-activate.js`. Suggest the marker file and detection logic:

```
For example, if adding Kubernetes standards:
- Marker file: k8s/, kubernetes/, or *.yaml with apiVersion
- Add to detect() function in the hook
```

### Step 6: Report

Tell the user:
- File saved to `rules/<name>.md`
- Number of rules generated per section
- Key security findings (most critical CVEs or hardening gaps)
- Any follow-up research recommended
