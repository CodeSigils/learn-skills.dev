---
name: run-experiment
description: Submit or run an ML experiment on a compute environment (local, SLURM HPC, RunAI/Kubernetes). Use when the user wants to launch a training run, submit a job, run ablations, or execute an experiment script on any compute cluster.
argument-hint: "[--env <local|ibex|uw|runai|...>] [--script <path>] [--name <job-name>] [--gpus <N>]"
allowed-tools: Read, Write, Bash, Glob
---

# Run Experiment

Submit an ML experiment to a compute environment — local machine, SLURM HPC (Ibex, UW, etc.), or RunAI/Kubernetes (EPFL).

Generates a **reproducible job script** in `jobs/` that is committed alongside the code, then provides the exact submit command to run.

Pair this skill with `research-project-memory` when a launched job should be linked to a planned experiment, evidence item, worktree, or project action.

Terminology:

- `local`: the machine where the agent is running, usually the user's Mac
- `Git remote`: GitHub/GitLab remote used for code sync, such as `origin`
- `server`: SSH/HPC/RunAI execution environment such as `quest`, `ibex-vscode`, or `epfl-haas`

When launching on SLURM or RunAI, call it a server run rather than a remote run unless referring to the Git remote.

## Skill Directory Layout

```
<installed-skill-dir>/
├── SKILL.md
├── environments.yaml        # Environment profiles (extend for new clusters)
└── templates/
    ├── slurm_job.sh         # SLURM template (Ibex, UW, any SLURM cluster)
    ├── runai_job.sh         # RunAI/Kubernetes template (EPFL)
    └── local_run.sh         # Local tmux/nohup template
```

---

## Steps to Follow

### 1. Read the environment registry

Resolve `<installed-skill-dir>` as the directory containing this `SKILL.md`, then read `<installed-skill-dir>/environments.yaml`.

List the available environments to the user with a one-line description each.

### 2. Ask for experiment details

Ask the user **in a single message**:

1. **Environment**: Which compute env? (show available choices from environments.yaml + "other")
2. **Script / command**: What command to run? (e.g., `uv run python train.py --lr 1e-3`)
3. **Job name**: Short identifier (e.g., `baseline-cifar10`, `ablation-no-attn`). Default: script basename + date.
4. **GPU count**: How many GPUs? (default from env profile, 0 for CPU-only)
5. **Walltime / time limit**: (SLURM only) How long? (default from env profile)
6. **Conda env or venv**: Name of the conda environment, or `.venv` path (if applicable)
7. **Output directory**: Where to save checkpoints/results? (default: `outputs/<job-name>/`)
8. **Anything special?**: Extra env vars, array job, specific GPU type, PVC mounts (RunAI), etc.

If `--env`, `--script`, `--name`, or `--gpus` were passed as arguments, pre-fill those answers.

### 3. Locate the project root

```bash
git rev-parse --show-toplevel 2>/dev/null || pwd
```

Also capture the short git commit hash:
```bash
git rev-parse --short HEAD 2>/dev/null || echo "no-git"
```

### 4. Generate the job script

Based on the environment type:

#### type: slurm (ibex, uw, or any SLURM cluster)

Read the SLURM template from `<installed-skill-dir>/templates/slurm_job.sh`.

Fill in all `{PLACEHOLDER}` variables:

| Placeholder | Value |
|---|---|
| `{PROJECT}` | project directory name |
| `{ENV_NAME}` | environment key (e.g., `ibex`) |
| `{ENV_DISPLAY}` | display name from profile |
| `{DATE}` | today's date YYYY-MM-DD |
| `{COMMIT}` | short git SHA |
| `{JOB_NAME}` | user-provided job name |
| `{SCRIPT_NAME}` | filename of the generated script |
| `{PARTITION}` | from env profile defaults (or user override) |
| `{CPUS}` | cpus_per_task from profile (or user override) |
| `{GPUS}` | user-provided GPU count |
| `{MEM}` | from profile defaults (or user override) |
| `{WALLTIME}` | user-provided or profile default |
| `{LOG_DIR}` | `outputs/logs/<job-name>` |
| `{OUTPUT_DIR}` | `outputs/<job-name>` |
| `{PROJECT_ROOT}` | absolute project root path |
| `{CONDA_ENV}` | user-provided env name |
| `{RUN_COMMAND}` | user-provided command |
| `{SCRATCH}` | scratch path from env profile |

Uncomment the relevant `module load` lines based on the env profile's `common_modules`.
Uncomment the `conda activate` or `source .venv/activate` line based on user's answer.
If scratch path is in the env profile, uncomment the TMPDIR block.

**Output path**: `jobs/<job-name>.sh`

#### type: runai (runai profile)

Read the RunAI template from `<installed-skill-dir>/templates/runai_job.sh`.

Fill in placeholders:

| Placeholder | Value |
|---|---|
| `{PROJECT}` | project directory name |
| `{DATE}` | today's date |
| `{COMMIT}` | short git SHA |
| `{JOB_NAME}` | user-provided job name |
| `{SCRIPT_NAME}` | filename of generated script |
| `{IMAGE}` | from env profile `default_image` (ask user to confirm) |
| `{RUNAI_PROJECT}` | from env profile `project` |
| `{GPUS}` | GPU count |
| `{CPUS}` | CPU count from profile defaults |
| `{MEM}` | memory from profile defaults |
| `{PVC_FLAGS}` | generated from `pvc_mounts` in profile: `--pvc claim:path \` per mount |
| `{RUN_COMMAND}` | user-provided command |

**Output path**: `jobs/<job-name>-runai.sh`

#### type: local

Read the local template from `<installed-skill-dir>/templates/local_run.sh`.

Fill in placeholders similarly. Uncomment conda/venv activation as appropriate.

**Output path**: `jobs/<job-name>-local.sh`

#### type: other / unknown

If the user specifies an environment not in `environments.yaml`:

1. Ask: "What scheduler does it use? (slurm / runai / other)"
2. If SLURM-compatible: use the SLURM template with the info the user provides.
3. If truly novel: generate a minimal generic wrapper and explain what to fill in.
4. Suggest: "Want me to add this environment to `environments.yaml` for future use?"

### 5. Write the job script and preview

Create the job script directory, log directory, and output directory before previewing or submitting:
```bash
mkdir -p <project-root>/jobs
mkdir -p <project-root>/outputs/logs/<job-name>
mkdir -p <output-dir>
```

Write the filled-in script to `jobs/<job-name>.sh` (or `-runai.sh` / `-local.sh`).

Show the user the full generated script for review.

### 6. Show the submit command and ask to launch

Print the exact command(s) to submit, tailored to the environment:

#### SLURM (Ibex / UW / etc.)

```
# If you're already on the login node:
sbatch jobs/<job-name>.sh

# If submitting from your local machine to a server (requires ssh access):
scp jobs/<job-name>.sh <ssh-alias>:<project-root>/jobs/
ssh <ssh-alias> "cd <project-root> && mkdir -p outputs/logs/<job-name> <output-dir> jobs && sbatch jobs/<job-name>.sh"

# Monitor:
squeue -u $USER
sacct -j <jobid> --format=JobID,State,Elapsed,AllocGRES
tail -f outputs/logs/<job-name>/slurm-<jobid>.out
```

#### RunAI

```
bash jobs/<job-name>-runai.sh

# Monitor:
runai list
runai logs <job-name> -f
```

#### Local

```
# Attached (output in terminal):
bash jobs/<job-name>-local.sh

# Detached in tmux:
tmux new-session -d -s <job-name> "bash jobs/<job-name>-local.sh"
tmux attach -t <job-name>

# Background with nohup:
nohup bash jobs/<job-name>-local.sh &
```

Ask: **"Want me to run the submit command now?"**

- If yes and local: run it directly.
- If yes and server: run the `scp` + `ssh sbatch` command (requires ssh key auth to be set up).
- If no: remind the user that the script is saved in `jobs/` and ready to submit.

### 7. Offer to add to jobs index (optional)

If a `jobs/README.md` or `jobs/index.md` exists, offer to append a one-line entry:
```
| {DATE} | {JOB_NAME} | {ENV_NAME} | {COMMIT} | {RUN_COMMAND_BRIEF} |
```

If the repo follows the code evidence layout from `init-python-project`, also offer to create or update a short run pointer under:

```text
docs/runs/<DATE>-<job-name>.md
```

This file should contain the command, config, commit, output path, expected metric, and monitor command. It should not contain raw logs.

### 8. Update project memory when present

If the repo has `memory/` or a worktree `.agent/worktree-status.md`, update only verified run pointers:

- `memory/evidence-board.md`: add or update the linked `EXP-###` with job script path, commit, command, output directory, and status `planned`, `submitted`, or `running` only if verified
- `docs/runs/`: write a small run pointer when the code repo uses that convention
- `memory/action-board.md`: mark the launch action as `doing` or create a monitor action
- `memory/current-status.md`: record the latest known job and what must be checked next
- `<worktree>/.agent/worktree-status.md`: link the run to the worktree purpose and exit condition

Do not store queue state, job success, or final metric values as durable facts unless they were verified in this session. Use `needs-verification` for monitor tasks.

---

## Environment Reference

All environments are defined in `environments.yaml`. The current known environments:

| Key | Type | Cluster | Notes |
|---|---|---|---|
| `local` | local | — | Current machine, tmux/nohup |
| `ibex` | slurm | KAUST Ibex | `ilogin.ibex.kaust.edu.sa`; gpu/batch/himem partitions |
| `uw` | slurm | UW HPC | Placeholder — update `environments.yaml` with actual details |
| `runai` | runai | EPFL RunAI | Kubernetes; update project/image in `environments.yaml` |

### Adding a New Environment

Edit `<installed-skill-dir>/environments.yaml` and add a block:

```yaml
my-cluster:
  type: slurm                       # or runai / local
  display_name: "My University HPC"
  login_node: "login.cluster.edu"
  ssh_alias: mycluster
  scheduler: slurm
  partitions:
    gpu:
      name: gpu
      flag: "--partition=gpu"
      gpu_flag: "--gres=gpu:{count}"
      max_gpus_per_job: 4
  defaults:
    partition: gpu
    gpus: 1
    cpus_per_task: 4
    mem: "32G"
    walltime: "12:00:00"
    max_walltime: "48:00:00"
  storage:
    home: "/home/{user}"
    scratch: "/scratch/{user}"
  module_system: lmod
  common_modules:
    - "cuda/12.1"
    - "python/3.11"
  notes: "..."
```

---

## Reproducibility Conventions

Every generated job script includes:
- **Git commit hash** in the header and as an env var (`GIT_COMMIT`)
- **Structured output directory**: `outputs/<job-name>/` for checkpoints, `outputs/logs/<job-name>/` for logs
- **Timestamped log files** so reruns don't overwrite
- **Exit code propagation** so job arrays and downstream scripts detect failures

The `jobs/` directory should be committed to git (the scripts are small text files). Actual outputs go to `outputs/` which is typically `.gitignore`d.

---

## Example Invocations

```
/run-experiment                                              # interactive wizard
/run-experiment --env ibex --script train.py --gpus 2
/run-experiment --env local --script eval.py --name eval-baseline
/run-experiment --env runai --gpus 4 --name big-run
/run-experiment --env ibex --script sweep.py --name sweep --gpus 1
```

---

## Common Patterns

### Job Array (SLURM) — hyperparameter sweep

When the user says "I want to sweep over N configs":

1. Ask for the sweep configs or config file (e.g., `configs/sweep.yaml` with N entries).
2. Add `#SBATCH --array=0-{N-1}%{max_concurrent}` to the script.
3. Add to the run command: `--config configs/sweep.yaml --config-idx $SLURM_ARRAY_TASK_ID`
4. Output dir: `outputs/<job-name>/$SLURM_ARRAY_TASK_ID/`

### Multi-GPU (DDP)

When GPUs > 1 and the env is SLURM:

- Add `--ntasks-per-node={GPUS}` directive
- Wrap command with `torchrun --nproc_per_node={GPUS}` or `srun python -m torch.distributed.launch`
- Ask the user which distributed launcher they use

### Interactive Session (Debugging)

When the user wants to debug interactively (not submit a batch job):

**Ibex**:
```bash
srun --partition=gpu --gres=gpu:1 --cpus-per-task=4 --mem=32G --time=2:00:00 --pty bash
```

**RunAI**:
```bash
runai submit <name> --image <image> --gpu 1 --interactive --stdin -- bash
runai bash <name>
```

Generate this command directly without creating a script file.
