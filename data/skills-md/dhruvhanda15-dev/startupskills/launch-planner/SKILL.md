---
name: launch-planner
description: Use when planning a product launch - generates a phased go-to-market plan covering MVP definition, target audience, pricing, pre-launch checklist, launch day playbook, and post-launch strategy with user approval at each phase.
---

# Launch Planner

## Overview

Builds a complete, actionable launch plan in 6 phases. Each phase requires approval before proceeding. Works best after running `/idea-validator` and `/competitor-analysis`.

Outputs a `LAUNCH-PLAN.md` file in the project directory after all phases are approved.

## Prerequisites

Ask the user for:
- Product/idea summary (or pull from idea-validator output)
- Target launch date (if any)
- Budget range: bootstrapped / <$5k / $5k-$50k / funded
- Team size and roles

---

## Phase 1: MVP Definition

Define the smallest version that proves the core value and can be launched in the target window.

**Deliver:**
- The one core feature (singular) that makes or breaks the product
- What to cut for v1 (explicit list)
- What "done" looks like: the success metric for MVP ("we'll know it's working when...")
- Realistic build time estimate

**Ask the user to confirm the scope** - scope creep kills launches.

**STOP.**
```
Phase 1 complete. Type APPROVE to continue to Phase 2, or revise the MVP scope.
```

---

## Phase 2: Target Audience + Channel Strategy

Define exactly who the first 100 customers are and how to reach them.

**Customer profile:**
- Job title or role
- Company size or context
- The specific trigger event that makes them look for a solution right now
- Where they spend time online

**Channel recommendations:**

| Channel | Effort | Cost | Speed | Fit? |
|---------|--------|------|-------|------|
| Niche communities (Reddit, Discord, Slack) | Low | Free | Fast | |
| LinkedIn content | Medium | Free | Medium | |
| X/Twitter content | Low | Free | Medium | |
| Cold email/DM outreach | Medium | Free | Fast | |
| SEO/content marketing | High | Low | Slow | |
| Product Hunt launch | Medium | Free | One-time | |
| Hacker News (Show HN) | Low | Free | One-time | |
| Paid ads | Low | High | Fast | |
| Partnerships | High | Low | Slow | |

Recommend the top 2 channels based on audience and budget. Explain why.

**STOP.**
```
Phase 2 complete. Type APPROVE to continue to Phase 3, or revise the audience/channel strategy.
```

---

## Phase 3: Pricing Strategy

Research competitor pricing (web search if not already done), then recommend:

**Deliver:**
- Pricing model: per seat / usage-based / flat monthly / freemium
- Launch price with rationale (start low to get traction, or anchor high?)
- Free tier or trial structure (yes/no and why)
- Pricing table:

| Plan | Price | What's included |
|------|-------|-----------------|
| Free / Starter | $0 | ... |
| Pro | $X/mo | ... |
| Enterprise | Custom | ... |

- Future pricing trajectory (where does pricing go in 12 months?)

**STOP.**
```
Phase 3 complete. Type APPROVE to continue to Phase 4, or revise the pricing.
```

---

## Phase 4: Pre-Launch Checklist

A dated checklist of everything to complete before launch day, based on the user's timeline.

**Product:**
- [ ] Landing page live with email capture
- [ ] Core flow works end-to-end (tested by non-founder)
- [ ] Payment processing set up and tested
- [ ] Analytics installed (PostHog / Mixpanel / GA)
- [ ] Error monitoring set up (Sentry or equivalent)
- [ ] Mobile-responsive if relevant

**Users:**
- [ ] 5-10 beta users recruited and onboarded
- [ ] Feedback collected from at least 3 beta users
- [ ] At least one user has paid (even $1 proves intent)

**Marketing:**
- [ ] Launch content drafted (posts, Product Hunt listing, etc.)
- [ ] Social accounts set up and have posted at least once
- [ ] Email list with at least 50 subscribers (or plan to get them)

**Legal:**
- [ ] Privacy policy live
- [ ] Terms of service live
- [ ] Business entity formed (if needed for payments)

**Security:**
- [ ] Run `/security-review` before launch (critical step)

Generate with specific dates based on the user's target launch date.

**STOP.**
```
Phase 4 complete. Type APPROVE to continue to Phase 5, or adjust the checklist.
```

---

## Phase 5: Launch Day Playbook

Hour-by-hour plan for launch day.

**Where to post (in order):**
1. Product Hunt (12:01am PST for maximum voting window)
2. Hacker News Show HN (morning EST)
3. Relevant subreddits (check rules first - no spam)
4. Relevant Discord/Slack communities
5. Your personal LinkedIn and X/Twitter
6. Email your list
7. DM personal network asking for upvotes/shares

**Post templates to write:**
- Product Hunt tagline + description
- Hacker News Show HN post
- LinkedIn announcement
- X/Twitter thread opener
- Email to list

**Who to notify in advance:**
- Beta users (ask them to upvote/review on launch day)
- Advisors and investors
- Personal network (pre-write the DM to send launch morning)

**Metrics to watch live:**
- Sign-ups per hour
- Where traffic is coming from
- Conversion rate (visitor to sign-up)
- Any errors in Sentry

**How to handle the first support requests:**
- Respond within 1 hour on launch day
- Every support request = a product insight
- Log every question - it becomes your FAQ

**STOP.**
```
Phase 5 complete. Type APPROVE to continue to Phase 6, or revise the launch day plan.
```

---

## Phase 6: Post-Launch (30-Day Plan)

**Week 1: Listen**
- Talk to every single person who signs up (DM, email, or call)
- Do not build anything new - just listen
- Ask: "What made you sign up? What were you hoping it would do?"

**Week 2: Fix**
- Address the top 3 issues surfaced from user conversations
- Only build what multiple users asked for
- Ship fast - users who give feedback expect to see it addressed

**Week 3: Double down**
- Identify the one channel that's working best
- Put 80% of effort into that channel only
- Kill the channels showing no traction

**Week 4: Decide**
- Review the metrics against targets
- Decision point: iterate on current idea, pivot, or stop

**30-day targets to set now:**

| Metric | Target |
|--------|--------|
| Signed-up users | |
| Paying customers | |
| MRR | |
| NPS score | |
| Key learning | |

Recommend running `/marketing-planner` for the full ongoing marketing strategy.

**STOP.**
```
Phase 6 complete. Full launch plan ready.
Type APPROVE to write the LAUNCH-PLAN.md file, or revise any phase.
```

---

## Output

After final approval, write a `LAUNCH-PLAN.md` file in the current project directory containing all phases, checklists, templates, and targets from this session.
