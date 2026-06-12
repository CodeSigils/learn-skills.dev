---
name: financial-model
description: Use when building a startup financial model - captures revenue assumptions, builds a 3-year P&L projection, calculates burn rate and runway, models headcount, and produces a FINANCIAL-MODEL.md with scenario analysis and key assumptions, with user approval at each phase.
---

# Financial Model

## Overview

Builds a 3-year financial model in plain English and structured tables. You don't need a finance background. You do need to know your assumptions - this skill helps you find them, stress-test them, and present them clearly to investors.

Outputs a `FINANCIAL-MODEL.md` after all phases are approved.

## Prerequisites

Ask the user for:
- Business model (SaaS / marketplace / e-commerce / services)
- Current monthly revenue (or $0 if pre-revenue)
- Current monthly burn rate (how much you spend per month)
- Current cash balance (or how much you're raising)
- Team size today + planned hires

---

## Phase 1: Revenue Model

Define exactly how money comes in. Be specific about the assumptions.

**For SaaS:**

**Key inputs:**
- Number of new customers per month (Month 1: X, growing by Y% per month)
- Average revenue per customer per month (ARPU)
- Monthly churn rate (% of customers who cancel per month)

**Cumulative customer calculation:**
- Customers Month N = Customers (N-1) + New customers - Churned customers
- Churned = Customers (N-1) × Monthly churn rate

**Revenue calculation:**
- MRR Month N = Customers Month N × ARPU
- ARR = MRR × 12

**Expansion revenue** (if applicable):
- % of customers who upgrade per month
- Average expansion amount per upgrade

**For Marketplace:**
- GMV (gross merchandise volume) projection
- Take rate (% of GMV you keep)
- Revenue = GMV × Take rate

**For E-commerce:**
- Units sold per month
- Average order value
- Revenue = Units × AOV

**Build a monthly revenue table for Year 1:**

| Month | New customers | Churn | Total customers | MRR |
|-------|--------------|-------|-----------------|-----|
| 1 | | | | |
| ... | | | | |
| 12 | | | | |

**Year 2-3:** Switch to quarterly projections.

**Key assumption to justify:**
- "We'll acquire X new customers per month" - how? (channel + conversion rate math)
- "Churn will be X%" - based on what? (comparable companies, early data, or assumption)

**STOP.**
```
Phase 1 complete. Type APPROVE to build the cost model, or adjust revenue assumptions.
```

---

## Phase 2: Cost Model

**Cost categories:**

**Cost of Revenue (COGS) - costs that scale with revenue:**
- Hosting / infrastructure (% of revenue or fixed)
- Payment processing fees (typically 2.9% + $0.30 per transaction via Stripe)
- Customer support (if outsourced or per-ticket cost)
- Third-party APIs or services per customer

**Gross Margin = Revenue - COGS**
- Good SaaS gross margin: 70-80%+
- Marketplace: 40-60%
- E-commerce: 30-50%

**Operating Expenses (OpEx) - fixed or semi-fixed:**

**Headcount (largest cost for most startups):**
Build a hiring plan:

| Role | Start month | Annual salary | Monthly cost (including ~20% benefits/taxes) |
|------|-------------|---------------|---------------------------------------------|
| Founder 1 | Now | $X | $X |
| Founder 2 | Now | $X | $X |
| [Role] | Month X | $X | $X |

**Non-headcount OpEx:**
- Software / tools (Notion, Linear, Figma, AWS, etc.): $X/mo
- Marketing / ads: $X/mo (growing as you scale)
- Office / coworking (if applicable): $X/mo
- Legal / accounting: $X/mo
- Misc / travel: $X/mo

**Total monthly OpEx = Headcount + Non-headcount**

**STOP.**
```
Phase 2 complete. Type APPROVE to calculate burn rate and runway, or adjust costs.
```

---

## Phase 3: Burn Rate + Runway

**Monthly burn rate:**
- Pre-revenue: Burn = Total OpEx + COGS
- Revenue-generating: Net burn = Total OpEx + COGS - Revenue

**Build monthly P&L:**

| Month | Revenue | COGS | Gross profit | OpEx | Net burn (loss) | Cash balance |
|-------|---------|------|--------------|------|-----------------|--------------|
| 1 | | | | | | Starting cash |
| ... | | | | | | |

**Runway:**
- Runway (months) = Current cash / Monthly net burn
- Flag: When does cash run out? (the month cash balance hits $0)
- Flag: When should you start fundraising? (6 months before running out)

**Default alive / default dead:**
- Default alive: If costs stay flat and revenue grows at current rate, do you reach profitability before running out of cash?
- Default dead: If not, you need to either cut burn or raise money

**STOP.**
```
Phase 3 complete. Type APPROVE to run scenario analysis, or adjust the model.
```

---

## Phase 4: Scenario Analysis

Build three scenarios: conservative, base, and optimistic.

**Vary the key assumptions:**

| Assumption | Conservative | Base | Optimistic |
|------------|-------------|------|------------|
| Monthly new customers | | | |
| Monthly churn rate | | | |
| ARPU | | | |
| Month revenue growth begins | | | |

**For each scenario, show:**
- MRR at Month 12 / Month 24 / Month 36
- Months to profitability
- Total cash needed before profitability

**Sensitivity analysis:**
What's the biggest lever? Run "if we change just one assumption":
- If churn drops from 3% to 2%: [MRR impact at 24 months]
- If new customer growth is 50% lower: [runway impact]
- If ARPU increases by $10: [MRR impact at 24 months]

This tells you where to focus. Usually churn has a bigger long-term impact than new customer growth.

**STOP.**
```
Phase 4 complete. Type APPROVE to build the investor-facing summary, or adjust scenarios.
```

---

## Phase 5: Investor-Facing Summary

Summarize the model for a pitch deck or data room.

**Key metrics at 12/24/36 months (base case):**

| Metric | Month 12 | Month 24 | Month 36 |
|--------|----------|----------|----------|
| MRR | | | |
| ARR | | | |
| Total customers | | | |
| Gross margin % | | | |
| Monthly burn | | | |
| Headcount | | | |

**Use of funds (if raising):**

| Category | % of raise | Purpose |
|----------|------------|---------|
| Engineering / product | X% | [Specific hires] |
| Sales / marketing | X% | [Specific channels] |
| Operations | X% | [What] |
| Buffer | X% | Runway extension |

**Key milestones this raise funds:**
- Month X: [Revenue milestone]
- Month X: [Product milestone]
- Month X: Ready to raise Series [X]

**STOP.**
```
Phase 5 complete. Full financial model ready.
Type APPROVE to write the FINANCIAL-MODEL.md file, or revise any phase.
```

---

## Output

Write `FINANCIAL-MODEL.md` with all tables, assumptions, scenarios, and the investor summary.

## Financial Modeling Rules

- **Every number needs an assumption behind it.** "Revenue grows 20% month-over-month" → why? What's driving that?
- **Bottom-up beats top-down.** "We'll capture 1% of a $10B market" is not a model. Build from customer counts and conversion rates.
- **Investors know your Year 3 numbers are fiction.** They're evaluating your logic, not your precision.
- **Churn compounds.** A 5% monthly churn rate = 46% annual churn. Model it explicitly.
- **Headcount is your biggest variable.** Every hire is a 3-year decision when you factor in ramp time and severance risk.
- **Update the model monthly.** Replace assumptions with actuals as you learn. The model should get more accurate over time.
