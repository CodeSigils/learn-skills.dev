---
name: business-case
description: >
  Calculates financial business cases for applicable modernization scenarios.
  Computes per-application and portfolio-level costs, savings, and ROI using
  scenario finance configurations and complexity-based multipliers. Use when
  calculating modernization costs, estimating ROI, or building financial
  justification for transformation initiatives.
---

# Business Case

Calculate the financial impact of applicable modernization scenarios.

## Input

Read these files:
- `output/applications/consolidated_schema/consolidated_schema_application_<app_id>.json` — individual application JSON files
- `output/complexity_results/complexity_<app_id>.json` — per-application complexity scores
- `output/scenario_applicability_results/scenario_assessment_<app_id>.json` — per-application scenario applicability results
- `output/out_of_scope_results/out_of_scope_<app_id>.json` — in-scope filter
- `references/modernization_scenarios_finance.json` (bundled with this skill) — cost/savings definitions

Only include in-scope applications (`out_of_scope: false`) in financial aggregation.

## Finance config structure

Each scenario has a finance entry in `modernization_scenarios_finance.json`:

```json
{
  "scenario_id": "app_containerization",
  "costs": [
    { "type": "migration", "amount": 5000, "occurrence": "once", "scope": "per_application" }
  ],
  "savings": [
    { "type": "operational", "amount": 2000, "occurrence": "yearly", "scope": "per_application" }
  ]
}
```

## Calculation process

### Step 1: Filter applicable scenarios

Only calculate business cases for scenario-application pairs where `status == "APPLICABLE"`.
Read scenario ID from `scenarios_detailed[].id`.

### Step 2: Apply complexity multipliers

Adjust base costs using the application's complexity score from `complexity_score`.

**Cost multiplier (exponential):**

```
cost_multiplier = 0.5 * 1.15 ^ complexity_score
```

| Complexity | Multiplier | Meaning |
|------------|-----------|---------|
| 1 | 0.57x | Simple apps cost less to modernize |
| 3 | 0.76x | Below average cost |
| 5 | 1.01x | Roughly base cost |
| 7 | 1.33x | Above average cost |
| 10 | 2.02x | Complex apps cost ~2x the base |

**Savings multiplier (for Application-focus scenarios only):**

| Complexity | Multiplier |
|------------|-----------|
| 1-3 | 1.0x |
| 4-6 | 0.9x |
| 7-10 | 0.8x |

For non-Application-focus scenarios (OS, Database), savings are not adjusted.

### Step 3: Calculate per-scenario totals

For each applicable scenario-application pair:

```
adjusted_cost = base_cost * cost_multiplier    (one-time costs)
adjusted_savings = base_savings * savings_multiplier   (yearly savings)
```

### Step 4: Aggregate portfolio totals

Sum across all applications and scenarios:
- `total_one_time_costs`: Sum of all adjusted one-time costs
- `total_yearly_savings`: Sum of all adjusted yearly savings
- `roi_years`: total_one_time_costs / total_yearly_savings (break-even point)

## Output format

Save to `output/business_case_results/business_case.json`:

```json
{
  "assessment_date": "2025-01-15",
  "portfolio_summary": {
    "total_applications_assessed": 30,
    "applications_with_opportunities": 25,
    "total_applicable_scenarios": 87,
    "total_one_time_costs": 450000,
    "total_yearly_savings": 180000,
    "roi_years": 2.5
  },
  "scenarios_summary": [
    {
      "scenario_id": "app_containerization",
      "scenario_name": "Application Containerization",
      "applicable_count": 15,
      "total_cost": 120000,
      "total_yearly_savings": 45000,
      "roi_years": 2.67
    }
  ],
  "application_details": [
    {
      "app_id": "APP_001",
      "app_name": "Customer Portal",
      "complexity_score": 6,
      "scenarios": [
        {
          "scenario_id": "app_containerization",
          "base_cost": 5000,
          "cost_multiplier": 1.15,
          "adjusted_cost": 5750,
          "base_yearly_savings": 2000,
          "savings_multiplier": 0.9,
          "adjusted_yearly_savings": 1800
        }
      ],
      "total_cost": 12500,
      "total_yearly_savings": 5200,
      "roi_years": 2.4
    }
  ]
}
```

## Rules

- Round all monetary amounts to whole numbers.
- If finance config is missing for a scenario, skip financial calculation for that scenario but note it in the output.
- ROI in years should be rounded to 1 decimal place.
- If total yearly savings is 0, set `roi_years` to `null` (no payback).
