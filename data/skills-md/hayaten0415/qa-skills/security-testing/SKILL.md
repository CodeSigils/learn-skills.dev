---
name: security-testing
description: >-
  Design and implement application security testing grounded in OWASP (Top 10, ASVS,
  WSTG) for the ISO/IEC 25010:2023 Security characteristic (confidentiality,
  integrity, non-repudiation, accountability, authenticity, resistance). Use when:
  "security testing," "セキュリティテスト," "OWASP," "SAST/DAST," "vulnerability
  scan," "penetration test scope," "SQL injection," "auth/access control testing,"
  "dependency/secrets scanning," or hardening a CI pipeline. Produces an ASVS-based
  test plan (design mode) and CI security gates — SAST/DAST/SCA/secrets scans
  (implementation mode). Authorized/defensive testing only. Not for: LLM-specific
  attacks (prompt injection, jailbreak, RAG red-teaming) — use llm-application-testing;
  or infra/network pen-testing of third parties. Related: test-strategy-doc,
  llm-application-testing.
license: MIT
metadata:
  version: "1.0"
  istqb: "CTFL v4.0 §2.2.1 (non-functional test types)"
  iso25010: [security]
  mode: [design, implementation]
---

# Security Testing

Verify the application protects data and resists attack, using OWASP's testable
standards as the coverage map — not an ad-hoc "we ran a scanner once."

## Objective

A security test approach anchored to **OWASP ASVS** (requirements), **OWASP Top 10**
(the highest-risk categories), and **OWASP WSTG** (how to test each), covering the six
ISO 25010:2023 Security sub-characteristics, and enforced as CI gates. The failure
mode this prevents: security treated as a one-off audit rather than a repeatable,
regression-proof part of the pipeline.

> **Scope & authorization:** apply only to systems you are authorized to test
> (your own app, or with explicit written permission). This skill is for defensive
> testing and secure-SDLC hardening, not for attacking third parties.

## Context Discovery

- **Risk profile & compliance**: handles PII/PHI/payment data? Subject to PCI-DSS,
  GDPR, HIPAA, SOC 2? These set the required rigor and the ASVS level (L1/L2/L3).
- **Attack surface**: public API, auth flows, file upload, admin panel, third-party
  integrations — read routes/controllers to enumerate untrusted-input sinks.
- **Existing controls**: what scanning already runs in CI? Auth model (session/JWT/
  OAuth)? Don't duplicate; find the gaps.
- **Stack**: languages/frameworks (selects the right SAST/SCA tooling).

## Instructions

1. **Set the ASVS level and derive requirements**: L1 (baseline) / L2 (most apps,
   defense-in-depth) / L3 (high-value). ASVS chapters (auth, access control, session,
   validation, crypto, logging) become your requirement checklist.

2. **Map the Top 10 to concrete tests**: for each relevant category — Broken Access
   Control, Injection, Cryptographic Failures, Security Misconfiguration, Supply Chain,
   Authentication Failures, etc. — define at least one test. Use the current OWASP Top
   10 edition; verify categories rather than reciting from memory.

3. **Layer the techniques** (each catches what others miss):
   - **SAST** — static analysis of source for injection sinks, hardcoded secrets,
     unsafe APIs.
   - **DAST** — dynamic black-box probing of the running app (XSS, injection, auth
     bypass), guided by WSTG test cases.
   - **SCA / dependency scanning** — known-vulnerable libraries (CVEs) → maps to Supply
     Chain Failures.
   - **Secrets scanning** — credentials/keys/tokens in code and git history.
   - **AuthN/AuthZ testing** — privilege escalation, IDOR, missing function-level
     access control (the #1 category); test as multiple roles.
   - **Injection testing** — SQLi, command injection, SSRF, XSS on every untrusted sink.

4. **Manual verification for logic flaws**: automated tools miss business-logic authz
   (e.g. user A reading user B's order via a guessable ID). Test object-level
   authorization manually per critical resource.

5. **Triage by real risk**: rank findings by exploitability × impact, not scanner
   severity alone. Confirm exploitability before filing a Critical; note false positives.

6. **Gate in CI**: SAST/SCA/secrets on every PR (fail on high severity); DAST on a
   schedule (slower). Track the ASVS checklist as living coverage.

## Output Format

### design mode

```
# Security Test Plan: {app} — ASVS Level {L1/L2/L3}
## Compliance drivers (PCI/GDPR/HIPAA/SOC2)
## Attack surface & trust boundaries
## Top 10 coverage
   | Category | Applicable? | Test(s) | Technique | Tool |
## ASVS requirement checklist (per chapter, pass/fail)
## Manual test cases (business-logic authz, IDOR)
## CI gates & severity policy
```

### implementation mode

CI security gates (fail the build on high severity):

```yaml
# SAST + secrets + dependency scanning on every PR
- run: semgrep ci                 # SAST (OWASP/CWE rulesets)
- run: gitleaks detect --no-git   # committed secrets
- run: trivy fs --severity HIGH,CRITICAL --exit-code 1 .   # SCA / vulns
# DAST on schedule against a deployed env
- run: zap-baseline.py -t "$STAGING_URL" -c zap.conf
```

Add role-based API tests asserting a lower-privilege token gets 403 on privileged
endpoints. Verify tool/rule names against installed versions.

## Anti-Patterns

- **Scanner output = security posture** — a green scan with untested business-logic
  authz. **Guard:** manual object-level authorization tests for every sensitive
  resource; scanners don't understand your permission model.
- **Unconfirmed Criticals / false positives filed as fact** — flooding devs with
  noise. **Guard:** confirm exploitability before rating Critical; note FPs.
- **Reciting an outdated Top 10 / hallucinated CVEs** — quoting categories or CVE IDs
  from memory. **Guard:** cite the current OWASP Top 10 edition and real CVE IDs from
  the scan; verify, don't recall.
- **Testing prod without authorization** — legal and ethical breach. **Guard:** written
  scope + authorization before any active testing; prefer staging.
- **Secrets scanning HEAD only** — a key rotated out of HEAD still lives in history.
  **Guard:** scan git history, and rotate any exposed secret (don't just delete it).

## Related Skills

- `llm-application-testing` — LLM-specific attacks (prompt injection, RAG red-teaming);
  hand off LLM features while this skill covers the classic app/API surface.
- `test-strategy-doc` — sets the Security priority, ASVS level, and compliance drivers.

## References

- OWASP Top 10 (current edition) — https://owasp.org/Top10/
- OWASP ASVS (Application Security Verification Standard) — https://owasp.org/www-project-application-security-verification-standard/
- OWASP WSTG (Web Security Testing Guide) — https://owasp.org/www-project-web-security-testing-guide/
- ISO/IEC 25010:2023 — Security (confidentiality, integrity, non-repudiation, accountability, authenticity, resistance)
- Tools: OWASP ZAP, Semgrep, Trivy, Dependabot, gitleaks
