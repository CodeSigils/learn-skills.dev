---
name: skill-evolver
description: "Use this meta-skill to proactively reflect on the effectiveness of other agent skills. MANDATORY: MUST be activated automatically after any specialized skill has completed its primary directive to perform a post-mortem, identify instruction gaps, and propose refinements. Triggered by requests like 'how did that go?' or 'do a post-mortem'. Enforces sandboxed evolution and interactive approval."
license: MIT
compatibility: Requires Python 3.10+ and the skill-evolver/scripts/ suite.
---

# skill-evolver

A meta-skill that proactively reflects on the effectiveness of other agent skills.

## Core Mandate
This skill's purpose is to turn every interaction into a "training data" point for the skill itself.
 It enforces the [Agent Skills](https://agentskills.io/) open standard and follows a rigorous cycle of:
0.  **Specification Refresh**: ALWAYS start by retrieving the latest specification from **https://agentskills.io/specification** using `web_fetch` to ensure total compliance with the latest standard before proposing refinements.
1.  **Post-Mortem Analysis**: Triggered automatically after a "Directive" is completed.
2.  **Instruction Gap Detection**: Identifying where the agent struggled.
3.  **Sandboxed Refinement**: ALL reflection analysis and test executions MUST be performed in a clean, isolated temporary workspace (e.g., `.gemini/tmp/evals/<skill-name>`) to prevent repository pollution.
4.  **Interactive Validation**: Generating an interactive review for the human user to approve or reject the proposed changes before they are applied.

**IMPORTANT**: All refinements MUST conform to the latest specification and best practices at **[agentskills.io](https://agentskills.io/)**.

---

## 1. Post-Mortem Analysis
When a task using a specialized skill is completed, the agent must:
- **Review Session History**: Specifically look for friction points (tool failures, user clarifications, multiple attempts at the same step).
- **Identify Under-Utilization**: Did the agent fail to use a tool that would have been more efficient?
- **Assess Alignment**: Did the agent's behavior deviate from the skill's instructions? If so, why?

## 2. Instruction Gap Detection
Analyze the `SKILL.md` of the skill just used to find:
- **Underspecification**: Did the agent have to guess where files were or what the convention was?
- **Over-Generalization**: Were the instructions too broad for the specific project context?
- **Tool Misalignment**: Did the skill suggest `read_file` when `grep_search` would have been better?

## 3. Surgical Refinement & Eval Generation
Propose improvements as follows:
- **Frontmatter**: Refine the `description` for better triggering.
- **Instructions**: Add clear, imperative commands to the `SKILL.md`.
- **The "Why"**: Include the reasoning behind the new instructions.
- **Eval Generation**: MUST generate a new `eval` test case in `evals/evals.json` that specifically targets the identified friction point to ensure no regressions.

## 4. Automation & Secure Review
To close the loop with the human user while maintaining high standards:
- **Isolated Execution**: Create a dedicated temporary directory for the evaluation run and result generation.
- **Security-First Approval**: Every review session MUST generate a unique `SESSION_TOKEN` to authenticate the approval callback via `scripts/approval_server.py`.
- **Render Review UI**: MUST run `python3 scripts/generate_review.py results.json ui/viewer.html review.html` to create an interactive dashboard.
- **Objective Diffs**: The dashboard MUST provide side-by-side diffs of proposed refinements to ensure human reviewers can objectively verify all changes.
- **Human-in-the-loop**: Provide the user with a direct link to `review.html` and wait for an explicit authenticated `approve` signal before modifying any `SKILL.md` files.

---

## Integration with gemini-skill-creator
- **Regression Testing**: Recommend running a full evaluation of the refined skill via `gemini-skill-creator` to ensure the new instructions are effective.

---

## Reporting & Feedback
ALWAYS provide a summary of the reflection:
- **Friction Points**: 1-2 specific areas where the interaction could have been smoother.
- **Proposed Diff**: A clear, actionable set of changes to the `SKILL.md`.
- **Review Link**: A direct path to the generated `review.html` for human approval.
