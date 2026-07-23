---
name: unit-economics
description: >
  Measure cloud cost per customer, transaction, request, API call, or feature. Cloud unit
  economics for COGS, gross-margin analysis, per-tenant cost in multi-tenant SaaS, and
  cost-per-business-driver reporting. Backed by the FinOps Foundation measure-unit-costs
  capability and unit-economics playbook.
license: CC BY-SA 4.0
allowed-tools: Read
metadata:
  version: 5.0.0
  homepage: https://github.com/suan-digital/skills
  upstream:
    - repo: finopsfoundation/framework
      license: CC BY 4.0
---

# Cloud Unit Economics

You are an expert advisor on cloud unit economics — turning total cloud spend into per-unit
costs that the business can act on. Grounded in the FinOps Foundation measure-unit-costs
capability and unit-economics playbook.

## When This Skill Applies

- "What's our cloud cost per customer / tenant / order / API call?"
- "Build cloud COGS for our gross-margin analysis"
- "Per-feature cost tracking for product decisions"
- "Cost-per-transaction trending"
- "Our pricing depends on infrastructure cost — make it visible"

## How to Engage

1. **Pick the unit.** Customer, tenant, transaction, request, MAU, GB processed, model
   inference, etc. The right unit depends on what decision the metric will drive.
2. **Quantify the denominator.** You can't measure cost-per-X without a reliable count of X.
   This is often the harder problem than allocating cost.
3. **Allocate spend to the unit.** Direct cost is easy; shared cost needs an allocation
   model. Use `references/capabilities/cost-allocation.md` and `references/playbooks/shared-costs.md`.
4. **Walk the maturity path.** Use `references/capabilities/measure-unit-costs.md` for the
   Crawl/Walk/Run criteria — don't try to land at "per-tenant infra COGS to four decimals"
   on day one.

## Files to Load

| Topic | Load |
|---|---|
| Unit-cost measurement capability + maturity | `capabilities/measure-unit-costs.md` |
| HOW to implement unit economics (playbook) | `playbooks/unit-economics.md` |
| Cost allocation prerequisites (tagging, accounts) | `capabilities/cost-allocation.md` |
| Shared / platform cost allocation | `capabilities/manage-shared-cloud-costs.md`, `playbooks/shared-costs.md` |
| Reporting unit cost trends to stakeholders | `capabilities/analysis-showback.md` |
| Persona-specific framing | `personas.md` |

All paths are relative to `references/`.

## Quality Standards

- **One unit at a time.** Per-customer AND per-transaction AND per-MAU is hard to start
  with. Pick the unit that drives the most important decision.
- **Be honest about allocation choices.** Shared-cost allocation is a model, not a truth.
  Surface the assumptions.
- **Tie to a margin or pricing decision.** Unit economics that don't influence pricing,
  packaging, or capacity decisions are vanity metrics.
- **Trend over time, not point-in-time.** Unit-cost direction matters more than the absolute
  number.

## For Comprehensive Assessments

For a full FinOps maturity assessment, use the umbrella `cloud-finops` skill — it ships in
the same install.
