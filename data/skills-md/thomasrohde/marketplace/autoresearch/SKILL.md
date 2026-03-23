---
name: autoresearch
description: >
  Autonomous agent-driven optimization loop inspired by Karpathy's autoresearch.
  Sets up and runs an iterative hill-climbing harness where subagents modify an
  artifact, evaluate against a single scalar metric, and keep improvements.
  Use this skill whenever the user wants to "optimize something iteratively",
  "run an autoresearch loop", "hill-climb on performance", "auto-optimize",
  "iterate and improve automatically", "run experiments autonomously",
  "autonomous optimization", or mentions "autoresearch" in any context.
  Also triggers when the user describes a workflow like "try variations and
  measure which is best", "keep tweaking until it's faster", "optimize this
  config", "find the best prompt", "tune hyperparameters", "benchmark
  variations", or any scenario where they want an agent to autonomously
  explore a search space against a measurable objective. Works with any
  domain — code performance, prompt engineering, config tuning, SQL optimization,
  CSS optimization, model training, build flags, or anything with a measurable
  outcome.
---

# autoresearch

An autonomous optimization loop where subagents iteratively modify an artifact,
evaluate it against a single scalar metric, and keep improvements. Inspired by
[Karpathy's autoresearch](https://github.com/karpathy/autoresearch) — generalized
beyond ML training to any domain with a measurable objective.

## The pattern in four invariants

| Component | What it is | Why it matters |
|-----------|-----------|----------------|
| **Editable artifact** | The file(s) the agent modifies each iteration | Bounds the search space |
| **Evaluation oracle** | A command that produces a single number on stdout | Unambiguous better/worse signal |
| **Metric direction** | `minimize` or `maximize` | Tells the agent which way is "better" |
| **Program document** | Human-written intent, constraints, and boundaries | Steers the search without micromanaging |

The loop is simple: hypothesize → edit → evaluate → keep or revert → repeat.

## Phase 1: Setup interview

Before scaffolding anything, understand the use case. Gather these answers from the
user — extract what you can from conversation context and ask for the rest:

1. **What are you optimizing?** Identify the artifact file(s). Examples:
   - A Python script's runtime performance
   - A prompt template's accuracy on a test set
   - An nginx config's throughput
   - A SQL query's execution time
   - A CSS file's Lighthouse score

2. **How do we measure success?** Identify or help create the evaluation command.
   It must:
   - Be runnable as a single shell command
   - Print exactly one number to stdout (the metric)
   - Exit 0 on success, non-zero on failure
   - Complete in a bounded time (ideally under 5 minutes)

3. **Which direction is better?** `minimize` (latency, error rate, file size) or
   `maximize` (throughput, accuracy, score).

4. **What's off limits?** Constraints the agent must respect. Examples:
   - "Don't change the public API"
   - "Keep Python 3.10 compatibility"
   - "Don't add dependencies"
   - "Output format must stay the same"

5. **How many iterations?** Default: 20. The user can set a limit or say "run until
   I stop you."

6. **Evaluation budget per iteration?** If the evaluation command has a natural time
   bound (like training for N minutes), note it. Otherwise the evaluation command's
   own runtime is the budget.

If the user provides a use case description up front (e.g., "optimize my sorting
algorithm for speed"), extract as much as possible and confirm the gaps.

## Phase 2: Scaffold the harness

Create a `.autoresearch/` directory in the project root with these files:

### `.autoresearch/config.json`

```json
{
  "artifact_paths": ["path/to/file.py"],
  "eval_command": "python evaluate.py",
  "metric_name": "execution_time_ms",
  "metric_direction": "minimize",
  "max_iterations": 20,
  "branch_prefix": "autoresearch",
  "created_at": "2026-03-15T10:00:00Z"
}
```

### `.autoresearch/program.md`

Write this collaboratively with the user. It should contain:

```markdown
# Research Program: [Title]

## Objective
[One sentence: what we're optimizing and why]

## Artifact
[Path to the file(s) being modified, and a brief description of what they contain]

## Evaluation
[The eval command and what the metric means]

## Constraints
[What the agent must NOT change or break]

## Strategy hints
[Optional: suggested directions to explore, known dead ends, domain knowledge]
```

The program.md is the most important file — it's the agent's "research brief." Help
the user write one that's specific enough to be useful but open enough to allow
creative exploration. Explain *why* constraints exist so the agent can reason about
edge cases.

### `.autoresearch/results.tsv`

Initialize with the header row:

```
iteration	timestamp	commit	metric_value	hypothesis	changes_summary	kept
```

### Evaluation script

If the user doesn't already have an evaluation command, help create one. Save it as
`evaluate.py` (or `evaluate.sh`) in the project root. The script must:

- Print exactly one number to stdout
- Send all diagnostics to stderr
- Exit 0 on success
- Exit non-zero if the artifact is broken (syntax error, crash, etc.)

Example patterns:

**Performance benchmark:**
```python
import subprocess, time, statistics, sys

times = []
for _ in range(5):
    start = time.perf_counter()
    result = subprocess.run(["python", "solution.py"], capture_output=True)
    if result.returncode != 0:
        print("FAILED", file=sys.stderr)
        sys.exit(1)
    times.append(time.perf_counter() - start)

print(f"{statistics.median(times) * 1000:.1f}")  # median ms
```

**Accuracy eval:**
```python
import json, sys

results = json.load(open("test_results.json"))
correct = sum(1 for r in results if r["predicted"] == r["expected"])
print(f"{correct / len(results) * 100:.2f}")  # accuracy %
```

### Baseline run

Before starting the loop, run the evaluation once on the unmodified artifact to
establish a baseline. Record it as iteration 0 in results.tsv.

### Git branch

Create a dedicated branch:
```
git checkout -b autoresearch/<topic>-<date>
```

Commit the scaffold files as the first commit on this branch.

## Phase 3: Run the optimization loop

This is the core of the skill. You act as the **coordinator**, spawning a subagent
for each iteration.

### Loop structure

```
for each iteration (1 to max_iterations):
    1. Spawn a researcher subagent
    2. Wait for it to complete
    3. Collect the metric
    4. If improved: git commit, log as kept
    5. If not improved: git revert changes, log as not kept
    6. Report progress to user
    7. Check stopping criteria
```

### Spawning the researcher subagent

For each iteration, spawn a subagent with this prompt template (adapt the specifics
to the use case):

```
You are a researcher running iteration {N} of an optimization loop.

## Your goal
Improve the metric "{metric_name}" ({metric_direction} is better).
Current best: {best_value} (iteration {best_iteration}).

## Research program
{contents of .autoresearch/program.md}

## History of past experiments
{contents of .autoresearch/results.tsv}

## Instructions
1. Read the artifact file(s): {artifact_paths}
2. Analyze the history — what has been tried, what worked, what didn't
3. Form a hypothesis about what change might improve the metric
4. Edit the artifact file(s) to test your hypothesis
5. Run the evaluation: {eval_command}
6. Report your results

## Output format
After running the evaluation, output exactly this JSON to stdout:
{
  "hypothesis": "what you tried and why",
  "changes_summary": "brief description of edits made",
  "metric_value": <the number from evaluation>,
  "eval_exit_code": <0 or non-zero>,
  "notes": "any observations for future iterations"
}

If evaluation fails (non-zero exit), still report — set metric_value to null.

## Rules
- Make ONE focused change per iteration (easier to attribute improvements)
- Read the full experiment history before deciding what to try
- Don't repeat experiments that already failed
- Stay within the constraints defined in the research program
- If you're stuck after seeing many failures, try a fundamentally different approach
```

Use `mode: "bypassPermissions"` for the subagent so it can edit files and run
commands without prompting.

### Handling results

After each subagent completes:

1. **Parse the result** — extract metric_value from the subagent's output
2. **Compare to best** — check if this iteration improved the metric
3. **If improved:**
   - `git add` the changed artifact files
   - `git commit -m "autoresearch: iteration {N} — {hypothesis} ({metric}: {value})"`
   - Update best_value and best_iteration
   - Append to results.tsv with `kept=true`
4. **If not improved or evaluation failed:**
   - `git checkout -- {artifact_paths}` to revert changes
   - Append to results.tsv with `kept=false`
5. **Report to user** — brief status line:
   `Iteration {N}: {metric}={value} (best={best}) — {kept/reverted} — "{hypothesis}"`

### Stopping criteria

Stop the loop when any of these are true:
- Reached max_iterations
- The user interrupts (sends a message)
- 5 consecutive iterations without improvement (plateau detection)
- The evaluation command fails 3 times in a row (something is broken)

When stopping, report a summary.

## Phase 4: Summary report

When the loop ends (or is interrupted), produce a summary:

```markdown
## Autoresearch Summary: [topic]

**Iterations:** {total} ({kept} improvements, {reverted} reverted)
**Baseline:** {metric_name} = {baseline_value}
**Final best:** {metric_name} = {best_value} (iteration {best_iteration})
**Improvement:** {percentage}% {better/worse}

### Top improvements
| Iter | Metric | Hypothesis | Kept |
|------|--------|-----------|------|
| ...  | ...    | ...       | ...  |

### Key observations
- [What worked]
- [What didn't work]
- [Suggested next directions]
```

Also point the user to:
- `.autoresearch/results.tsv` — full experiment log
- The git log on the autoresearch branch — each kept iteration is a commit
- The final state of the artifact — the current best version

## Tips for effective use

### Writing good evaluation commands
- **Deterministic is ideal.** If your metric has variance (e.g., network latency),
  run multiple samples and report the median.
- **Fast feedback wins.** A 10-second eval enables 6x more iterations per hour than
  a 60-second eval. If your eval is slow, consider a proxy metric.
- **Fail loudly.** If the artifact is broken (syntax error, crash), exit non-zero
  so the iteration is marked as failed and reverted.

### Writing good program documents
- **Explain the why.** "Don't use recursion" is less useful than "Don't use recursion
  because the input can be 10M items deep and Python's stack limit is 1000."
- **Seed with domain knowledge.** If you know that "batch processing usually helps"
  or "the bottleneck is probably I/O", say so — it saves the agent from rediscovering
  basics.
- **Define the boundaries, not the path.** Tell the agent what's off-limits, not
  what to do. Let it explore creatively within the constraints.

### When autoresearch works best
- Clear, fast, scalar metric
- Single file or small set of files to modify
- Large search space with many possible improvements
- Domain where LLMs can reason about the artifact (code, configs, prompts, text)

### When to use something else
- Multi-objective optimization with no clear weighting
- Artifacts that require human judgment (visual design, UX, writing tone)
- Evaluation that takes hours per run
- Changes that require coordinated edits across many files
