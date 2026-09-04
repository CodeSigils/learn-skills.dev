---
name: launch-readiness
description: "Assess one release candidate for a go/no-go, hold, or risk decision on the exact build. Use when the user asks whether a release, launch, or rollout is ready, or to review a launch plan. Do not use to plan or execute the launch."
---

# Review Launch Readiness

Make one release decision from the exact candidate. Local checks support a candidate claim; merged revision supports landed; live claims need observation from that layer. A plan is not readiness of this build.

Open [launch readiness patterns](references/launch-readiness-patterns.md) for domain-specific release concerns. Open [release health watch](references/release-health-watch.md) when the rollout uses a canary, bounded exposure, or staffed window.

Use `build-distribution-readiness` for signed package proof. Use `run-incident-response` if the candidate is already harming users.
