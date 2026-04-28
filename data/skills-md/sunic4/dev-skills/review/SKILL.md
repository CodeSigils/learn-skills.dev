---
name: "review"
description: "代码审查与质量评估。五轴评审：正确性/安全性/性能/可维护性/测试覆盖。feat-accept 后的独立审查环节，或用户显式触发。支持 full（完整报告）和 lite（内联简评）两种模式。"
---

# Review - 代码审查

## 职责
**独立第三方视角的代码质量评估** — 不是自验收(feat-accept)，而是 peer review。

## 触发方式

### 方式 A: 流程触发
- **full 模式** feat-accept 验收通过后 → 自动进入 review（必须）
- **lite 模式** feat-accept 验收通过后 → **可选**进入 review（ff 通道可跳过）
- `ship` 发布前 → 必须经过 review

### 方式 B: 显式调用
- 用户要求"review 一下"/"审查这段代码"/"code review"
- PR/MR 准备提交前

### 模式选择规则

| 条件 | 模式 | 说明 |
|------|------|------|
| 变更 ≤100 行, ≤3 文件 | **lite** (可选) | 内联简评，可合并到 design.md |
| 变更 >100 行 或 >3 文件 | **full** (必须) | 完整五轴审查 + 独立报告 |
| 涉及安全/支付/认证 | **full** (必须) | 无论大小，安全相关必须完整审查 |
| 用户显式要求 | 以用户选择为准 | — |

## 与 feat-accept 的区别

| | feat-accept (自验收) | review (代码审查) |
|---|---|---|
| **视角** | 开发者自己 | 第三方 (code-reviewer persona) |
| **标准** | "功能是否按需求实现" | "Staff 工程师会 approve 吗？" |
| **输出 (full)** | acceptance.md | **review-report.yaml** |
| **输出 (lite)** | 合并到 design.md 末尾 | 内联到 design.md `## Code Review` 章节 |
| **可否跳过** | 小改动(lite)可跳过 | **lite 可跳过**, full 不可跳过 |

## 审查流程

```
feat-accept 通过
     │
     ▼
┌─────────────────────┐
│ Step 1: 变更范围评估   │
│ (变更大小 + 复杂度)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Step 2: 五轴逐项审查   │
│ (correctness/security │
│  performance/maint/   │
│  test_coverage)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Step 3: 生成报告      │
│ (review-report.yaml) │
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     ↓           ↓
  approved    需修复
     │           │
     ↓           ↓
  可进入 ship  返回 feat 修复后 re-review
```

### Step 1: 变更范围评估

```bash
# 用脚本读取 checklist 摘要（~10 行输出），避免全量加载
node skills/init/references/tools/read-yaml.mjs wiki/features/{slug}/impl-checklist.yaml --summary
# 或精确查询:
node skills/init/references/tools/read-yaml.mjs wiki/features/{slug}/impl-checklist.yaml \
    --query "files[*].path,files[*].status,steps[*].status"
```

基于脚本输出，计算：

| 指标 | 计算 | 阈值 |
|------|------|------|
| **变更文件数** | impl-checklist.files.length | > 10 个文件 → 标记 large |
| **代码行数** | git diff --stat 的 +/- 总和 | > 500 行 → 标记 large |
| **模块跨度** | files 跨越的一级目录数 | > 3 个模块 → 需要拆分建议 |
| **复杂度** | 涉及的新增依赖/外部 API 数量 | 高复杂度 → 加强安全+性能审查 |

**变更大小判定**:
- **small**: ≤100 行，≤3 文件 → 快速审查模式
- **medium**: 101-500 行，4-8 文件 → 标准五轴审查
- **large**: >500 行 或 >8 文件 → **必须拆分**，先 review 第一部分

> ⚠️ Red Flag: 单次变更超过 400 行 → 建议拆分为多个小 PR

### Step 2: 五轴审查

每轴独立评分 (1-5) + 记录 findings:

#### Axis 1: Correctness（正确性）

| 关注点 | 检查项 |
|--------|--------|
| 逻辑正确 | 边界条件、空值处理、类型安全、竞态条件 |
| 错误处理 | 异常是否被捕获、错误信息是否有用、fallback 是否存在 |
| 数据一致性 | 状态更新是否原子、副作用是否可控 |
| API 契约 | 是否符合 arch 定义的接口规范 |

#### Axis 2: Security（安全性）

*(详细检查见 `security` 技能的嵌入式检查清单)*

| 关注点 | 检查项 |
|--------|--------|
| 输入验证 | 用户输入是否校验和清洗 |
| 认证授权 | 是否有越权访问风险 |
| 敏感数据 | 密码/token/密钥是否明文暴露 |
| 依赖安全 | 新引入的依赖是否有已知漏洞 |

#### Axis 3: Performance（性能）

| 关注点 | 检查项 |
|--------|--------|
| O(n) 问题 | 是否有明显的 N+1 查询 / O(n²) 循环 |
| 内存 | 大对象是否及时释放、是否有内存泄漏风险 |
| 网络 | 是否有不必要的请求、缓存策略是否合理 |
| 渲染 | 前端是否有不必要的重渲染 |

#### Axis 4: Maintainability（可维护性）

| 关注点 | 检查项 |
|--------|--------|
| 命名 | 变量/函数/文件名是否语义清晰 |
| 长度 | 单函数 >50 行？单文件 >300 行？单组件 >200 行？ |
| 复杂度 | 嵌套层级 >4？圈复杂度 >10？ |
| DRY | 是否有重复逻辑可提取？(DAMP > DRY — 可读性优先) |
| 注释 | 为什么(why) 有注释，怎么做(how) 靠代码表达 |

#### Axis 5: Test Coverage（测试覆盖）

| 关注点 | 检查项 |
|--------|--------|
| 覆盖率 | 核心路径是否有测试？边界值是否覆盖？ |
| 测试质量 | 测试是否验证行为而非实现？是否有有意义的 assertion？ |
| Edge case | 空/null/异常输入是否测试？并发/超时等场景？ |
| 测试命名 | 是否描述了被测行为而非实现细节？ |

### Step 3: 生成报告（按模式区分）

#### Full 模式 — 独立 review-report.yaml

运行脚本生成结构化报告：
```
node wiki/tools/review-generate.mjs --feature {slug}
```
输出: `wiki/features/{slug}/review-report.yaml`

#### Lite 模式 — 内联到 design.md

在 `{slug}-design.md` 末尾追加 `## Code Review` 章节：

```markdown
## Code Review

**审查时间**: YYYY-MM-DD HH:MM
**模式**: lite
**审查者**: code-reviewer (AI)
**结论**: ✅ approved | ⚠️ conditional_approved | ❌ request_changes

### 各轴评分 (1-5)

| 轴 | 评分 | 关键发现 |
|----|------|---------|
| Correctness | 4/5 | — |
| Security | 5/5 | — |
| Performance | 4/5 | — |
| Maintainability | 4/5 | — |
| Test Coverage | N/A | lite 模式不强制 |

### Findings
- [should] 建议拆分 `handleAuth` 函数，当前圈复杂度偏高
- [fyi] 可考虑使用 `const` 替代部分 `let`

### 结论说明
{简要说明}
```

**两种模式共用 Verdict 判定规则**:

| 条件 | verdict | 含义 |
|------|---------|------|
| 所有轴 ≥4 且无 must 级 finding | **approved** | 可直接进入 ship |
| 有 should 级 finding 但无 must | **conditional_approved** | 修复 should 后可 ship（可并行） |
| 有 must 级 finding | **request_changes** | 必须修复后 re-review |
| correctness < 2 或 security 有 must | **rejected** | 重大问题，打回重做 |

## Finding 严重性标签

| 标签 | 含义 | 阻止合并？ |
|------|------|-----------|
| **must** | 必须修复，否则有 bug/安全风险 | ✅ 是 |
| **should** | 应该修复，但有合理理由可 waive | ⚠️ 条件性 |
| **fyi** | 知道就好，不强制修复 | ❌ 否 |
| **optional** | 改进建议，nice to have | ❌ 否 |
| **nit** | 风格/格式偏好 | ❌ 否 |

## Anti-Rationalization（反合理化）

| "借口" | 反驳 |
|--------|------|
| "这只是内部工具，不需要这么严格" | 内部工具的安全漏洞往往是攻击入口 |
| "后面再重构/优化" | 临时代码是最持久的代码。如果值得写就值得写好 |
| "测试覆盖率已经够了" | 覆盖率数字 ≠ 测试质量。检查的是关键路径是否被验证 |
| "这个改动能跑就行" | "能跑" 和 "能维护" 是两件事 |
| "时间紧，先 merge 再说" | 合并后的技术债利息比预想的高得多 |

## Red Flags

- ⚠️ 审查者只说了 "LGTM" / "looks good" → 要求具体反馈（每轴至少一条）
- ⚠️ 变更包含 `TODO` / `HACK` / `FIXME` 且无对应 issue → 必须创建 issue 追踪
- ⚠️ 新增了 dependency 但 package.json 无版本锁定 → 必须 lock
- ⚠️ 删除了测试用例且无解释 → 必须说明原因
- ⚠️ console.log / debugger 残留在代码中 → 必须清除

## 与其他技能的关系

| 上游 | 动作 | 下游 | 触发条件 |
|------|------|------|---------|
| feat-accept 通过 | 开始 review | ship | verdict == approved |
| feat-accept 通过 | 开始 review | feat (re-fix) | verdict == request_changes/rejected |
| security | 嵌入式调用 | — | Step 2 Axis 2 时自动执行 security 检查清单 |
| kb | 写入 raw/lessons | — | 发现通用反模式时触发 |
