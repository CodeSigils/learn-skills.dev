---
name: incident-response
description: Use when recording, triaging, or learning from failures; creates incident records with symptom, cause, impact, mitigation, prevention, systems, domains, and traceability.
---

# Purpose

Reusable workflow for incident response and preservation.

# Required Knowledge

- `ai-workspace/70-knowledge/incidents/TEMPLATE.md`
- `ai-workspace/70-knowledge/domains/`
- `ai-workspace/70-knowledge/systems/`
- `ai-workspace/90-logs/errors.md`
- `ai-workspace/90-logs/bugs.md`
- `ai-workspace/90-logs/conflicts.md`

# Inputs

- symptom
- affected system
- affected domain
- observed impact
- mitigation taken
- suspected or known cause

# Workflow

1. Capture symptom.
2. Identify related systems and domains.
3. Search previous incidents and logs.
4. Record cause or hypothesis.
5. Record impact.
6. Record mitigation.
7. Define prevention.
8. Create or update incident markdown under `ai-workspace/70-knowledge/incidents/`.
9. Link related logs, tasks, artifacts, and commits.
10. Recommend distilled knowledge or skill updates when the pattern is reusable.

# Safety Rules

- Do not hide failed attempts.
- Do not mark root cause as certain if it is only a hypothesis.
- Do not delete previous incident history.
- Do not expose secrets or private data.

# Incident References

- Always check existing incidents before creating a new one.

# Output

- incident markdown
- linked log entry when needed
- prevention recommendation

# Verification

- Incident includes symptom, cause, impact, mitigation, prevention, related systems, and related domains.
- Traceability links are present.
- Verified status is explicit.
