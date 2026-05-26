---
name: baostock
description: BaoStock is a free, open-source A-share securities data platform providing historical K-line, financial statements, macroeconomic indicators, and industry classification data via Python API, returning pandas DataFrames.
---
# BaoStock

## Overview

BaoStock is a free, open-source securities data platform for China A-shares. It provides historical quotes, financial indicators, macroeconomic data, and industry classification through a unified Python API, returning pandas DataFrames.

**Key advantages**: Free, stable, long history (since 1990), no rate limits or credits required.

## Quick Start

### Installation

```bash
pip install baostock
```

### Basic Usage Pattern

```python
import baostock as bs
import pandas as pd

# 1. Login (required)
lg = bs.login()

# 2. Query data
rs = bs.query_history_k_data_plus(
    "sh.600000",
    "date,code,open,high,low,close,volume,amount",
    start_date="2024-01-01",
    end_date="2024-12-31",
    frequency="d",
    adjustflag="3",
)

# 3. Collect results (pandas 2.0+ compatible)
rows = []
while (rs.error_code == "0") and rs.next():
    rows.append(rs.get_row_data())
df = pd.DataFrame(rows, columns=rs.fields)

# 4. Logout
bs.logout()
```

### Stock Code Format

BaoStock uses `exchange.code` format (note the **dot** separator):

| Exchange | Prefix | Example |
|----------|--------|---------|
| Shanghai (SSE) | `sh.` | `sh.600000` (SPDB) |
| Shenzhen (SZSE) | `sz.` | `sz.000001` (Ping An Bank) |

## Parameter Conventions

- **Date**: `YYYY-MM-DD` (e.g., `2024-12-31`)
- **Stock code**: `sh.600000`, `sz.000001`
- **Return format**: Iterate via `rs.next()` + `rs.get_row_data()`, assemble into DataFrame
- **All return values are strings**: Must manually `pd.to_numeric()` for numeric columns

## Complete API Reference

### I. Market Data

#### 1. Historical K-line: `query_history_k_data_plus()`

**The most important API** — supports daily/weekly/monthly/minute bars with adjustment.

```python
rs = bs.query_history_k_data_plus(
    code="sh.600000",       # Stock code
    fields="date,code,...", # Return fields (comma-separated)
    start_date="2024-01-01",# Start date, default 2015-01-01
    end_date="2024-12-31",  # End date, default latest trading day
    frequency="d",          # Frequency
    adjustflag="3",         # Adjustment type
)
```

**frequency values**:

| Value | Frequency | Notes |
|-------|-----------|-------|
| `"d"` | Daily | Default |
| `"w"` | Weekly | |
| `"m"` | Monthly | |
| `"5"` | 5-minute | Index does not support minute bars |
| `"15"` | 15-minute | |
| `"30"` | 30-minute | |
| `"60"` | 60-minute | |

**adjustflag values**:

| Value | Meaning | Method |
|-------|---------|--------|
| `"3"` | Unadjusted | Default |
| `"1"` | Backward adjusted | Percentage change method |
| `"2"` | Forward adjusted | Percentage change method |

> **Note**: BaoStock uses the "percentage change adjustment method", which differs from other platforms (e.g., Tongdaxin).

**Daily/Weekly/Monthly fields**:

| Field | Description | Type |
|-------|-------------|------|
| `date` | Trading date | str |
| `code` | Stock code | str |
| `open` | Open price | str→float |
| `high` | High price | str→float |
| `low` | Low price | str→float |
| `close` | Close price | str→float |
| `preclose` | Previous close | str→float |
| `volume` | Volume (shares) | str→float |
| `amount` | Amount (CNY) | str→float |
| `adjustflag` | Adjustment flag | str |
| `turn` | Turnover rate (%) | str→float, empty string when suspended |
| `tradestatus` | Trading status | str, `"1"`=normal, `"0"`=suspended |
| `pctChg` | Price change (%) | str→float |
| `peTTM` | PE ratio (TTM) | str→float |
| `pbMRQ` | PB ratio (MRQ) | str→float |
| `psTTM` | PS ratio (TTM) | str→float |
| `pcfNcfTTM` | PCF ratio (TTM) | str→float |
| `isST` | Is ST stock | str, `"1"`=yes, `"0"`=no |

**Minute bar fields**:

| Field | Description |
|-------|-------------|
| `date` | Date |
| `time` | Time (format `YYYYMMDDHHmmssSSS`) |
| `code` | Stock code |
| `open` | Open price |
| `high` | High price |
| `low` | Low price |
| `close` | Close price |
| `volume` | Volume |
| `amount` | Amount |
| `adjustflag` | Adjustment flag |

> **Minute bars do not include index data or valuation metrics (peTTM, etc.).**

#### 2. Index K-line

Uses the same `query_history_k_data_plus()` API with index codes:

| Index | Code |
|-------|------|
| SSE Composite | `sh.000001` |
| SZSE Component | `sz.399001` |
| CSI 300 | `sh.000300` |
| CSI 500 | `sh.000905` |
| ChiNext Index | `sz.399006` |

> Index **does not support minute bars**, only daily/weekly/monthly.

#### 3. All Securities on Date: `query_all_stock()`

```python
rs = bs.query_all_stock(day="2024-12-31")
# Returns: code, tradeStatus columns
```

### II. Basic Information

#### 4. Stock Basic Info: `query_stock_basic()`

```python
rs = bs.query_stock_basic(code="sh.600000")  # Single stock
rs = bs.query_stock_basic()                   # All stocks
```

Returns: `code`, `code_name`, `ipoDate`, `outDate`, `type` (1=stock, 2=index, 3=other, 4=convertible bond, 5=ETF), `status` (1=listed, 0=delisted)

#### 5. Industry Classification: `query_stock_industry()`

```python
rs = bs.query_stock_industry(date="2024-12-31")  # Specific date
rs = bs.query_stock_industry()                     # Latest
```

Returns: `updateDate`, `code`, `code_name`, `industry`, `industryClassification`

> Uses **CSRC industry classification** standard.

#### 6. SSE 50 Constituents: `query_sz50_stocks()`

```python
rs = bs.query_sz50_stocks(date="2024-12-31")
```

Returns: `updateDate`, `code`, `code_name`

#### 7. CSI 300 Constituents: `query_hs300_stocks()`

```python
rs = bs.query_hs300_stocks(date="2024-12-31")
```

#### 8. CSI 500 Constituents: `query_zz500_stocks()`

```python
rs = bs.query_zz500_stocks(date="2024-12-31")
```

### III. Dividends & Adjustment

#### 9. Dividend Information: `query_dividend_data()`

```python
rs = bs.query_dividend_data(
    code="sh.600000",
    year="2024",
    yearType="report",  # "report"=announcement year, "operate"=ex-dividend year
)
```

Returns:

| Field | Description |
|-------|-------------|
| `dividPreNoticeDate` | Pre-notice date |
| `dividAgmPumDate` | AGM announcement date |
| `dividPlanAnnounceDate` | Plan announcement date |
| `dividPlanDate` | Implementation announcement date |
| `dividRegistDate` | Record date |
| `dividOperateDate` | Ex-dividend date |
| `dividPayDate` | Payment date |
| `dividStockMarketDate` | Stock listing date |
| `dividCashPsBeforeTax` | Cash dividend per share (before tax) |
| `dividCashPsAfterTax` | Cash dividend per share (after tax) |
| `dividStocksPs` | Stock dividend per share |
| `dividCashStock` | Dividend & transfer info |
| `dividReserveToStockPs` | Reserve to stock per share |

#### 10. Adjustment Factor: `query_adjust_factor()`

```python
rs = bs.query_adjust_factor(
    code="sh.600000",
    start_date="2015-01-01",
    end_date="2024-12-31",
)
```

Returns: `code`, `dividOperateDate`, `foreAdjustFactor`, `backAdjustFactor`, `adjustFactor`

### IV. Quarterly Financial Data

All quarterly APIs share the same parameters:

```python
rs = bs.query_xxx_data(code="sh.600000", year=2024, quarter=2)
```

- `code`: Stock code
- `year`: Fiscal year (int)
- `quarter`: Quarter (1/2/3/4)

#### 11. Profitability: `query_profit_data()`

Returns:

| Field | Description |
|-------|-------------|
| `code` | Stock code |
| `pubDate` | Publication date |
| `statDate` | Statistics end date |
| `roeAvg` | ROE (average, %) |
| `npMargin` | Net profit margin (%) |
| `gpMargin` | Gross profit margin (%) |
| `netProfit` | Net profit (CNY) |
| `epsTTM` | Earnings per share |
| `MBRevenue` | Main business revenue (CNY) |
| `totalShare` | Total shares |
| `liqaShare` | Tradable shares |

#### 12. Operating Efficiency: `query_operation_data()`

Returns: `NRTurnRatio` (receivables turnover), `NRTurnDays`, `INVTurnRatio` (inventory turnover), `INVTurnDays`, `CATurnRatio` (current asset turnover), `AssetTurnRatio` (total asset turnover)

#### 13. Growth: `query_growth_data()`

Returns: `YOYEquity` (equity YoY), `YOYAsset` (asset YoY), `YOYNI` (net income YoY), `YOYEPSBasic` (basic EPS YoY), `YOYPNI` (net income attributable to parent YoY)

#### 14. Solvency: `query_balance_data()`

Returns: `currentRatio`, `quickRatio`, `cashRatio`, `YOYLiability`, `liabilityToAsset`, `assetToEquity`

#### 15. Cash Flow: `query_cash_flow_data()`

Returns: `CAToAsset`, `NCAToAsset`, `tangibleAssetToAsset`, `ebitToInterest`, `CFOToOR`, `CFOToNP`, `CFOToGr`

#### 16. DuPont Analysis: `query_dupont_data()`

Returns: `dupontROE`, `dupontAssetSto498` (equity multiplier), `dupontAssetTurn`, `dupontPnitoni`, `dupontNitogr`, `dupontTaxBurden`, `dupontIntburden`, `dupontEbittogr`

#### 17. Express Report: `query_performance_express_report()`

Returns: `performanceExpPubDate`, `performanceExpStatDate`, `performanceExpRevenue`, `performanceExpDeductedNP`, `performanceExpNetProfit`, `performanceExpEPSChgPct`, `performanceExpROEChgPct`, etc.

#### 18. Forecast Report: `query_forecast_report()`

Returns: `profitForcastExpPubDate`, `profitForcastExpStatDate`, `profitForcastType` (increase/decrease/turnaround/first loss/continued profit/continued loss/slight increase/slight decrease/uncertain), `profitForcastAbstract`, `profitForcastChgPctUp`, `profitForcastChgPctDwn`

### V. Macroeconomic Data

#### 19. Deposit Rates: `query_deposit_rate_data()`

```python
rs = bs.query_deposit_rate_data(start_date="2020-01-01", end_date="2024-12-31")
```

Returns: `pubDate`, `depositType`, `depositRate`

#### 20. Loan Rates: `query_loan_rate_data()`

```python
rs = bs.query_loan_rate_data(start_date="2020-01-01", end_date="2024-12-31")
```

Returns: `pubDate`, `loanType`, `loanRate`

#### 21. Reserve Requirement Ratio: `query_required_reserve_ratio_data()`

```python
rs = bs.query_required_reserve_ratio_data(start_date="2020-01-01", end_date="2024-12-31")
```

Returns: `pubDate`, `effectiveDate`, `deposit` (large institution), `smallDeposit` (small institution)

#### 22. Money Supply (Monthly): `query_money_supply_data_month()`

```python
rs = bs.query_money_supply_data_month(start_date="2020-01", end_date="2024-12")
```

Returns: `statYear`, `statMonth`, `m0Month`, `m0YOY`, `m0ChainRelative`, `m1Month`, `m1YOY`, `m1ChainRelative`, `m2Month`, `m2YOY`, `m2ChainRelative`

#### 23. Money Supply (Annual): `query_money_supply_data_year()`

```python
rs = bs.query_money_supply_data_year(start_date="2020", end_date="2024")
```

Returns: `statYear`, `m0`, `m1`, `m2`

## Common Pitfalls

### 1. All return values are strings

BaoStock returns **all fields as strings**. You must convert manually:

```python
df["close"] = pd.to_numeric(df["close"], errors="coerce")
```

### 2. Empty string for turnover rate when suspended

Turnover rate returns `""` on suspended days. Direct `float()` conversion will fail:

```python
df["turn"] = pd.to_numeric(df["turn"], errors="coerce")  # "" → NaN
```

### 3. pandas 2.0+ compatibility

BaoStock internally uses `DataFrame.append()`, which was removed in pandas 2.0+. **You must manually collect data**:

```python
# BAD: rs.get_data() crashes on pandas 2.0+
df = rs.get_data()

# GOOD: Manual collection
rows = []
while (rs.error_code == "0") and rs.next():
    rows.append(rs.get_row_data())
df = pd.DataFrame(rows, columns=rs.fields)
```

### 4. login/logout prints to stdout

BaoStock's `login()` and `logout()` print messages to stdout. Suppress with:

```python
import os, contextlib
with open(os.devnull, "w") as devnull:
    with contextlib.redirect_stdout(devnull):
        bs.login()
```

### 5. Minute bar time field format

The `time` field in minute bars is `YYYYMMDDHHmmssSSS` (17-digit string):

```python
# "20240102093500000" → "2024-01-02 09:35:00"
t = "20240102093500000"
dt = f"{t[:4]}-{t[4:6]}-{t[6:8]} {t[8:10]}:{t[10:12]}:{t[12:14]}"
```

### 6. Adjustment method differs from other platforms

BaoStock uses the **percentage change adjustment method**, which produces slightly different absolute prices compared to Tongdaxin's fixed-point method.

### 7. Connection loss requires re-login

After network interruption or long idle time, BaoStock connections may expire. Add retry + re-login logic:

```python
try:
    rs = bs.query_history_k_data_plus(...)
except Exception:
    bs.logout()
    bs.login()
    rs = bs.query_history_k_data_plus(...)  # Retry
```

### 8. Index does not support minute bars

Index codes (e.g., `sh.000001`) return empty data for minute frequencies without error.

### 9. Limited ETF support

BaoStock has limited ETF data coverage. Consider using pytdx or tushare for ETF quotes.

## Official Resources

- Website: https://www.baostock.com
- API Docs: https://www.baostock.com/mainContent?file=pythonAPI.md
- GitHub: https://github.com/baostock/baostock
- PyPI: `pip install baostock`
