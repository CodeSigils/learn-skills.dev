---
name: dispatching-parallel-agents
description: "Run multiple independent tasks in parallel using subagents for faster execution."
---

# Dispatching Parallel Agents

## Overview
Parallel agent dispatching executes multiple independent tasks simultaneously by leveraging subagents. This skill should be invoked when you have three or more independent tasks that can run concurrently without sharing state or sequential dependencies.

## Core Principles
- **Independence**: Tasks must not depend on each other's output
- **Clear Boundaries**: Each subagent should have focused, self-contained work
- **Result Aggregation**: Plan how to combine results after parallel execution
- **Resource Management**: Consider parallel execution limits

## Preparation Checklist
- [ ] Identify all tasks and verify they are independent
- [ ] Break down work into focused subtasks
- [ ] Define what each subagent needs to know
- [ ] Plan result integration approach

## Step-by-Step Process
1. **Analyze**: Verify tasks have no dependencies
2. **Break Down**: Divide work into focused subtasks
3. **Spawn**: Launch all subagents in parallel
4. **Wait**: Collect results as they complete
5. **Integrate**: Aggregate results into unified outcome
6. **Verify**: Ensure all results are correct

## Do's and Don'ts
- ✅ **Do** verify tasks are truly independent before parallelizing
- ✅ **Do** provide clear context to each subagent
- ✅ **Do** wait for all results before proceeding
- ❌ **Don't** parallelize tasks with hidden dependencies
- ❌ **Don't** overload subagents with too much work
- ❌ **Don't** skip result verification

## Anti-Patterns
- **False Independence**: Assuming tasks are independent when they're not
- **Context Leak**: Subagents accidentally depending on each other
- **Result Loss**: Not properly collecting all results
- **Over-Parallelization**: Spawning too many agents at once
