---
name: "issue"
description: "Bug 诊断与修复。当遇到程序错误、异常行为或需要调试问题时调用此技能。包含 report(报告)、analyze(分析)、fix(修复)三个子流程。"
---

# Issue - 问题修复

## 职责
问题报告 → 根因分析 → 修复实施 → 回归验证

## 触发条件
- 用户报告 bug / 报错 / 异常行为
- dev 路由判定为"问题类"意图
- 测试/验收中发现缺陷

## issue vs feat 边界判定（必须先执行）

在开始 issue 流程前，用以下决策树判断：

```
用户描述的问题
    ↓
修改范围多大?
    ├─ < 50 行, 单一文件, 恢复预期行为
    │   → ✅ 走 issue-fix
    │
    ├─ 50-200 行, 2-3 文件
    │   → 判断意图:
    │     ├─ 纯恢复原有功能 → issue-fix (标记 severity=major)
    │     └─ 带有新能力增强 → 转为 feat (关联原 ISS)
    │
    └─ > 200 行, 多文件, 或涉及架构变更
        → ⚠️ 必须走 feat 流程 (可从 issue 衍生)

额外维度:
    ├─ 是否需要新测试? → 是 → 走 feat-accept
    ├─ 是否影响公共 API? → 是 → 需 req 更新
    └─ 是否需要架构变更? → 是 → 需 arch review
```

**边界判定补充规则**:

| 场景 | 判定 | 理由 |
|------|------|------|
| 修复 bug 时发现需要重构 | issue → feat | 重构超出修复范围 |
| 修复 bug 时顺便优化性能 | issue (如果 ≤50行) 或 feat | 看改动量 |
| 修复 bug 时发现设计缺陷 | issue-fix 先止血 + 新建 feat | 分离紧急修复和长期改进 |
| 安全漏洞修复 | issue (P0 走 hotfix) | 安全修复优先级最高 |
| 文档/配置错误 | issue (轻量) | 无需 feat 流程 |
| UI 文案/样式微调 | issue (如果 ≤20行) | 不涉及逻辑变更 |
| 数据修复脚本 | issue (一次性) + feat (如果需持久化工具) | 区分临时和长期方案 |

**issue → feat 转换流程**:
1. issue-fix 先完成紧急止血（最小修复使系统恢复可用）
2. 在 issue-report 中记录"衍生 feat"标记：`derived_feat: {feat-id}`
3. 创建新 feat，在 design.md frontmatter 中记录 `origin_issue: {issue-id}`
4. feat 完成后，回填 issue-report 的 `derived_feat` 状态

**歧义时** → 使用 AskUserQuestion 确认: "这主要是修复已有问题，还是趁机改进/新增能力？"

## 工作流程

### issue-report 问题报告

**输出**: `wiki/issues/{slug}-report.md`

frontmatter 格式：
```yaml
---
id: "login-timeout"
type: issue
status: reported                  # reported | analyzing | fixing | fixed | closed | wontfix
title: "登录超时问题"
depends_on: []                    # 通常为空，除非与某需求或特性关联
severity: major                   # critical | major | minor | trivial
created: "2026-04-26T09:00"
updated: "2026-04-26T09:00"
stale: false
---
```

**正文必须包含**:
1. 问题描述（现象）
2. 复现步骤（Step by step）
3. 期望行为 vs 实际行为
4. 环境信息（浏览器/OS/版本）
5. 严重度: critical / major / minor / trivial

文档结构见 `references/issue-report.md`

### issue-kb-retrieve 历史经验检索（analyze 前）

在开始根因分析前，先检查**正式目录**中是否有类似问题的解决记录：

```
Grep pattern: "{错误类型关键词} + {涉及模块/组件}"
target: wiki/knowledge/lessons/*.md, wiki/knowledge/patterns/*.md   ← 只读正式目录，不含 raw/
```

**检索策略**:
- 用错误信息中的**核心名词**（如 timeout / null / memory / auth）作为关键词
- 同时搜索 `wiki/knowledge/patterns/*.md`（可能已有防御模式）
- 如果找到相关 lesson → 将"错误做法→正确做法"注入 analyze 上下文
- **目的**: 避免重复踩坑，加速根因定位

### issue-analyze 根因分析

**输出**: `wiki/issues/ISS-{NNN}-analysis.md` (可选，非显然时才创建)

**分析方法**:

| 方法 | 适用场景 |
|------|---------|
| 5 Whys | 找根本原因 |
| 错误分类 | TS类型错误 / 运行时错误 / 逻辑错误 / 样式 / 性能 / 内存泄漏 |
| 二分排查 | 缩小问题范围 |
| 日志/断点 | 定位具体代码位置 |

**分析完成后**: 确定修复方案（快速修复 vs 彻底修复），评估影响范围

### issue-fix 修复实施

**输出**: 修复代码 + 更新 report.md 的 status 为 `fixed`

**修复规则**:
- 注释说明修复原因 (Fix {slug}: ...)
- 添加防御性编程处理边界情况
- 同时添加/更新回归测试

**修复完成后必须执行**:

#### 回归检查清单

| 类别 | 检查项 | 跳过条件 |
|------|--------|---------|
| 功能验证 | 原问题已解决、相关功能未受影响 | 无 |
| 运行检查 | 有测试则跑 `npm test` (或项目等价命令) | 项目无测试配置 |
| 类型检查 | 无 TS 编译错误 | 非 TS 项目 |
| Lint | ESLint/Prettier 通过 | 未配置 |
| 影响范围 | 确认没有引入新问题 | 无 |

**如果改动范围大** (影响多文件/公共API):
→ 可选触发 `feat-accept` 流程做完整验收

## 状态流转

```
reported → analyzing → fixing → fixed → closed
                        ↘ wontfix   ↘ reopened
```

| 状态转换 | 条件 |
|---------|------|
| reported → analyzing | 信息足够开始排查 |
| analyzing → fixing | 根因已定位，方案已确定 |
| fixing → fixed | 代码已提交，回归检查通过 |
| fixed → closed | 确认无复发，触发 kb (规则见 `dev/SKILL.md` KB触发表) |
| any → reopened | 问题复现或修复不完整 |

## 与其他技能的协作

| 场景 | 动作 | 目标技能 |
|------|------|---------|
| 修复范围超出边界 | → 转为 `feat` | 在 depends_on 中关联 ISS-ID |
| 修复涉及需求变更 | → 更新 `req` | 同步 REQ 文档的 frontmatter |
| 修复涉及架构调整 | → 调用 `arch` | 记录 ADR |
| 修复后有普遍性教训 | → **触发 `kb`** (必须, 见 `dev/SKILL.md` KB触发表) | 写 lesson |
| 修复后需完整验收 | → **可选触发 `feat-accept`** | 跑完整流程 |

## 输出规范

| 项目 | 格式 |
|------|------|
| 报告文档 | `wiki/issues/{slug}-report.md` (含 frontmatter) |
| 分析文档 | `wiki/issues/{slug}-analysis.md` (可选) |
| ID 命名 | kebab-case 语义化名, 如 login-timeout / null-pointer-crash / memory-leak |
