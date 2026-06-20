---
name: monte-carlo
description: Run Monte Carlo simulation on portfolio strategy — distribution of outcomes, confidence intervals, risk of ruin. Use when the user wants to stress test the strategy or see probability-weighted outcomes.
disable-model-invocation: true
argument-hint: "[--simulations 1000] [--days 252] [--portfolio 1]"
allowed-tools: Bash(curl *) Bash(python *) Read
---

# Monte Carlo Simulation

Parameters: $ARGUMENTS

## Run via API

```bash
# Fetch Monte Carlo results (if already computed)
curl -s "http://localhost:5000/api/monte-carlo?portfolio_id=1"
```

## Run via Python (fresh simulation)

```bash
cd /home/photoprism/stock && source stock_trading_env/bin/activate
python -c "
from config import Config
from models.database import init_db, session_scope
from services.monte_carlo_simulator import MonteCarloSimulator

init_db(Config.DATABASE_URL)
sim = MonteCarloSimulator()
results = sim.run_simulation(portfolio_id=1, num_simulations=1000, num_days=252)
if results:
    print(f'Simulations:    {results.get(\"num_simulations\", 0)}')
    print(f'Time Horizon:   {results.get(\"num_days\", 0)} days')
    print()
    print(f'Expected Return: {results.get(\"expected_return\", 0):.1f}%')
    print(f'Median Return:   {results.get(\"median_return\", 0):.1f}%')
    print(f'Best Case (95):  {results.get(\"percentile_95\", 0):.1f}%')
    print(f'Worst Case (5):  {results.get(\"percentile_5\", 0):.1f}%')
    print(f'Risk of Ruin:    {results.get(\"risk_of_ruin\", 0):.1f}%')
    print(f'Max Drawdown:    {results.get(\"max_drawdown\", 0):.1f}%')
    print(f'Sharpe Ratio:    {results.get(\"sharpe_ratio\", 0):.3f}')
else:
    print('Simulation failed — check logs')
"
```

## Web Dashboard

The Monte Carlo results are also viewable at: `http://localhost:5000/monte-carlo`

## Present Results

1. **Distribution Summary**: Expected, median, best case (95th), worst case (5th)
2. **Risk Metrics**: Risk of ruin probability, max drawdown distribution
3. **Confidence Intervals**: 50%, 75%, 95% confidence bands
4. **Sharpe Distribution**: Range of Sharpe ratios across simulations
5. **Interpretation**: Is the strategy robust? What scenarios are dangerous?
6. **Recommendation**: Based on risk tolerance, should position sizes be adjusted?
