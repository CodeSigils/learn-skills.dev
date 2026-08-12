---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled — the questions you can ask _now_ without guessing at answers you haven't heard yet. Enumerate the whole frontier for yourself, then ask it **one question at a time**: post Q1 and stop. Wait for the user's answer. Only then post Q2.

**One question per message. No exceptions:**

- Don't post the round's numbered list — a list of questions is a batch, whatever you call it.
- Don't append "and also…" or a follow-up to the question you just asked.
- Don't bundle ("what about X, Y, and Z?"). That's three questions, so it's three turns.
- A question the last answer made moot gets dropped, not asked.

Each answer is feedback, not just data: it can retire later questions in the round, add ones you hadn't seen, or change how you'd word them. Batching forfeits all of that.

Each question should be formatted like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Once every question in the round has been answered, the user's answers reshape the tree — settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round, again one question at a time. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. Before you ask anything, check whether the answer is already in the codebase. If a question can be answered by reading the code, tests, config, git history, or docs, **go read them instead of asking**. Asking the user something you could have looked up spends their turn on your work, and their recollection is worse evidence than the file.

When the lookup is broad enough to be worth it, dispatch a sub-agent — and don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the report. Ask the rest of the frontier meanwhile.

The _decisions_ are the user's — put each to them and wait. The line: anything discoverable is yours to find; anything that's a preference, a priority, or a tradeoff call is theirs to make.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
