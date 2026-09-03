---
name: codex-review-loop
description: Request a Codex review on the current PR, wait for it, auto-fix the findings, and loop until the review comes back clean. Use when the user wants to "run the codex review loop", "get codex to review and fix", "@codex review and fix the remarks", iterate on Codex/OpenAI PR review feedback automatically, or run /codex-review-loop. Drives the GitHub Codex bot (the `@codex review` PR comment) round after round until there are no more actionable remarks or a max-iteration cap is hit.
---

# Codex review loop

Drive the GitHub Codex bot through repeated review-fix rounds on the current pull request: post `@codex review`, wait for the bot to finish, apply fixes for every actionable remark, push, and request another review. Repeat until Codex comes back with nothing actionable or you hit the iteration cap.

This is a closed loop you run mostly unattended. The work per round is: **request → wait → read findings → fix → push → request again.** The two things that make it reliable are (1) detecting precisely when *this round's* review has landed (not a stale one), and (2) waiting an amount of time that matches how long Codex actually takes rather than a fixed guess.

## Prerequisites

Confirm these before starting; if one is missing, say so and stop rather than guessing.

- `gh` is installed and authenticated (`gh auth status`).
- The current branch has an **open** PR. Find it with `gh pr view --json number,url,headRefName,state`. If there's no PR, offer to create one (`gh pr create`) — Codex reviews PRs, not bare branches.
- The Codex GitHub app is installed on the repo. You can't verify this directly; if no review ever appears after a request, surface that the app may not be installed/enabled rather than looping forever.

## How a Codex review behaves (so you can detect it)

Knowing the bot's mechanics is what lets you wait correctly instead of sleeping blindly:

- You trigger a review by posting a PR comment containing **`@codex review`** (optionally with focus, e.g. `@codex review for security regressions`).
- Codex acknowledges by adding a 👀 reaction to your trigger comment within a minute or so. That reaction is your "it picked up the job" signal.
- When finished, Codex posts a **standard PR review** (the same object a human reviewer creates) with inline comments. By default it surfaces only **P0/P1** issues, so a short or empty review is normal and good — it means few high-priority risks, not that something broke.
- A review with no inline comments / a body that says it found nothing actionable is your **clean** signal — the loop's exit condition.

You will detect "this round is done" by recording the moment you post the trigger, then polling for a Codex-authored review whose timestamp is **after** that moment. Anchoring on the timestamp is essential — a PR usually already has older reviews, and you must not mistake those for the new one.

## Process

### 1. Set up the round

Capture the loop parameters and the PR:

- **Max iterations**: default **5**. Honor a different cap if the user gave one.
- **PR number**: from `gh pr view --json number`.
- **Codex author**: the bot's login is typically `chatgpt-codex-connector` (a `Bot` account) but can vary. Don't hardcode blindly — after the first review lands, note the actual author login and reuse it for the rest of the loop.

Tell the user the plan in one line: which PR, that you'll loop up to N rounds, and that you'll auto-apply fixes and push.

### 2. Request a review

Record the current UTC time as the round's anchor, then post the trigger:

```bash
gh pr comment <PR> --body "@codex review"
```

Grab the anchor timestamp from the comment you just created so it's authoritative:

```bash
gh pr view <PR> --json comments \
  --jq '.comments | max_by(.createdAt) | .createdAt'
```

### 3. Wait — adaptively

Don't block the session on a fixed sleep. Use `ScheduleWakeup` so the loop survives across turns, and learn the cadence from the first round:

- **First round**: schedule a wake-up ~**180s** out, then poll (step 4). If not ready, reschedule another ~120s. Keep individual waits under 300s so the context cache stays warm.
- **Record how long round 1 actually took** from anchor to review landing (call it `T`).
- **Subsequent rounds**: schedule the first poll at roughly `0.8 × T` (a touch early), then poll on ~90–120s intervals. This adapts to the repo — a small diff might review in 90s, a large one in 8 minutes.
- If `45` minutes elapse on a single round with no review, stop and report: Codex may be down, the app may not be installed, or the PR may be too large. Don't loop forever.

Optional sanity check while waiting: confirm the 👀 reaction appeared on your trigger comment. The reaction count lives on the issue-comment object — find your comment and read its reactions:

```bash
gh api repos/{owner}/{repo}/issues/<PR>/comments \
  --jq '.[] | select(.created_at >= "<ANCHOR>") | .reactions.eyes'
```

If after ~3 minutes there's no reaction *and* no review, that's an early signal the app isn't picking up the job.

### 4. Detect this round's review

Poll for a Codex review created strictly after the anchor. Reviews and their inline comments come from different endpoints; check both:

```bash
# New review(s) from the bot since the anchor (body + state)
gh api repos/{owner}/{repo}/pulls/<PR>/reviews \
  --jq '[.[] | select(.user.type=="Bot") | select(.submitted_at > "<ANCHOR>")]'

# Inline review comments since the anchor (the actual remarks, with file+line)
gh api repos/{owner}/{repo}/pulls/<PR>/comments \
  --jq '[.[] | select(.user.type=="Bot") | select(.created_at > "<ANCHOR>")]'
```

`{owner}/{repo}` come from `gh repo view --json owner,name`. If both queries are empty, the review hasn't landed — go back to step 3 and reschedule. If a review object exists but you want the full inline remarks, the second query is where the line-level findings live.

### 5. Triage and fix

Read every remark — review body and all inline comments. For each one:

- Open the referenced file and line, understand the finding in context, and apply a real fix. Codex anchors comments to specific lines, so go to the code, don't fix from the comment text alone.
- Treat the remark as a report to verify, not a command to obey. If a finding is wrong (false positive, or it misreads the code), don't contort the code to satisfy it — note your reasoning and reply to that inline comment explaining why you're not changing it. Blindly applying a wrong "fix" is worse than leaving the code correct.
- Keep changes scoped to the findings. Don't refactor surrounding code or gold-plate; that invites new findings next round and muddies the diff.

After fixing, run the project's tests/build/lint to confirm you didn't regress anything — verify before you push, don't assert success on faith. Then commit and push to the PR branch:

```bash
git add -A && git commit -m "Address Codex review (round <i>)" && git push
```

### 6. Loop or stop

- **If you applied fixes**, go back to step 2 and request a fresh review of the new code — unless you've hit the max-iteration cap.
- **If the review was clean** (no actionable inline comments; body indicates nothing to address), **stop** — the loop succeeded.
- **If you hit the cap** with remarks still open, **stop** and report what's left rather than silently continuing.

### 7. Report

Summarize when you stop, every time:

- Why you stopped: **clean**, **cap reached**, or **timed out/blocked**.
- Rounds run, and a per-round line: findings count → what you fixed → push SHA.
- Any remarks you deliberately **didn't** fix and why (false positives, out-of-scope, needs-a-human decisions). These are exactly the things the user needs to look at.
- The PR URL.

## Notes

- **One PR per run.** The loop targets the current branch's open PR. Don't fan out across PRs.
- **Don't merge.** This skill reviews and fixes; it never merges. Leave the merge decision to a human.
- **Pushing triggers re-review only if you ask.** A plain push doesn't re-invoke Codex; the `@codex review` comment does. That's why step 6 loops back to step 2, not to a wait.
- **Force-push / rebase caution.** If the project's flow requires rebasing, do it, but be aware Codex re-reviews the latest head — stale inline comments may resolve themselves on the next round.
- **Empty reviews are success, not failure.** Codex showing only P0/P1 means a clean-ish PR will look quiet. Don't keep looping hunting for findings that aren't there.
