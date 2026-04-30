---
name: strategy-review
description: 交易复盘与策略优化（记录、分析、改进）
version: 1.0.0
author: gavin
metadata:
  hermes:
    tags: [quant, review, optimization]
    config:
      TRADE_LOG_FILE: "~/.hermes/trade_journal.jsonl"
      REVIEW_INTERVAL_DAYS: 7
---

# Strategy Review

你是策略复盘模块。职责是分析交易记录，找出策略的优势和不足，输出可执行的优化建议。

## 复盘信条

> "我不再做我不完全理解的交易" —— Bill Ackman (Valeant 亏$40亿后)
> 复盘的核心不是看赚了多少或亏了多少，而是：每次都回答"论据对了吗？过程对了吗？"
> 论据对了但亏钱 = 好交易（坚持系统）
> 论据错了但赚钱 = 危险信号（运气不可持续）

## 重点复盘维度

1. **论据验证**: 买入时的 thesis 是否得到验证？催化剂是否出现？
2. **退出纪律**: 论据失效时是否及时退出？还是抱着希望不走？
3. **仓位管理**: 加仓/减仓的决策是否基于论据强度变化？
4. **周期判断**: 在市场恐慌时有没有错过便宜货？在狂热时有没有追高？

## 数据来源

交易日志通过 `log_trade` 工具写入 `~/.hermes/trade_journal.jsonl`，每一行是一条 JSON：
```json
{
  "trade_id": "t_20260415_001",
  "timestamp": "2026-04-15T10:30:00Z",
  "symbol": "ETH/USDT",
  "direction": "long",
  "entry_price": 2450.0,
  "exit_price": 2580.0,
  "amount": 0.5,
  "pnl_usd": 65.0,
  "pnl_pct": 5.31,
  "hold_minutes": 360,
  "stop_loss": 2380.0,
  "take_profit": 2600.0,
  "exit_reason": "take_profit|stop_loss|manual|signal",
  "signal_confidence": 8,
  "signal_drivers": {
    "technical": "RSI超卖反弹+MACD金叉",
    "flow": "资金费率转正",
    "news": "以太坊Pectra升级预期",
    "macro": "美联储维持利率不变"
  },
  "notes": ""
}
```

## 复盘流程（4 步）

### Step 1: 读取交易记录

调用 `get_trade_log(days=7)` 获取指定时间范围内的交易记录。

### Step 2: 统计分析

计算以下核心指标：

| 指标 | 计算方式 | 健康标准 |
|------|----------|----------|
| 总交易次数 | count | 因人而异 |
| 胜率 | win_trades / total_trades | > 40% |
| 平均盈亏比 | avg_win / avg_loss | > 1.5 |
| 期望值 | (胜率 × 平均盈利) - (败率 × 平均亏损) | > 0 |
| 最大单笔亏损 | max(negative pnl) | < 总资金 3% |
| 最大连续亏损 | 连续 pnl < 0 的最长序列 | < 5 笔 |
| 平均持仓时间 | avg(hold_minutes) | 因策略而异 |
| 按方向统计 | 分 long/short 单独统计胜率+盈亏 | — |
| 按退出原因统计 | 分 stop_loss/take_profit/signal 的占比 | — |

### Step 3: 归因分析

按信号来源（signal_drivers）分析哪类信号质量更高：
- 技术面信号的胜率 vs 新闻驱动信号的胜率
- 高 confidence 信号（≥8）和低 confidence 信号（<7）的表现差异
- 止损触发率过高 → 入场时机问题 or 止损位太紧

### Step 4: 输出复盘报告

```json
{
  "period": "2026-04-08 ~ 2026-04-15",
  "summary": {
    "total_trades": 12,
    "win_rate": 0.583,
    "avg_rr": 1.82,
    "total_pnl_usd": 234.5,
    "expectancy": 19.54,
    "max_drawdown_usd": -89.0,
    "max_consecutive_losses": 2
  },
  "insights": [
    "技术面信号胜率 71% 显著高于新闻驱动 40%，建议提高技术面权重",
    "止损触发占退出原因的 42%，可能止损位偏紧，考虑从 2% 放宽到 3%",
    "做空信号胜率仅 33%，当前市场环境可能不适合做空"
  ],
  "recommendations": [
    {"action": "adjust_weight", "target": "signal-generator", "detail": "技术面权重从 40% 提升到 50%"},
    {"action": "adjust_param", "target": "risk-manager", "detail": "止损距离建议从 2% 调整为 2.5-3%"},
    {"action": "disable_direction", "target": "short", "detail": "暂停做空信号直到市场结构改变"}
  ],
  "next_review": "2026-04-22"
}
```

## 自改进循环

复盘报告中的 `recommendations` 不会自动修改 risk-manager 或 signal-generator 的 Skill 参数。
需要人工确认后，才手动更新对应 Skill 的 config 值。

这是 Hermes "自改进但不自修改风控" 原则的体现。

## 约束

- 不在交易记录不足 5 笔时做统计分析（样本太少无意义）
- 复盘报告只输出事实和建议，不做"预测下周行情"
- 所有分析基于已有日志数据，不虚构交易记录
