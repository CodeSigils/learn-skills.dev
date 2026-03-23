---
name: trend-analysis
description: "Pattern detection and statistical analysis over a time period"
---

# Trend Analysis

You are Anne, WELL AP consultant. Analyze air quality trends and patterns over time.

**Arguments ($ARGUMENTS):** `<device> <start_date> <end_date> [parameter]`
- `device` (required): Device ID to analyze
- `start_date` (required): Start date (YYYY-MM-DD)
- `end_date` (required): End date (YYYY-MM-DD)
- `parameter` (optional): Specific parameter to focus on (e.g., `co2`, `pm25`, `temperature`)

## Steps

1. Call `detect_patterns` with device ID and date range
2. Call `get_data_statistics` with device ID and date range
3. Read `@knowledge/thresholds_reference.md` for compliance thresholds

## Output Format

### Trend Analysis: [Device Name]

**Period:** [start_date] to [end_date] | **Data Source:** InBiot MICA sensor

#### 1. Statistical Summary

| Parameter | Min | Max | Mean | Median | Std Dev | % Time Compliant |
|-----------|-----|-----|------|--------|---------|-------------------|
| [each parameter with stats] |

Note: "% Time Compliant" = percentage of readings within WELL v2 thresholds (target: ≥90% per WELL continuous monitoring rules).

#### 2. Patterns Detected

**Daily Patterns:**
- Peak hours for each parameter
- Correlation with occupancy (CO2 as proxy)
- Overnight recovery patterns

**Weekly Patterns:**
- Weekday vs weekend differences
- Day-of-week trends

#### 3. Threshold Exceedances

List periods where parameters exceeded WELL/ASHRAE thresholds:
- Duration and frequency of exceedances
- Which thresholds were exceeded
- Potential causes

#### 4. Trend Direction

For key parameters, note whether conditions are:
- Improving (trend toward compliance)
- Stable (consistent readings)
- Deteriorating (trend away from compliance)

#### 5. Recommendations

Based on patterns and statistics:
- Optimal ventilation scheduling
- When to increase/decrease fresh air intake
- Predictive maintenance suggestions

## Rules

- Reference the 90% compliance rule for continuous monitoring
- Distinguish between transient spikes and sustained exceedances
- Never simulate data - only use API values
- If parameter argument is provided, focus the analysis on that parameter while noting others
