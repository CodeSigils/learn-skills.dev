---
name: reliability-testing
description: >-
  Design and implement reliability and resilience tests — recovery, failover, fault
  injection / chaos experiments, and endurance — for the ISO/IEC 25010:2023
  Reliability characteristic. Use when: "reliability," "resilience," "信頼性," "chaos
  testing," "failover," "disaster recovery," "what happens if the DB goes down," or
  defining SLOs/error budgets. Produces a resilience test plan with a
  steady-state hypothesis (design mode) and fault-injection experiments / recovery
  test scripts (implementation mode). This skill covers recovery AFTER a fault. Not for:
  finding the load level at which it falls over or throughput/latency SLOs — use
  performance-testing; or guarding intentional destructive/irreversible actions
  (bulk-delete, kill switch) — use safety-analysis. Related: performance-testing,
  safety-analysis, test-strategy-doc.
license: MIT
metadata:
  version: "1.0"
  istqb: "CTFL v4.0 §2.2.1 (non-functional test types)"
  iso25010: [reliability]
  mode: [design, implementation]
---

# Reliability Testing

Prove the system stays available, tolerates faults, and recovers cleanly — by
deliberately breaking it under controlled conditions, not by hoping.

## Objective

A resilience test suite covering the four ISO 25010:2023 Reliability
sub-characteristics — **faultlessness** (correct under normal operation),
**availability**, **fault tolerance**, **recoverability** — each with a measurable
criterion. The failure mode this prevents: an architecture that "has redundancy" on
the diagram but has never had a node killed to prove failover actually works.

## Context Discovery

- **Availability target**: what SLO/error budget applies (e.g. 99.9% = 43 min/month)?
  Recovery objectives: RTO (time to recover) and RPO (tolerable data loss)?
- **Failure domains**: what can fail — instances, AZs, the DB, a downstream API,
  the network? Read the architecture/deploy config; each dependency is a fault to test.
- **Redundancy claims**: what does the system *claim* to survive? Those claims are the
  test scope; an untested failover is a liability.
- **Blast radius control**: can experiments run in staging, or prod with guardrails?
  Never inject faults in prod without an abort condition and limited scope.

## Instructions

1. **State a steady-state hypothesis** (Principles of Chaos Engineering): define the
   normal-operation metric that should hold (e.g. "checkout success rate ≥ 99% and p95
   < 800ms"). Experiments try to *disprove* it.

2. **Recovery testing**: interrupt/kill the system mid-operation; verify it recovers
   affected data and re-establishes the desired state within RTO, losing no more than
   RPO. Test backups by *restoring* them, not by confirming they exist.

3. **Failover testing**: kill the primary (instance, AZ, DB node); assert automatic
   switch to standby with service maintained and no data corruption. Measure the
   failover time.

4. **Fault injection / chaos experiments**: inject one variable at a time — instance
   termination, added latency, packet loss, dependency 500s, disk/CPU pressure — under
   the steady-state hypothesis. Start smallest blast radius; expand only when green.

5. **Endurance/soak for reliability**: run under sustained load for hours/days to
   surface memory leaks, connection exhaustion, and gradual degradation (faultlessness
   over time).

6. **Quantify**: track MTBF, MTTR, and availability (≈ MTBF / (MTBF + MTTR)); a
   resilience improvement should move these numbers.

## Output Format

### design mode

```
# Reliability / Resilience Test Plan: {system}
## Targets: Availability SLO, RTO, RPO, error budget
## Steady-State Hypothesis (the metric that must hold)
## Failure Domains & Experiments
   | Exp ID | Fault injected | Blast radius | Hypothesis | Abort condition | Expected recovery |
## Recovery & Failover procedures under test
## Metrics: MTBF, MTTR, failover time, data loss
```

### implementation mode

- **Fault injection**: Toxiproxy (network latency/drops in integration tests),
  LitmusChaos or Chaos Monkey (instance/pod kills in a cluster), or Gremlin.
  Toxiproxy example — assert the app degrades gracefully under 2s downstream latency:

```js
await toxiproxy.get('payments').addToxic({ type: 'latency', attributes: { latency: 2000 } });
const res = await request(app).post('/checkout');
expect(res.status).toBe(503);          // fails fast, not hangs
expect(res.body.retryable).toBe(true);
```

- **Recovery test**: scripted kill → wait → assert health + data-integrity checks.
- Chaos experiments run on a schedule (too disruptive per-PR); recovery/failover smoke
  can run in a nightly pipeline.

## Anti-Patterns

- **Redundancy assumed, never exercised** — "we have a standby" that has never taken
  traffic. **Guard:** every redundancy claim maps to a failover experiment that kills
  the primary.
- **Backups verified by existence** — a backup nobody has restored is Schrödinger's
  backup. **Guard:** recovery test restores the backup and asserts data integrity.
- **No abort condition** — an unbounded chaos experiment that takes down staging (or
  prod). **Guard:** every experiment declares blast radius + automatic abort criteria.
- **Multiple faults at once** — injecting three failures so you can't attribute the
  break. **Guard:** one variable per experiment.
- **Recovery time unmeasured** — "it came back" without a number vs RTO. **Guard:**
  record and assert failover/recovery time against the objective.

## Related Skills

- `performance-testing` — shares soak/endurance; provides the load under which
  resilience experiments run.
- `test-strategy-doc` — sets availability SLO, RTO/RPO and reliability priority.

## References

- ISO/IEC 25010:2023 — Reliability (faultlessness, availability, fault tolerance, recoverability)
- Principles of Chaos Engineering — https://principlesofchaos.org/
- Tools: Toxiproxy, LitmusChaos, Chaos Monkey, Gremlin
