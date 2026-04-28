---
name: "ship"
description: "发布与部署流程。Git 提交规范、CI/CD 门禁、Feature Flag 生命周期、灰度发布、回滚准备、上线监控。代码写完到上线运行的完整收尾。"
---

# Ship - 发布部署

## 职责
**"代码写完 ≠ 交付"。Ship 是从 feat 完成 + review 通过 → 生产环境稳定运行的完整收尾流程。**

## 触发方式

### 方式 A: 流程触发
- `review` verdict == `approved` 或 `conditional_approved`(已修复)
- 用户要求"发布"/"deploy"/"上线"/"ship it"

### 方式 B: 显式调用
- 准备发版/打 tag
- 紧急 hotfix 发布
- Feature flag 翻转

## 发布流程

```
review approved
     │
     ▼
┌─────────────────────┐
│ Step 1: Git 规范检查   │
│ (commit style +      │
│  branch cleanliness) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Step 2: 安全最终检查  │
│ (security gate)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Step 3: 发布准备      │
│ (changelog +        │
│  version + tag)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Step 4: 部署策略      │
│ (canary/rolling/    │
│  blue-green)        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Step 5: 发布后验证    │
│ (smoke test +       │
│  monitoring)        │
└──────────┬──────────┘
           │
           ▼
        🚢 Live
```

### Hotfix 紧急通道

**适用条件（全部满足才可走紧急通道）**:

| 条件 | 判断 |
|------|------|
| 严重度 | P0 级生产事故（服务不可用/数据丢失/安全漏洞被利用） |
| 影响面 | 影响核心业务流程，无法等待正常发布周期 |
| 修复范围 | ≤ 3 个文件，≤ 100 行改动 |
| 无数据迁移 | 不涉及数据库 schema 变更 |

**紧急通道流程**:

```
P0 生产事故
     │
     ▼
┌─────────────────────┐
│ Step H1: 快速修复      │
│ (hotfix/{id} 分支)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Step H2: 安全必检      │
│ (security Layer 1+2) │  ← 不可跳过
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Step H3: 快速部署      │
│ (Big Bang 策略)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Step H4: 冒烟验证      │
│ (核心流程 + 监控)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Step H5: 事后补审      │  ← 24h 内必须完成
│ (review + changelog) │
└─────────────────────┘
```

**紧急通道 vs 正常通道差异**:

| 步骤 | 正常通道 | 紧急通道 |
|------|---------|---------|
| review | 发布前必须 | **24h 内事后补审** |
| security | 三层全检 | **Layer 1+2 必检，Layer 3 事后补** |
| changelog | 发布前更新 | **发布后 24h 内补** |
| 部署策略 | canary/rolling | **Big Bang（直接全量）** |
| commit 规范 | 严格检查 | **允许简化，事后整理** |

**事后补审清单（24h 内必须完成）**:

- [ ] 补充完整 review（五轴审查）
- [ ] 补充 security Layer 3 检查
- [ ] 更新 changelog
- [ ] 整理 commit message（如需要，squash 后重写）
- [ ] 创建 postmortem 文档（记录根因和预防措施）
- [ ] 触发 kb: 记录 lesson（P0 事故必须有教训沉淀）

**禁止事项**:
- ❌ 非 P0 事故走紧急通道
- ❌ 紧急通道跳过 security Layer 1+2
- ❌ 超过 24h 未补审
- ❌ 修复范围超过 3 文件/100 行仍走紧急通道（应走正常流程）

### Step 1: Git 规范检查

#### Commit 规范

每个 commit 必须遵循 Conventional Commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

| type | 用途 |
|------|------|
| `feat` | 新功能 |
| `fix` | bug 修复 |
| `docs` | 文档变更 |
| `style` | 格式调整（不影响代码逻辑）|
| `refactor` | 重构（非新功能也非修复）|
| `perf` | 性能优化 |
| `test` | 测试相关 |
| `chore` | 构建/工具/依赖变更 |
| `security` | 安全相关变更 |

**Commit 质量**:

| 检查项 | 标准 |
|--------|------|
| 大小 | **~100 行/commit**。超出则拆分 |
| 原子性 | 一个 commit 只做一件事 |
| 可回滚 | 单个 commit revert 后不应破坏构建 |
| message | subject ≤ 50 字符，body 解释 why not what |

**Branch 规范**:

| 类型 | 格式 | 示例 |
|------|------|------|
| 功能 | `feat/{slug}` | `feat/auth-login` |
| 修复 | `fix/{issue-id}-{slug}` | `fix/102-timeout` |
| 发布 | `release/v{version}` | `release/v1.2.0` |
| 热修复 | `hotfix/{issue-id}` | `hotfix/105-auth-bypass` |

#### 执行脚本
```
git log --oneline HEAD~N..HEAD   # 查看 commit 列表
# 检查: commit message 格式、大小、原子性
```

### Step 2: 安全最终门禁

调用 security 技能做最终检查:
- 运行 `security` 三层边界系统的 Layer 2 + Layer 3 检查
- 确认无新的 critical/high 漏洞
- **verdict != fail** 才可继续

### Step 3: 发布准备

#### Changelog 格式

```markdown
## [Unreleased]

### Added
- {新功能描述} (#{issue or pr})

### Changed
- {变更描述}

### Fixed
- {bug 修复描述}

### Security
- {安全修复描述}
```

#### Version 管理

| 变更类型 | 版本递增 |
|---------|---------|
| Bug 修复 | PATCH (x.x.**X**) |
| 新功能（向后兼容）| MINOR (x.**X**.x) |
| 破坏性变更 | MAJOR (**X**.x.x) |

#### Tag 规范
```
git tag -a v{version} -m "v{version}: {一句话总结}"
git push origin v{version}
```

### Step 4: 部署策略

根据风险等级选择:

| 策略 | 适用场景 | 回滚难度 | 说明 |
|------|---------|---------|------|
| **Canary（金丝雀）** | 高风险大功能 | 低 | 先放 5% 流量，观察指标 |
| **Rolling（滚动）** | 无状态服务 | 低 | 逐实例替换 |
| **Blue-Green（蓝绿）** | 有状态/数据库迁移 | 中 | 两套环境瞬时切换 |
| **Big Bang（全量）** | 低风险小修复 | 高 | 直接部署全部（仅 hotfix）|

**Feature Flag 生命周期**:

```
off → internal_test → percentage_rollout → full_on → cleanup
 │         │                  │              │          │
 │    仅内部可访问         渐进放量       全量开放    移除代码
```

### Step 5: 发布后验证

#### Smoke Test（冒烟测试）

| # | 检查项 | 方法 |
|---|--------|------|
| 1 | 服务可访问 | curl / health endpoint 返回 200 |
| 2 | 核心流程走通 | 手动或自动化执行主路径 |
| 3 | 无新增 error | 检查日志/监控 dashboard |
| 4 | 性能基线正常 | p95 响应时间不超过阈值 |
| 5 | 安全头完整 | 检查 CSP / HSTS / X-Content-Type |

#### 监控确认

发布后 **30min 内** 确认:
- [ ] Error rate ≤ 基线 × 1.5
- [ ] P95 latency ≤ 基线 × 1.2
- [ ] 无新的 alert 触发
- [ ] Core Web Vitals 在绿色区间

#### 回滚预案

**每次发布前必须有回滚预案**:

```yaml
# rollback-plan.yaml (附加到 feature 目录)
rollback:
  method: git-revert | db-migration-down | feature-flag-off | container-rollback
  estimated_time: "<分钟>"
  data_impact: none | partial | full
  notification_required: true
  decision_maker: "{who authorizes rollback}"
```

## CI/CD 集成（Shift Left）

```
                    Shift Left 原则
                    ══════════════
                    
  本地              PR              Merge           Deploy
  ─────            ───             ─────           ──────
  lint ✓           lint ✓          build ✓        smoke ✓
  type-check ✓     type-check ✓    test-all ✓      monitor ✓
  unit-test ✓      unit-test ✓     security-scan ✓  alert ✓
                   integration ✓   changelog ✓
                   review-report ✓
```

**质量门禁**: 任何一步失败 → **阻止继续**

## Anti-Rationalization

| "借口" | 反驳 |
|--------|------|
| "先上线再修复" | 上线的 bug 比开发中的 bug 修复成本高 10-100 倍 |
| "没有 CI/CD 就手动部署" | 手动部署是可重复性的敌人，也是错误的温床 |
| "changelog 太麻烦了" | 没有 changelog = 不知道什么变了 = 不敢升级 |
| "不需要回滚预案" | 如果你确信不需要回滚，那正是你最需要回滚预案的时候 |
| "这是小 hotfix，走简化流程" | Hotfix 跳过的每一步检查都是未来生产事故的种子 |

## Red Flags

- ⚠️ commit message 是 "fix"、"update"、"wip" → 必须重写
- ⚠️ 直接 push 到 main/master → 必须走 PR/MR
- ⚠️ 发布时没有 version/tag/changelog → 必须补齐
- ⚠️ 没有回滚预案 → 必须制定后再发布
- ⚠️ 发布后没有监控确认 → 等于盲飞
- ⚠️ database migration 没有 down migration → 无法回滚

## 与其他技能的关系

| 上游 | 动作 | 下游 | 触发条件 |
|------|------|------|---------|
| review approved | 开始 ship 流程 | — | 发布完成 |
| review conditional_approved | 确认 should 项已修复 | — | 修复后开始 ship |
| security | 最终门禁 | — | Step 2，fail 则阻止发布 |
| feat | 生成 changelog 条目 | — | 从 feat 的 checklist 提取变更摘要 |
| kb | 写入 raw/lessons | — | 发布后发现问题时触发 |
