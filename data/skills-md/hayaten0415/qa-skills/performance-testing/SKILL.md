---
name: performance-testing
description: >-
  Design and implement performance tests — load, stress, spike, soak/endurance,
  scalability, and volume — for the ISO/IEC 25010:2023 Performance Efficiency
  characteristic (time behaviour, resource utilization, capacity). Use when:
  "performance test," "load test," "負荷テスト," "性能テスト," "stress test,"
  "throughput," "p95 latency," "how many concurrent users can it handle," or
  before a launch/scaling event. Produces a workload model + SLO-based test plan
  (design mode) and runnable k6/JMeter/Gatling scripts with CI thresholds
  (implementation mode). This skill measures capacity/latency — the load at which the
  system degrades. Not for: crash/hang and recovery AFTER a fault — use
  reliability-testing; or single-request profiling / algorithmic Big-O (code
  optimization). Related: reliability-testing, test-strategy-doc.
license: MIT
metadata:
  version: "1.0"
  istqb: "CTFL v4.0 §2.2.1; CT-PT (Certified Tester — Performance Testing)"
  iso25010: [performance-efficiency]
  mode: [design, implementation]
---

# Performance Testing

Measure time behaviour, resource utilization, and capacity against explicit targets
under a realistic workload — not "it felt fast on my laptop."

## Objective

A performance test suite driven by an SLO-anchored workload model, covering the test
types the risk warrants (load, stress, spike, soak, scalability, volume), with
pass/fail thresholds wired into CI. The failure mode this prevents: shipping with no
number for p95 latency or max sustainable throughput, then discovering the ceiling in
production during a traffic peak.

## Context Discovery

Infer before asking:

- **SLOs/SLAs**: target p95/p99 latency, error rate, throughput. If none exist, that
  is finding #1 — you cannot pass/fail without a number. Propose targets from current
  production metrics if available.
- **Workload shape**: realistic user mix, peak vs average concurrency, think times,
  data volumes. Read analytics/APM (Datadog, Grafana, CloudWatch) rather than guessing.
- **Environment parity**: is the test env representative of prod (instance sizes, data
  volume)? Results from a toy env are misleading — state the caveat explicitly.
- **Tooling**: detect existing tooling in the repo (k6/JMeter/Gatling/Locust).

## Instructions

1. **Build the workload model first**: define scenarios, their weight, arrival rate,
   ramp profile, and test data. A load test without a justified workload model tests
   an imaginary system.

2. **Select test types by risk** (ISTQB CT-PT):
   - **Load** — behaviour at expected/peak load; establishes the baseline.
   - **Stress** — at and beyond limits (or with reduced resources); finds the breaking
     point and failure mode.
   - **Spike** — sudden surge then drop; tests autoscaling/queueing.
   - **Soak/Endurance** — sustained load over hours; surfaces memory leaks and gradual
     degradation.
   - **Scalability** — does capacity grow when you scale up/out?
   - **Volume** — behaviour with large data sets.
   Pick the subset the risk justifies; document which you skipped and why.

3. **Define pass/fail thresholds**, not just graphs: e.g. `p95 < 500ms AND error_rate
   < 1% at 1000 RPS`. Thresholds fail the CI job, so regressions block merges.

4. **Isolate variables**: warm up caches, run enough iterations for stable numbers,
   pin the environment, and run baseline + candidate on the same infra. Report the
   environment alongside every result.

5. **Measure the full picture**: latency percentiles (not just mean), throughput,
   error rate, AND resource utilization (CPU, memory, connections) to attribute a
   bottleneck to a resource.

## Output Format

### design mode

```
# Performance Test Plan: {system}
## SLOs (p95/p99 latency, throughput, error budget)
## Workload Model (scenarios, weights, arrival/ramp profile, data)
## Test Types in scope (load/stress/spike/soak/scalability/volume + why)
## Environment & parity caveats
## Pass/Fail Thresholds per scenario
## Metrics & observability (what to capture, where)
```

### implementation mode

k6 canonical shape (thresholds are the pass/fail gate):

```js
import http from 'k6/http';
import { check } from 'k6';
export const options = {
  scenarios: { load: { executor: 'ramping-vus', stages: [
    { duration: '2m', target: 200 }, { duration: '5m', target: 200 }, { duration: '2m', target: 0 },
  ] } },
  thresholds: { http_req_duration: ['p(95)<500'], http_req_failed: ['rate<0.01'] },
};
export default function () {
  const res = http.get(`${__ENV.BASE_URL}/api/orders`);
  check(res, { 'status 200': (r) => r.status === 200 });
}
```

Use the repo's tool if one exists (JMeter `.jmx`, Gatling Scala/Java DSL, Locust
Python). One scenario file per workload; thresholds mirror the SLOs from design mode.

## Anti-Patterns

- **Testing without SLOs** — LLMs generate a load script but no thresholds, so it can
  never fail. **Guard:** every scenario has a numeric pass/fail threshold tied to an
  SLO; no threshold = incomplete.
- **Averages hide pain** — reporting mean latency masks the p99 tail users actually
  feel. **Guard:** always report percentiles (p95/p99), never mean alone.
- **Unrealistic workload** — hammering one endpoint at max RPS with zero think time
  proves nothing about real usage. **Guard:** workload model derived from analytics.
- **Non-representative env** — passing on a laptop, failing in prod. **Guard:** state
  environment parity; flag when the test env cannot represent production.
- **Hallucinated tool APIs** — inventing k6/JMeter options that don't exist. **Guard:**
  verify option/executor names against the installed tool version.

## Related Skills

- `reliability-testing` — soak/endurance overlaps; reliability adds fault injection.
- `test-strategy-doc` — decides the performance-efficiency priority and SLO targets.

## References

- ISO/IEC 25010:2023 — Performance Efficiency (time behaviour, resource utilization, capacity)
- ISTQB Certified Tester — Performance Testing (CT-PT) syllabus
- Tools: k6, Apache JMeter, Gatling, Locust
