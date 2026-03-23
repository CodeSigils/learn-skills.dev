---
name: run-experiment
description: >
  Deploy and run ML experiments on remote GPU servers. Use this skill whenever
  the user wants to run training jobs, launch experiments, execute scripts on
  remote machines, or check GPU status. Triggers on: "跑实验", "跑一下",
  "run experiment", "在3090上跑", "launch", "multi-seed", "grid search",
  or any request involving remote GPU execution.
---

# Run Experiment

All remote execution is unified into a single self-contained bash script.
The script is generated locally, synced to remote via syncthing, then launched
in a tmux session. Output is redirected to a log file. Claude waits event-driven
via `tmux wait-for` — no polling, no sleep loops.

## Core Concept

```
One experiment = one bash script + one log file (same name, different suffix)

Local:  exp/scripts/{exp_name}_{timestamp}.sh   → syncthing → Remote
Remote: exp/logs/{exp_name}_{timestamp}.log      ← rsync    ← Local
```

The script is fully self-contained: no arguments, all parameters hardcoded inside.
The script handles conda init, GPU assignment, and the actual command internally.
Output redirection happens at the tmux launch level, not inside the script.

## CLAUDE.md Config

Minimal config needed:
```yaml
remote:
  device: 3090
  devices:
    3090:
      ssh_alias: "3090"
      work_dir: "~/00_lab/graph/gramoe-align"
      conda_env: "graph"
      preferred_gpus: [2, 3, 5, 7]   # optional
      excluded_gpus: [0, 1]           # optional
    l40:
      ssh_alias: "l40"
      work_dir: "~/projects/gramoe-align"
      conda_env: "llm"
```

If `conda_env` is missing, auto-detect (see Phase 1).

## Workflow

### Phase 1: Read Config

Locate project `CLAUDE.md`: check cwd, search upward, or search `~/workspace/`
by project name.

Extract: `ssh_alias`, `work_dir`, `conda_env`, `preferred_gpus`, `excluded_gpus`.

**Detect conda path and envs on remote:**
```bash
ssh {ssh_alias} '
  for p in ~/miniforge3 ~/miniconda3 ~/anaconda3 ~/opt/conda; do
    [ -f "$p/bin/conda" ] && echo "CONDA_PATH=$p" && $p/bin/conda env list && break
  done
'
```
Use the detected path as `{conda_path}` in the script template.
If `conda_env` is missing, pick the most likely env (match project name or common names
like `graph`, `ml`, `torch`). Confirm with user, then write back to CLAUDE.md.

### Phase 2: GPU Selection

```bash
ssh {ssh_alias} 'nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader'
```

Three-level priority:
1. User specifies in prompt ("用GPU3", "CUDA_VISIBLE_DEVICES=2") → use directly
2. CLAUDE.md `preferred_gpus` / `excluded_gpus` → filter candidates
3. Auto-select: prefer truly idle GPUs (memory < 100MiB AND util < 5%)
   - Tier 1: memory < 100MiB AND util < 5% → select automatically
   - Tier 2: memory < 500MiB AND util < 20% → confirm with user
   - All busy → show table, ask user

### Phase 3: Sync Check

```bash
# Compare git hash local vs remote
git -C {local_project_dir} rev-parse HEAD
ssh {ssh_alias} 'cd {work_dir} && git rev-parse HEAD 2>/dev/null || echo NO_GIT'
```

- Match → proceed
- Mismatch → wait up to 30s for syncthing, then fallback rsync:
  ```bash
  rsync -avz --exclude='exp/' --exclude='__pycache__/' --exclude='*.pyc' \
    {local_project_dir}/ {ssh_alias}:{work_dir}/
  ```
- Uncommitted local changes → warn user (syncthing syncs disk state, not git state)

### Phase 4: Generate Script

**Script naming:** `{exp_name}_{timestamp}.sh`
- `exp_name` = semantic description of what this run does, e.g. `acm2dblp_full`, `cora_mseed`
- `timestamp` = `$(date +%Y%m%d_%H%M%S)` — ensures uniqueness

**Script location:** `{local_project_dir}/exp/scripts/` (syncthing auto-syncs this)

**Script template:**
```bash
#!/bin/bash
# Experiment: {exp_name}
# Generated: {timestamp}
# Device: {ssh_alias} | GPU: {gpu_id} | Env: {conda_env}

# CONDA_PATH: auto-detected in Phase 1 from remote env listing
# e.g. ~/miniforge3, ~/miniconda3, ~/anaconda3 — fill in actual path
CONDA_PATH="{conda_path}"
CONDA_ENV="{conda_env}"
WORK_DIR="{work_dir}"
GPU_ID="{gpu_id}"

eval "$($CONDA_PATH/bin/conda shell.bash hook)"
conda activate $CONDA_ENV 2>/dev/null

cd $WORK_DIR

# --- experiment command ---
PYTHONPATH=. CUDA_VISIBLE_DEVICES=$GPU_ID python exp/main.py \
  --source ACMv9 --target DBLPv7

# --- end ---
echo $? > /tmp/{exp_name}_{timestamp}.exit
tmux wait-for -S {exp_name}_{timestamp}_done
```

All parameters hardcoded. No arguments passed at runtime.
The `tmux wait-for -S` is always the last line.

**Sync script to remote:**
- syncthing: script in `exp/scripts/` is auto-synced. Verify it appears on remote:
  ```bash
  ssh {ssh_alias} 'ls {work_dir}/exp/scripts/{script_name} 2>/dev/null && echo OK || echo MISSING'
  ```
- If MISSING after 10s → scp directly:
  ```bash
  scp {local_script} {ssh_alias}:{work_dir}/exp/scripts/
  ```

### Phase 5: Launch

**Check for duplicate session:**
```bash
ssh {ssh_alias} 'tmux has-session -t {exp_name} 2>/dev/null && echo EXISTS || echo OK'
```
If EXISTS → warn user, ask to kill or abort.

**Step A — Launch tmux session (returns immediately):**
```bash
ssh {ssh_alias} 'tmux new-session -d -s {exp_name} \
  bash -c "bash {work_dir}/exp/scripts/{script_name} \
  > {work_dir}/exp/logs/{log_name} 2>&1"'
```

- Script and log share the same base name: `{exp_name}_{timestamp}`
- Script: `exp/scripts/{exp_name}_{timestamp}.sh`
- Log:    `exp/logs/{exp_name}_{timestamp}.log`
- Log is written in real-time (no buffering with `> file 2>&1`)

**Step B — Early sanity check (20 seconds):**

Wait 20 seconds, then pull and read the first chunk of the log:
```bash
sleep 20
rsync -avz {ssh_alias}:{work_dir}/exp/logs/{log_name} ./exp/logs/
head -50 ./exp/logs/{log_name}
```

Check for:
- Import errors, missing modules → report immediately, no need to wait
- CUDA errors → report immediately
- Normal training output → proceed to Step C

**Step C — Wait for completion (event-driven):**
```bash
ssh {ssh_alias} '[ -f /tmp/{exp_name}_{timestamp}.exit ] && exit 0; \
  timeout {timeout} tmux wait-for {exp_name}_{timestamp}_done'
```

- smoke/quick: run inline (blocking), timeout 10min
- full experiment: `run_in_background: true`, timeout 24h
- multi-seed: one master waiter for all seeds, `run_in_background: true`

The script writes exit code before signaling:
```bash
# Add before tmux wait-for in script:
echo $? > /tmp/{exp_name}_{timestamp}.exit
```

**SSH disconnect recovery:**
```bash
ssh {ssh_alias} 'tmux has-session -t {exp_name} 2>/dev/null && echo RUNNING || echo DONE'
```
- RUNNING → re-run Step C with `run_in_background: true`
- DONE → read exit file, pull log

### Phase 6: Results

On `<task-notification>` (or after blocking wait):

```bash
# Read exit code
ssh {ssh_alias} 'cat /tmp/{exp_name}_{timestamp}.exit'

# Pull log
mkdir -p ./exp/logs
rsync -avz {ssh_alias}:{work_dir}/exp/logs/{log_name} ./exp/logs/

# Cleanup sentinel
ssh {ssh_alias} 'rm -f /tmp/{exp_name}_{timestamp}.exit'
```

- exit 0 → parse metrics from log, display results
- exit non-0 → show last 50 lines, diagnose error
- Pull result files only if needed (not the whole results/ dir)

## Multi-seed

Generate N scripts (one per seed), each with its seed hardcoded.
Launch all in one SSH call:
```bash
ssh {ssh_alias} '
  tmux new-session -d -s {exp_name}_s0 bash -c "bash {work_dir}/exp/scripts/{exp_name}_s0_{ts}.sh > {work_dir}/exp/logs/{exp_name}_s0_{ts}.log 2>&1"
  tmux new-session -d -s {exp_name}_s1 bash -c "bash {work_dir}/exp/scripts/{exp_name}_s1_{ts}.sh > {work_dir}/exp/logs/{exp_name}_s1_{ts}.log 2>&1"
  ...
'
```

Master waiter (one `<task-notification>` for all seeds):
```bash
ssh {ssh_alias} '
  for s in 0 1 2 3 4; do
    name={exp_name}_s${s}_{ts}
    [ -f /tmp/${name}.exit ] || tmux wait-for ${name}_done
  done
'
```
Run with `run_in_background: true`.

After all done: pull all logs, compute mean ± std across seeds.

## Directory Layout

```
{work_dir}/
└── exp/
    ├── scripts/   # bash scripts — synced by syncthing, version-controlled
    ├── logs/      # run logs — pulled back via rsync
    ├── results/   # experiment outputs — pulled on demand
    └── ckpts/     # checkpoints
```

## Quick Reference

```bash
# Check running sessions
ssh {ssh_alias} 'tmux ls'

# Tail a live log
ssh {ssh_alias} 'tail -f {work_dir}/exp/logs/{log_name}'

# Attach to session
ssh -t {ssh_alias} 'tmux attach -t {exp_name}'

# Kill a session
ssh {ssh_alias} 'tmux kill-session -t {exp_name}'

# GPU status
ssh {ssh_alias} 'nvidia-smi'
```
