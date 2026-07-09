---
name: performance-optimization
description: Performance optimization workflow inspired by Abseil Performance Hints. Use when reviewing or changing performance-sensitive code, CPU/memory/latency hot paths, benchmarks, profiles, allocation-heavy paths, cache-locality problems, C++ APIs/data structures, protobuf use, concurrency or lock contention, flat profiles, or when the user asks to optimize, speed up, reduce allocations, improve throughput, lower latency, or evaluate performance tradeoffs.
---

# Performance Optimization

License notice: This skill is an original workflow/checklist inspired by Abseil Performance Hints. The source document is in the Apache-2.0 licensed `abseil/abseil.github.io` documentation repository. See the repository `LICENSE` and `NOTICE` files for attribution.

## Overview

Use this skill to make performance work evidence-driven, narrow, and maintainable. It converts the Abseil Fast performance-hints style into an agent workflow: classify the path, measure or estimate, pick an optimization family, make a small change, and verify the result.

Primary source: https://abseil.io/fast/hints.html

For detailed prompts and checklists, read `references/optimization-checklist.md`.

## Workflow

1. Define the performance question.
   - Identify whether the code is test-only, initialization, request path, library code, batch job, compiler path, serialization path, or synchronization path.
   - State the target metric: latency, throughput, CPU, memory footprint, allocations, binary size, tail latency, lock wait, or build time.
   - Locate the likely hot loop, hot API boundary, hot data structure, or high-frequency call site.

2. Get evidence before optimizing.
   - Prefer existing production metrics, profiles, traces, benchmark results, or regression reports.
   - If evidence is missing, add a focused benchmark, profile, allocation profile, lock-contention profile, or back-of-the-envelope estimate before making invasive changes.
   - For obvious low-risk changes, still explain why they are low risk and how they will be checked.

3. Choose the highest-leverage optimization family.
   - Prefer algorithmic or structural improvements before micro-optimizations.
   - Prefer avoiding work over making unnecessary work faster.
   - Prefer better data representation and fewer allocations when profiles show memory, allocator, or cache pressure.
   - Prefer bulk APIs and view types when per-item calls or copying dominate.
   - Prefer concurrency changes only after checking contention, available parallelism, and memory-bandwidth limits.

4. Keep changes inside clean boundaries.
   - Preserve public APIs when possible.
   - If an API change is needed, make it narrow and justify caller impact.
   - Avoid clever code unless the measured gain matters and tests protect the behavior.

5. Verify and report.
   - Run correctness tests plus the relevant benchmark/profile.
   - Compare before/after numbers with units and sample sizes when available.
   - Mention benchmark limitations and follow-up risks.
   - If no reliable measurement can be run, say so and provide the best available estimate.

## Review Heuristics

Look for these common opportunities:

- Algorithmic cost: repeated scans, nested loops, avoidable sorting, per-edge graph updates, repeated parsing, or general algorithms where a specialized case is common.
- Work avoidance: eager work that can be lazy, repeated computations that can be cached, cold paths mixed into hot paths, expensive checks in release hot paths, or debug/log formatting done unnecessarily.
- API shape: per-item calls where bulk calls can amortize validation, locking, allocation, parsing, RPC setup, or container lookup overhead.
- Copying and ownership: large values copied instead of moved, owned strings where views suffice, temporary containers built repeatedly, stable sorts where unstable sort is acceptable.
- Allocation pressure: allocation inside hot loops, one object per element, repeated vector growth, unnecessary heap ownership, arenas with mismatched lifetimes.
- Cache locality: pointer-rich structures, nested maps, maps for small integer domains, cold fields beside hot fields, mutable fields sharing cache lines across threads.
- Synchronization: locks around expensive work, fine-grained locking in hot paths, read-mostly data behind contended locks, atomics or lock-free code without strong justification.
- Serialization: protobufs used as in-memory data structures, deep message hierarchies, protobuf maps, large live parsed objects, repeated parse/serialize work.
- Code size and instruction cache: excessive inlining, templated slow paths in hot headers, heavy logging or status construction on success paths.

## Guardrails

- Do not optimize based only on style preference.
- Do not trade away readability, API usability, or correctness for small wins unless the path is proven important.
- Treat microbenchmarks as evidence about one workload, not proof of whole-system improvement.
- Validate with the narrowest benchmark and the broadest affordable system check.
- When a profile is flat, consider many small improvements, but still group them by measured subsystem impact.

## Response Shape

When reporting an optimization review or change, use:

1. Evidence: profile, benchmark, trace, estimate, or why measurement is currently blocked.
2. Bottleneck: the specific cost being attacked.
3. Change: smallest maintainable change that addresses it.
4. Validation: correctness checks and before/after performance numbers.
5. Risks: workload sensitivity, API impact, readability cost, or follow-up measurements.
