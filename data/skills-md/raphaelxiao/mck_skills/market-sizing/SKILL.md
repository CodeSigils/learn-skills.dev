---
name: market-sizing
description: Perform professional market sizing analysis (TAM/SAM/SOM) using Xiao Jing's structured methodologies (Demand-based, Supply-based, and Matching-based models). Use this skill when requested to estimate market sizes, industry scale, or company revenues from scratch without direct data.
---

# Market Sizing Skill

This skill provides workflows and computational tools to estimate market sizes systematically.

## Core Definitions

Before calculating, always define the metric you are solving for:
1. **TAM (Total Addressable Market)**: The theoretical maximum market size if 100% of the target market buys the product. Used in the **Introduction Phase** of an industry to judge the ultimate ceiling (e.g., VC threshold often >50B).
2. **SAM (Served Available Market)**: The portion of TAM that is currently being served by existing products/tech. Used in the **Growth Phase** to judge remaining penetration runway.
3. **SOM (Served Obtained Market)**: The actual slice of the market a specific company/store captures. Used in the **Mature Phase** to judge market share and concentration.

## The Three Methodologies

Select the appropriate method based on the goal:

1. **Demand-Based (Target: TAM/SAM)**: Calculate from the customer's perspective.
   - *Logic*: `Total Size = Target Customers × Penetration Rate × Annual Volume/Frequency × Unit Price`
   - *Reference*: See `references/demand_cases.md` for real-world examples (e.g., Pork consumption, Carpet household conversion).

2. **Supply-Based (Target: SOM / Single Entity)**: Calculate based on production/service bottlenecks.
   - *Logic*: Find the bottleneck step in the workflow -> calculate max output per hour -> split by active vs idle hours -> multiply by price.
   - *Reference*: See `references/supply_cases.md` for real-world examples (e.g., Mixue Bingcheng throughput).

3. **Matching-Based (Target: Mature markets / Complements)**: Calculate based on stable proxy ratios.
   - *Logic*: `Target Metric = Target Base / (Sample Base / Sample Metric)`
   - *Reference*: See `references/match_cases.md` for real-world examples (e.g., ATM density, coffee bean-to-berry proxy).

## Tools

Use the bundled script `scripts/calculator.py` to execute the math and avoid AI arithmetic errors.

**Demand Method:**
```bash
python3 scripts/calculator.py demand --customers <float> --penetration <float> --volume <float> --price <float>
```

**Supply Method:**
```bash
python3 scripts/calculator.py supply --bottleneck_sec <float> --active_hrs <float> --idle_hrs <float> --idle_mult <float> --price <float> [--days <float>]
```

**Match Method:**
```bash
python3 scripts/calculator.py match --source_base <float> --source_metric <float> --target_base <float> [--price <float>]
```

## Workflow

1. Identify if the user wants TAM, SAM, or SOM.
2. Select the correct Methodology (Demand, Supply, or Match).
3. If unsure how to construct the proxy or bottleneck, read the corresponding `references/<type>_cases.md` for Xiao Jing's original examples.
4. State assumptions clearly (e.g., "Assuming penetration is 40%").
5. Run the python script.
6. Perform a "Sense Check" on the final JSON output (is it logically possible?).
