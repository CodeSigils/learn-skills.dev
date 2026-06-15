---
name: money-retro
description: 复盘某个正在执行的搞钱机会：记录实际投入时间/实际收入 vs 当初预期，沉淀经验（哪类机会对我有效、哪些坑亲历过），更新状态文件。触发词："复盘"/"这个搞得怎么样"/"实际赚了多少"/"money retro"/"总结一下"。
argument-hint: "<机会名称>"
allowed-tools: Bash(*), Read, Write, Edit, Glob, Skill
---

# /money-retro — 复盘与经验沉淀

不复盘的尝试等于碰运气。这一步把"实际发生的"和"当初预期的"对齐，让推荐越来越准。

## 跨平台说明

`allowed-tools` 是 Claude Code 权限声明；Codex 可忽略，并使用当前会话可用的本地文件工具完成同等动作。

## 流程

### Step 1 — 取出原始预期
读 `.money-state.json`，找该机会的 plan 与 income_expectation（当初 money-plan/money-verify 写下的）。

### Step 2 — 问实际情况
- 实际投入了多少时间？
- 实际收到了多少钱？（第一笔是否到账？走的什么渠道？）
- 过程中有没有出现反诈红线（被要求付费/换私下交易/拖延结款）？
- 体感：愿不愿意继续？卡在哪？

### Step 3 — 对齐预期 vs 实际（校准环的核心）
取出当初 money-plan 写的 `active.prediction`，和实际逐项对账：预计投入/实际投入、预计多久见钱/实际、预计收入/实际。
给一句诚实判断：**继续 / 调整打法 / 止损放弃**。差距大的，想清楚是机会问题还是执行问题。
若触发了任何止损线或反诈红线 → 明确建议止损，并把这条经验记成"亲历坑"。

### Step 4 — 落盘 + 回流 lessons.md（闭合校准环）
- 在 `.money-state.json` 的 `retro_log[]` 追加一条：{date, opportunity_id, predicted, actual, verdict_update, lesson}。
- 更新该机会 status（running / done / dropped）。
- **把可复用经验写进/追加到当前工作目录的 `lessons.md`**（没有就创建）：一条一行，分两类——
  - `对我有效:` （例："小红书图文垂类 X 第 3 周开始有私信咨询"）
  - `亲历坑:` （例："标注类时薪确实低、不值得继续"／"某平台拖延结款"）
  - 这份 `lessons.md` 会被 money-find / money-verify 在 Step 0 读取，**让这套方法对这个用户越用越准**——这是校准环闭合的关键，不要省。

## 收尾
- 继续 → 给下一阶段的小目标。
- 止损 → 提示用 `money-find` 换方向，并把这次教训带入下次筛选。
