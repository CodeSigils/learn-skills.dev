---
name: data-quality-check
description: Use when a dataset, CSV, table, or export needs a structured reliability check before downstream interpretation.
source: perlytics-skill
version: 1.0.0
---

# Data Quality Check

## Purpose

Assess data reliability before any analysis begins so that findings are not built on faulty foundations.

## When to use

Use this skill when:

- you receive a new dataset, CSV, table, or export for analysis
- a metric or finding seems suspicious and the data source has not been audited
- a downstream analysis (root cause, funnel, retention, experiment) depends on the integrity of a specific dataset
- a stakeholder is asking for insights from data whose quality is unknown

Always run this skill before applying any analytical skill to a new data source.

## When not to use

Do not use this skill when:

- the dataset has been audited recently and the quality is documented and trusted
- the task is purely mechanical transformation on a known-good dataset

## Required thinking discipline

- Never interpret data you have not audited.
- Surface all quality issues before drawing any conclusions.
- Assign a trust level explicitly - do not leave quality assessment implicit.
- When quality issues are found, state what analysis is still possible and what is not.
- **Evidence constraint:** Every conclusion must cite specific data — a number, a rate, a segment, or a timeframe. Do not speculate without evidential basis. If data is insufficient, state what is missing rather than asserting an unsupported inference.

## Workflow

1. **Schema audit:** Check column names, data types, and expected vs. actual structure. Are columns named consistently? Are types correct (dates stored as strings, IDs stored as floats)?

2. **Completeness check:** Calculate the null and missing value rate per column. Note whether missingness is random, concentrated in a time range, or concentrated in specific segments. Distinguish "null" (no data) from "zero" (an actual value of zero).

3. **Duplicate detection:** Check for duplicate rows at the full-row level and at the expected primary key level. Duplicates on order IDs, user IDs, or event IDs will silently inflate any aggregate.

4. **Outlier and range check:** Identify values outside plausible business bounds. A revenue column with negative values, an age column with values over 150, or a percentage column over 100 are signals of data issues, not just outliers.

5. **Referential integrity:** If the dataset has join keys (user_id, account_id, product_id), check whether they match the expected reference table. Orphaned records (keys that exist in the fact table but not the dimension) will silently drop rows in joins.

6. **Date and time consistency:** Check for timezone ambiguity (are timestamps UTC or local?), format inconsistencies (YYYY-MM-DD vs. MM/DD/YYYY in the same column), gaps in expected time series, and future-dated records.

7. **Assign trust level:**

| Trust level | Meaning |
|---|---|
| High | No material issues found. Analysis can proceed without caveats. |
| Medium | Issues exist but are manageable with documented exclusions (e.g., exclude nulls, deduplicate on key). Analysis can proceed with stated caveats. |
| Low | Significant issues affect a material portion of records. Analysis conclusions must be heavily qualified. |
| Unusable | Issues are pervasive or the data cannot be linked to the intended entity. Do not proceed until the source is fixed. |

## Output format

- Dataset inventory (row count, column count, time range, primary key)
- Quality issues by dimension (completeness, duplicates, outliers, referential integrity, date consistency)
- Trust level with justification
- Recommended caveats for any downstream analysis
- Recommended exclusions or transformations before analysis

## Good example

Dataset: 90-day order export, 142,000 rows.

> Schema: revenue column is stored as VARCHAR, not numeric - requires casting.
> Completeness: shipping_country is null for 23% of rows, concentrated in orders before March 1 (likely a migration gap).
> Duplicates: 1,847 duplicate order_id values - likely split shipments sharing an order ID. Aggregate on order_id will double-count revenue.
> Outliers: 12 rows with revenue > $50,000 - confirm whether these are B2B bulk orders or data errors.
> Trust level: Medium.
> Recommended caveats: deduplicate on order_id using max(revenue) per order, exclude pre-March rows from geographic analysis, confirm high-value outliers with the source team before including in revenue totals.

## Bad example

> The data looks fine. Here are the key insights from the CSV.

Why this is bad:

- no quality check was performed
- null rates, duplicates, and outlier risk are invisible
- any insight is built on an untested foundation
- if quality issues exist, the conclusions could be wrong and there is no record of the risk

## Practical notes

- For large datasets, sample 1,000-5,000 rows for a fast initial quality scan before running checks on the full dataset.
- If a column has more than 40% nulls, ask whether the column is even usable for the intended analysis - high missingness often indicates that the field was not collected systematically.
- Duplicate detection should happen at the intended analysis grain, not just full-row. A full-row duplicate is one thing; a duplicate at the order or user level is a different problem that affects aggregation.
- Always note when data quality issues are concentrated in a specific time range - this often points to a pipeline change, backfill, or system migration.

## Optional variants

- **Pre-experiment data check:** run before an A/B test to confirm event logging is stable and the expected sample split matches the design.
- **Dashboard data check:** run on the underlying data source powering a dashboard before trusting its numbers.
- **Join validation:** when combining two tables, check the match rate and understand what happens to unmatched records (inner join silently drops them).
