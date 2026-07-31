---
name: stock-monitor
description: A股全流程工具——自动持仓监控+盈亏预警+策略审视+智能选股+持仓诊断+K线/板块。东方财富→腾讯→AkShare→新浪四级fallback。触发词：查股票、股票监控、自选股、持仓、选股、诊断持仓、止盈止损、K线、A股、板块。
---

# 股票监控 Stock Monitor

A 股自选股 + 持仓盈亏自动化监控 + 智能选股。零硬依赖启动。

---


## 🤖 Agent 行为准则

**本 skill 被触发时，Agent 必须遵守以下交互规则：**

| 场景 | 行为 |
|------|------|
| 📊 监控报告 | **直接给操作建议**，不反问用户。每只标的输出具体价位和动作 |
| 🔍 选股推荐 | 展示候选后可问用户感兴趣哪几只（选股需要用户偏好） |
| 💰 买入计算 | 用户选定标的后直接算，不问要不要算 |
| ⚠ 止盈止损 | 给出明确的触发后操作（上移/离场/持有），附具体价格 |

**原则**：用户来拿结论，不是来做选择题。能算出来的就直接给，不要"你觉得呢"。

---

## ⚡ 自动化行为

**当本 skill 被触发时，Agent 必须按顺序执行：**

### 第一步：拉取监控报告

```bash
python3 scripts/monitor.py full
```

自动加载持仓、实时行情、盈亏预警、策略审视。输出 Markdown 格式。

### 第二步：选股（如用户要求或现金闲置）

```
用户: "帮我选几只股"
Agent: python3 scripts/screener.py --top 5
```

筛选器展示候选标的（含 PE / 量比 / 1 手成本 / 入场止损止盈）。

### 第三步：用户挑选

```
Agent: "这几只里有你感兴趣的吗？"
用户: "华能国际和中国中免不错"
```

### 第四步：计算买入建议

```bash
python3 scripts/screener.py --allocate 600011,601888
```

自动读取现金余额，均分预算，给出每只的具体手数、股数、金额、占比。

```
💰 买入建议  |  预算 ¥20,000  均分 2 只
华能国际  11手(1100股)  ¥9,757  49%
中国中免  1手(100股)    ¥5,958  30%
投入 ¥15,715 (79%)  保留 ¥4,285 (21%)
```

### 第五步：用户交易后同步

```
用户: "华能国际 8.87 买了 1000 股"
Agent: python3 scripts/portfolio.py add 600011 --cost 8.87 --qty 1000
```

自动扣除现金、更新持仓。

---

## 💰 现金管理

```bash
python3 scripts/portfolio.py cash-set 50000    # 设置初始现金
python3 scripts/portfolio.py cash              # 查看余额

# 买入 → 自动扣现金
python3 scripts/portfolio.py add 600519 --cost 1680 --qty 100

# 卖出/删除 → 按现价退还现金
python3 scripts/portfolio.py remove 600519
```

---

## 功能概览

| 模块 | 能力 |
|------|------|
| 📊 自动监控 | 触发即加载持仓→行情→盈亏→预警→策略审视 |
| 💰 现金管理 | 设置/查看余额，买入卖出自动更新 |
| ⭐ 自选股 | 增删查改，名称自动识别 |
| 💼 持仓管理 | 成本/数量/止盈/止损，自动计算盈亏 |
| 🧠 策略审视 | K线趋势 + 止损/止盈合理性 + 动态调整建议 |
| 🔍 智能选股 | 多维筛选 → 用户挑选 → 精确计算买入手数 |
| ⚠ 止盈止损 | 三级预警：已触发/接近(2%)/安全 |
| 📈 K 线 | 日/周/月 K 线 + MA5/10/20 |
| 🔥 板块热度 | 行业板块 TOP20（腾讯申万行业），概念板块（东方财富/akshare） |
| 🩺 持仓诊断 | 4维分析 + AkShare 基本面增强 |

---

## 必备依赖

| 技能 | 用途 | 安装方式 |
|------|------|----------|
| `akshare-stock` | 实时行情（备用）、基本面 | `skillhub install akshare-stock` |

---

## 命令参考

```bash
# 监控
python3 scripts/monitor.py                    # 完整报告
python3 scripts/monitor.py --no-review        # 简洁版

# 选股
python3 scripts/screener.py --top 5           # 展示候选
python3 scripts/screener.py --direction 电力   # 指定方向
python3 scripts/screener.py --budget 20000    # 按预算过滤
python3 scripts/screener.py --allocate 600011,601888  # 计算买入建议

# 持仓
python3 scripts/portfolio.py add <code> --cost X --qty N --stop-loss X --take-profit X
python3 scripts/portfolio.py remove <code>
python3 scripts/portfolio.py cash-set <amount>

# 其他
python3 scripts/watchlist.py add <code>
python3 scripts/kline.py 600519 --period weekly
python3 scripts/sectors.py industry
```

---

## 脚本清单

| 脚本 | 功能 |
|------|------|
| `install.sh` | 一键初始化 |
| `data_source.py` | 四级数据源 (东方财富→腾讯→akshare→新浪) |
| `watchlist.py` | 自选股管理 |
| `portfolio.py` | 持仓 + 现金管理 |
| `monitor.py` | 核心监控 — Markdown 报告 + 现金提醒 |
| `screener.py` | 智能选股 — 筛选 + 买入计算 |
| `analysis.py` | 选股模板 + 持仓诊断 |
| `kline.py` | K 线查询 |
| `sectors.py` | 板块热度 |

---

## 数据存储

`~/.stock-monitor/`：

| 文件 | 内容 |
|------|------|
| `watchlist.json` | 自选股列表 |
| `positions.json` | 持仓明细 + 现金余额 |

---

## 免责声明

本工具仅供学习参考，**不构成投资建议**。投资有风险，入市须谨慎。
