---
name: exploratory-data-analysis
description: Use when a dataset needs a first-pass inventory of distributions, concentrations, time patterns, and candidate next questions.
source: perlytics-skill
version: 1.0.0
---

# Exploratory Data Analysis

## Purpose

Understand a dataset's structure, distributions, concentrations, and notable patterns before any hypothesis-driven analysis begins.

## When to use

Use this skill when:

- a user shares a dataset with no specific analytical question ("analyze this CSV," "what's in here?")
- you need to understand what a dataset contains before choosing which analytical skill to apply
- the business context is unclear and the data itself needs to inform the direction
- a first look is needed to surface what questions the data is well-positioned to answer

## When not to use

Do not use this skill when:

- the analytical question is already specific and well-framed - proceed directly to the relevant skill
- data quality has not yet been checked - run `data-quality-check` first if the dataset is new and untested

## Required thinking discipline

- Describe first, conclude never. EDA surfaces patterns and candidate questions - it does not answer them.
- Do not force a narrative on the data. If nothing is surprising, say so.
- Surface concentrations and anomalies without explaining them - explanation requires hypothesis and evidence.
- End by recommending which analytical direction the data supports, not by stating what the data means.
- **Evidence constraint:** Every conclusion must cite specific data — a number, a rate, a segment, or a timeframe. Do not speculate without evidential basis. If data is insufficient, state what is missing rather than asserting an unsupported inference.

## Workflow

1. **Inventory:** Record the dataset dimensions (row count, column count, time range if a time column exists, primary entity if identifiable). State what each column appears to represent.

2. **Distribution summary:**
   - For numeric columns: range, approximate mean and median, skew direction, and whether extreme values exist.
   - For categorical columns: cardinality (how many unique values), top 5 values and their share, and whether there is a long tail.
   - Flag any column where one value dominates more than 80% of rows - this limits the column's usefulness for segmentation.

3. **Time patterns (if a time column exists):**
   - Does the data show a trend (directional movement over time)?
   - Are there periodic patterns (weekly, monthly, seasonal)?
   - Are there gaps, spikes, or drops that stand out?
   - What is the coverage period and grain?

4. **Concentration analysis:**
   - Which entity, segment, or value drives the most volume? (e.g., top 10% of customers drive X% of revenue)
   - Is the distribution highly skewed, or relatively flat?
   - Are there meaningful clusters or natural breakpoints visible?

5. **Co-movement check:**
   - Which numeric columns tend to move together across time or segments?
   - Are there obvious correlations that suggest a relationship worth investigating?
   - Note but do not explain - correlation here is a candidate for later investigation, not a finding.

6. **Surface candidate questions:** Based on what the data contains, list 3-5 specific analytical questions this dataset is well-positioned to answer. These become the input to the next analytical skill.

## Output format

- Dataset inventory (dimensions, entity, time range)
- Key distributions by column type
- Time patterns (if applicable)
- Concentration summary
- Notable co-movements
- Anomalies or surprises observed
- Candidate analytical questions (3-5)
- Recommended next skill

## Good example

Dataset: 12-month transaction file, 280,000 rows, columns: customer_id, order_date, product_category, revenue, country.

> Inventory: 280K orders, 45K unique customers, Jan-Dec, daily grain.
> Distributions: revenue is right-skewed (median $42, mean $89, top 1% > $800); product_category has 6 values, with "Electronics" driving 54% of revenue; country has 23 values, with US + UK + DE covering 78%.
> Time patterns: clear weekly seasonality (Friday-Saturday peak), revenue spike in November (likely promotional), slight downward trend in Q4 excluding the November spike.
> Concentration: top 10% of customers by spend account for 61% of total revenue.
> Candidate questions: (1) What drives the revenue gap between top and mid-tier customers? (2) Is the November spike sustainable or driven by one-time promotions? (3) Is Electronics growth masking weakness in other categories?
> Recommended next skill: root-cause-analysis for Q4 trend, or cohort-retention to understand whether high-value customers are returning.

## Bad example

> Customers are spending more on Electronics than other categories, which suggests you should invest more in Electronics.

Why this is bad:

- it jumps from a distribution observation to a strategic recommendation without any causal evidence
- it does not account for margin, growth trend, or customer quality
- it presents EDA as a conclusion, not as a starting point

## Practical notes

- EDA is the step between `data-quality-check` and a focused analytical skill. It does not replace either.
- If no anomalies or patterns are visible, say so - "the data appears unremarkable along these dimensions" is a valid EDA output.
- For very large datasets, sample stratified subsets for distribution checks rather than trying to summarize every row.
- Do not over-interpret distributions - a right-skewed revenue distribution is nearly universal in transaction data and is not itself a finding.

## Optional variants

- **Time-series focused EDA:** emphasize trend decomposition, seasonality detection, and anomaly flagging over static distributions.
- **Customer dataset EDA:** emphasize behavioral segmentation signals (recency, frequency, monetary), lifecycle stage distribution, and cohort diversity.
- **Operations dataset EDA:** emphasize process stage volumes, cycle time distributions, exception rates, and bottleneck indicators.
