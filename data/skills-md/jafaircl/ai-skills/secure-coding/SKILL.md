---
name: secure-coding
description: Use for every task that creates, changes, generates, or reviews executable code, configuration, dependencies, build or deployment logic, or reusable code examples. Enforce a universal secure-coding baseline on every change, then apply additional controls and security-specific verification when the change affects a security property, trust boundary, security sink, sensitive data, dependency, or attacker-amplifiable resource.
---

# Secure Coding

Write code that preserves applicable security properties while satisfying the governing behavior.
When this workflow materially creates or edits durable technical prose, `technical-writing` MUST govern that prose.
If security-relevant repository, dependency, or runtime context is not already sufficient, `context-acquisition` MUST govern additional acquisition.
If normative security behavior is undefined, changed, or conflicted, `spec-driven-development` MUST govern it.
If a security choice is architecturally significant and unresolved, `architecture-decisions` MUST govern it.
When security work requires a behavior-changing production fix, `test-driven-development` and `implementation` MUST govern that fix after required security behavior is established.

## Terms

A **security property** is a required property related to confidentiality, integrity, availability, authentication, authorization, accountability, privacy, or isolation.
A **trust boundary** is a point where data, identity, authority, or control passes between components or actors with different trust assumptions.
**Untrusted input** is data whose integrity, structure, origin, or authority is not guaranteed at the point of use.
A **security sink** is an operation where attacker-controlled or insufficiently constrained data can cause a security effect, such as a query, command, path access, template render, redirect, deserialization, network request, or code execution.
A **security impact** exists when a change can alter a security property, trust assumption, security sink, sensitive-data flow, dependency risk, or attacker-amplifiable resource behavior.

## Core Invariant

The agent MUST consider security for every code change and code review.
Every change MUST preserve applicable security properties and MUST satisfy the universal secure-coding baseline in this skill.
The agent MUST assess security impact for every change before the owning workflow reports the change complete.

The agent MUST NOT opt out because a change appears low risk, private, small, internal, or functionally simple.
The security-impact assessment MUST determine which additional controls and verification are applicable; it MUST NOT determine whether secure coding applies.
A low-impact assessment MAY omit additional impact-specific profiles or security-specific verification only after the universal baseline is preserved and material security-impact uncertainty is resolved.
If the agent cannot determine whether a change affects a security property, trust boundary, security sink, sensitive data, dependency, privileged execution path, or attacker-amplifiable resource, it MUST acquire enough context to resolve that uncertainty rather than classify the change as low impact by default.

A control that has no relevant security property, boundary, sink, or threat MUST NOT be added only to satisfy a checklist.
Functional correctness MUST NOT be treated as sufficient security evidence.
Security controls MUST NOT be weakened, bypassed, or converted to fail-open behavior only to simplify implementation or make tests pass.
The agent MUST NOT claim that code is secure merely because this skill was applied or available tests passed.

## Universal Baseline

Apply this baseline to every change:

1. Existing security properties, controls, and documented trust boundaries MUST be preserved unless governing requirements authorize a change.
2. Trust assumptions about callers, gateways, prior validation, deployment topology, or data origin MUST NOT be invented.
3. External or caller-controlled data MUST be treated as untrusted until an authoritative boundary establishes the required properties.
4. Structured, typed, parameterized, or otherwise non-interpreting APIs SHOULD be preferred over construction of executable strings.
5. Secrets and sensitive values MUST NOT be exposed through source, generated artifacts, URLs, diagnostics, or logs unless a governing requirement or protocol requires the exposure and the boundary protects it appropriately.
6. Established suitable cryptographic primitives and protocols SHOULD be used. Custom security protocols or cryptographic constructions MUST NOT be invented without a governing requirement and justified security design.
7. Authority MUST be limited to what the operation requires, and authoritative authorization checks MUST be preserved.
8. Secure failure behavior MUST be preserved. A security-control failure MUST NOT silently become success without governing authority.
9. Errors and diagnostics crossing a trust boundary MUST NOT disclose secrets or sensitive implementation data unless governing requirements explicitly allow the disclosure.
10. Applicable dependency identity, provenance, integrity, and known-vulnerability constraints MUST be preserved when dependencies change.
11. Memory-safe and resource-bounded operations SHOULD be preferred when a safer practical alternative satisfies the requirement.
12. Production bypasses, insecure debug modes, permissive fallbacks, and security-disabled defaults MUST NOT be introduced for convenience.

When an established safer primitive or dependency satisfies the requirement, it SHOULD be preferred over custom security-sensitive logic.

## Security-Impact Assessment

For every change, determine whether it affects authentication or authorization; secrets or cryptography; untrusted input or an interpreter; files, network access, redirects, or deserialization; sensitive data; dependencies; memory safety; attacker-amplifiable resources; transport or browser boundaries; or security-relevant build, deployment, or configuration behavior.

When no additional security impact is identified, the universal baseline still applies.
The assessment MUST NOT conclude that there is no additional security impact while a material security-impact question remains unresolved.
Unrelated security controls, threat-model ceremony, or adversarial tests MUST NOT be manufactured solely to demonstrate security work.

When a security impact exists, the protected property, relevant trust assumption or boundary, required control, and secure failure behavior MUST be established before the production change.
Security-specific verification MUST be selected when a meaningful oracle exists.
Apply `references/security-boundaries.md` to establish this basis when it is not already explicit.

## Impact-Specific Profiles

Load only the profiles that the actual change requires:

- **Input, output, queries, commands, templates, and interpreters:** safe structured APIs and destination-specific protection MUST govern relevant sinks. Apply `references/input-output.md`.
- **Authentication, sessions, authorization, tenancy, and privilege:** identity and authorization MUST be enforced at authoritative boundaries using trusted decision data. Apply `references/auth-and-access.md`.
- **Secrets, cryptography, logging, and sensitive data:** secrets MUST remain protected and custom cryptography MUST NOT replace established suitable primitives. Apply `references/secrets-crypto-data.md`.
- **Files, uploads, archives, outbound requests, redirects, and deserialization:** attacker-controlled data MUST remain within the intended resource and execution boundary. Apply `references/files-network-deserialization.md`.
- **Dependencies and supply chain:** dependency identity, provenance, integrity, compatibility, and known-vulnerability evidence MUST be preserved. Apply `references/dependencies.md`.
- **Failure, memory, and attacker-amplifiable resources:** safe failure, memory-safety boundaries, and required resource bounds MUST be preserved. Apply `references/failure-memory-resources.md`.
- **Build, deployment, CI, and security-relevant configuration:** secure defaults, privilege boundaries, untrusted build inputs, credential exposure, and artifact-integrity controls MUST be preserved. Apply `references/build-deployment.md`.

## Verification

Every code review MUST verify that the universal baseline was not violated by the change.
A change with security impact MUST receive security-specific verification in addition to ordinary functional verification when a meaningful security oracle is available.

Security verification SHOULD use the strongest practical evidence that directly tests the affected property, including focused negative tests, authorization or isolation tests, injection or boundary regression tests, compiler or static-analysis checks, dependency security checks, policy or configuration validation, or authorized proof-of-vulnerability checks.

A passing functional test suite MUST NOT be cited as sufficient evidence that a security-impacting change is secure.
When no additional security impact exists, additional adversarial testing MAY be omitted; this permission MUST NOT be interpreted as permission to ignore the universal baseline.
Security testing MUST NOT attack systems, accounts, networks, or data without authorization.

Apply `references/verification.md` for verification selection.

## Compliance and Guidance Boundaries

Risk and exposure MAY influence which additional controls, verification techniques, and review depth are necessary.
Risk MUST NOT exempt a change from the universal baseline.

Project-declared regulatory, contractual, assurance, or compliance requirements MUST be treated as governing constraints when they apply to the current change.
A particular compliance regime MUST NOT be inferred when the project or task has not established it.
Compliance constraints MUST NOT replace more specific technical security requirements or verification when those requirements apply.

A standard or guidance name MUST NOT substitute for the operational rules in this skill.
Full compliance with a source standard or guidance set MUST NOT be claimed based only on this skill.
Apply `references/sources.md` for exact standards, guidance, versions, agent-security research, and evidence boundaries.

## Deviations

If secure implementation conflicts with a higher-authority requirement, the conflict MUST be reported and resolved through the owning specification or architecture workflow.
A known residual security risk MUST NOT be hidden by describing the implementation as secure.
When a required security control cannot be verified, the unverified control and residual risk MUST be reported.
Security hardening outside the current change SHOULD be reported separately when material rather than silently added to scope.

## Completion

Before an applicable code change or code review is reported complete, `references/review-checklist.md` MUST be applied.
The universal baseline MUST be satisfied. Material security-impact uncertainty, unverified required controls, and known residual risks MUST be resolved or reported rather than hidden by a completion claim.

## References

- `references/security-boundaries.md` — trust boundaries, assets, assumptions, and least privilege.
- `references/input-output.md` — validation, parameterization, encoding, injection, and interpreter boundaries.
- `references/auth-and-access.md` — authentication, sessions, authorization, tenancy, and ownership.
- `references/secrets-crypto-data.md` — secrets, cryptography, logging, and sensitive data.
- `references/files-network-deserialization.md` — path, upload, archive, SSRF, redirect, and deserialization boundaries.
- `references/dependencies.md` — dependency selection, vulnerabilities, provenance, and supply-chain decisions.
- `references/failure-memory-resources.md` — secure failure, memory-safety boundaries, and attacker-amplifiable resources.
- `references/build-deployment.md` — build, CI, deployment, privileged credentials, secure defaults, and artifact integrity.
- `references/verification.md` — universal review, security-specific verification, and safe negative testing.
- `references/review-checklist.md` — universal baseline and impact-specific completion review.
- `references/sources.md` — standards, current versions, research evidence, and house-policy boundaries.
