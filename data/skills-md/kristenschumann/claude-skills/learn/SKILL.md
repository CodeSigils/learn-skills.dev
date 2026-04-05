---
name: learn
version: 1.0.0
description: "Post-session retrospective: audits efficiency, proposes skill/memory/CLAUDE.md updates, and generates coaching feedback"
---
Learn from this session. Extract what went well, what went wrong, and update documentation so future sessions are better. Also give direct feedback on how the user can work with Claude more efficiently.

## Instructions

Parse $ARGUMENTS for optional focus area (e.g., `mistakes`, `efficiency`, `workflow`). If empty, do a full review.

### Step 0: Efficiency Audit (Elon's 5-Step Framework)

Before anything else, audit the work done in this session against each step in order:

**1. Make requirements less dumb**
- Were any requirements stated as facts that were actually assumptions? Who said this had to be done this way?
- Did requirements come from someone who isn't going to be accountable for the outcome?
- Flag any requirement that, in hindsight, was dumb, wrong, or unnecessary.

**2. Delete the part/process**
- What steps, outputs, or artifacts could have been eliminated entirely without losing value?
- Was anything produced that won't be used? Any process run "because we always do"?
- If you can't defend why something stayed, it should have been cut.

**3. Simplify or optimize the design**
- After deleting, what was still too complex?
- Were there cleaner paths to the same result? What added steps that didn't add value?

**4. Accelerate cycle time**
- Where did the session slow down? Waiting on tool results, iteration loops, back-and-forth?
- What would have made this 2x faster?

**5. Automate**
- What was done manually in this session that should be automated? (a skill, an n8n workflow, a memory update)
- Only after steps 1-4 — don't automate a dumb process.

Output this as a brief, opinionated table:

| Step | Finding | Verdict |
|------|---------|---------|
| Requirements | {what was dumb or necessary} | Cut / Keep |
| Deletions | {what could have been removed} | Should have cut |
| Simplify | {what was over-engineered} | Simplify next time |
| Speed | {where it slowed} | Fix: {suggestion} |
| Automate | {what to automate} | Skill / Sub-Agent / n8n / Memory |

### Step 1: Session Audit

Review the current conversation and identify:

**What went wrong:**
- Errors, dead ends, retries, or wasted steps
- Misunderstandings between user and Claude (unclear prompts, wrong assumptions)
- Tools that failed or returned unexpected results
- Approaches that were abandoned partway through

**What went well:**
- Efficient patterns (good use of parallel agents, clear prompts, smart sequencing)
- Decisions that saved time or tokens
- Workflows that should be repeated

**What was learned:**
- New facts about systems, data, processes, or tools
- Corrections to previous assumptions
- Patterns that should be codified

Summarize this back concisely before proceeding.

### Step 2: Documentation Updates — Skill vs. Memory Decision

For every insight from the session audit, classify it:

**Update a SKILL when:**
- A workflow was used and produced the wrong output or took extra steps
- A missing instruction caused Claude to go off-track during a skill execution
- A new edge case was discovered that a skill should handle
- A skill was invoked but the description didn't match (triggering issue)

**Update MEMORY when:**
- A new fact was learned about a system, tool, or data source
- A preference or convention was established that applies broadly
- A correction to a previous assumption (not tied to a specific skill)

**Create a NEW SKILL when:**
- You did something manually that took 3+ steps and will happen again
- You caught yourself giving Claude the same multi-step instruction twice
- A workflow emerged during the session that has a clear trigger and output

**Create a SUB-AGENT when:**
- A task is parallelizable — multiple independent workstreams that can run simultaneously
- A task is long-running and would flood the main context window with intermediate results
- A task requires autonomous tool use across many steps without needing user input mid-way
- The work is isolated enough that a fresh context (no session history) is an advantage, not a liability

**Skill vs. Sub-Agent decision rule:** If the work has a consistent *trigger + prompt template* → Skill. If the work requires *autonomous execution + tool calls + parallelism* → Sub-Agent. Many workflows need both: a Skill that *launches* a Sub-Agent.

**Update CLAUDE.md when:**
- A new "always do X" or "never do Y" rule was discovered
- A workspace routing rule changed
- A new MCP integration was added

For each proposed change, display:

| Change | Target | Type | Why |
|--------|--------|------|-----|
| {description} | {file path} | Skill edit / Memory / New skill / CLAUDE.md | {what happened} |

**Do NOT write any changes until the user approves.** Ask: "Want me to apply all of these, some of them, or none?"

### Step 3: Feedback for the User

Give direct, specific feedback on how the user can work with Claude more efficiently. Be honest — this is a coaching moment, not a compliment session.

Structure:

```markdown
## How to Get More Out of Claude

### Token Efficiency
{Were prompts unnecessarily long? Could context have been set once instead of repeated? Were there unnecessary back-and-forth cycles that a clearer initial prompt would have avoided?}

### Prompt Patterns
{What worked: e.g., "When you gave me the exact format you wanted, I nailed it first try."}
{What to try: e.g., "Next time you need X, try prompting with Y — it'll save a round trip."}

### Workflow Suggestions
{Could more work have been parallelized? Were there manual steps that could be skills? Did the user do something Claude should have done, or vice versa?}

### One Thing to Try Next Time
{The single highest-leverage change to how we work together.}
```

Be specific to THIS session. Reference actual moments. Don't give generic productivity advice.

### Step 4: Apply Approved Changes

After the user approves (all, some, or none):
- Write the approved memory files
- Edit the approved skill files
- Update CLAUDE.md if approved
- Confirm what was updated

### Step 5: AI Growth Prompt

Based on the session context, choose ONE of the following — pick whichever is more relevant:

**Option A — Study Prompt** (use when the session touched AI tools, models, workflows, or concepts that could go deeper):

Identify the most relevant AI concept from this session and suggest a specific resource to read. Format:

```markdown
## Learn Something

This session touched [concept]. Go deeper:

**Read:** [specific doc, post, or paper — link if you know it, otherwise describe exactly what to search for]
**Why it matters for your work:** [one sentence connecting it to courses, revenue, or automation]
**What to look for:** [the specific thing to extract from the read — a pattern, a technique, a mental model]
```

Use sources from: Anthropic docs (prompt engineering, tool use, agents), AI thought leaders (Andrej Karpathy, Simon Willison, Ethan Mollick, Lenny Rachitsky on AI), or recent AI news (if a specific model, tool, or capability was used that has notable coverage).

**Option B — Evaluation Question** (use when the session was mostly execution work — building, writing, analyzing):

Ask one hard question to evaluate whether the work was actually the right work. Choose from or riff on:

```markdown
## Honest Eval

[One of these, adapted to what actually happened:]

- Was any of this necessary? What would have happened if you hadn't done it?
- What's the single most questionable decision made in this session, and who challenged it?
- If you had to cut 40% of the output and keep only the most valuable, what survives?
- Did you solve the real problem, or the problem as originally stated?
- What assumption drove this session that you never actually validated?
```

Pick Option A only when the session genuinely introduced a new AI concept, capability, or tool that the user hadn't encountered before and could go deeper on. If the session used familiar AI tools in routine ways — even if it was a "capability" session — default to Option B. When in doubt, pick Option B.

## Notes

- This skill is most valuable after long or complex sessions where things didn't go smoothly
- The documentation updates are the durable output — they compound across future sessions
- Be honest in the feedback section. The user explicitly asked for this. Don't soften it.
- If the session went perfectly and there's nothing to learn, say so — don't manufacture feedback
- Never update documentation without showing the user first and getting approval
- When updating memory files, follow the memory system format (frontmatter with name, description, type)
