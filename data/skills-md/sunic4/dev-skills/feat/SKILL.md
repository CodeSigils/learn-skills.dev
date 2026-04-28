---
name: "feat"
description: "特性设计与实现。当需要将需求转化为代码、进行编码实现时调用此技能。包含 design(设计)、impl(实现)、accept(验收)三个子流程。"
---

# Feat - 特性开发

## 职责
需求/架构 → 技术设计 → 编码实现 → 验收

## 触发条件
- req/arch 输出后，进入实现阶段
- 用户明确要求"写代码"/"实现功能"/"开发xx"
- dev 路由判定为"实现类"意图

## 前置检查（必须执行）

### 1. 上游依赖检查 — 读 frontmatter

读取上游 REQ 和 ARCH 文档的 frontmatter：
```yaml
# 读 wiki/requirements/REQ-001-xxx.md 的 frontmatter
stale: true   ← 如果是 true，先同步上游再继续

# 读 wiki/architecture/ADR-xxx.md 或 modules/xxx.md 的 frontmatter
stale: false  ← OK，可以继续
```
→ 任何一个上游 `stale: true` 则**暂停并提示用户**

### 2. 冲突检测 — 局部扫描 checklist.yaml

```
Step 1: Grep pattern: "status: implementing"
        target: wiki/features/*/impl-checklist.yaml

Step 2: 对比每个活跃 feat 的 files.path 列表与当前 feat 的 files 列表

Step 3: 有路径重叠 → 警告:
    ⚠️ src/Login.tsx 被 FEAT-002 同时修改
    [A] 等待对方完成  [B] 协调拆分文件  [C] 强制继续(风险自负)
```

### 3. 依赖顺序检查
如果当前 feat design.md 的 `depends_on` 引用了其他未完成的 FEAT：
→ 提示: "FEAT-XXX 尚未完成，本特性依赖其输出。是否等待？"

### 4. Roadmap 上下文读取（Roadmap 关联 Feat 时必须执行）

```
Step 1: 检查上游 REQ 的 depends_on 是否引用了 roadmap
        或 Grep: "roadmaps/*/{slug}-roadmap.md" → 检查 items.yaml 中是否有当前 feat

Step 2: 如果找到关联 roadmap:
        ```bash
        # 仅提取需要的字段（~8 行输出）
        node skills/init/references/tools/read-yaml.mjs wiki/roadmaps/{slug}/items.yaml \
            --query "items[*].title,items[*].status,items[*].priority,items[*].depends_on"
        ```
        → 获取: priority / depends_on(同 roadmap 内) / 整体进度
        → 读取 {slug}-roadmap.md 中的接口契约章节

Step 3: 将以下信息注入 design.md 的上下文:
        - 本 feat 在 roadmap 中的优先级和位置
        - 哪些 feat 等待本 feat 完成
        - 必须遵守的跨模块接口契约（来自 roadmap Step 3）
```

**如果有关联 roadmap 但未执行此步**: design 可能与整体规划冲突，接口可能不兼容。

### 5. 接口契约合规检查（涉及多模块时）

如果 Step 4 发现存在关联 roadmap 且定义了接口契约：

| 检查项 | 动作 |
|--------|------|
| roadmap 定义了本模块的对外接口 | design.md 的"接口与类型定义"必须与之对齐 |
| roadmap 定义了依赖的上游接口 | 确认上游 feat 已实现或将在本 feat 之前实现 |
| 设计中发现需要新接口 | **暂停 → 回退到 roadmap 补充接口定义** |

### 6. KB 经验检索（设计/实现前）

只检索**正式目录**中的知识：

```
Grep pattern: "{当前功能领域关键词}"
target: wiki/knowledge/patterns/*.md, wiki/knowledge/lessons/*.md   ← 不含 raw/
```

如果找到相关 pattern 或 lesson：
→ 将经验注入 design 或实现上下文，避免重复踩坑

### 7. 模式选择（lite vs full）

前置检查全部通过后，根据变更规模自动选择模式：

| 判定维度 | **lite 模式** | **full 模式** |
|---------|--------------|--------------|
| 改动文件数 | ≤ 3 个文件 | > 3 个文件 |
| 代码行数 | ≤ 100 行（新增+修改） | > 100 行 |
| 复杂度 | 单一功能点，不涉及新模块/架构 | 多模块、新接口、复杂逻辑 |
| 典型场景 | 修 bug、改样式、加字段、小重构 | 新功能开发、架构调整 |

**选择结果影响后续流程**：
- **lite**: 简化 checklist（无 steps/evidence）、acceptance 合并到 design、可选跳过 review
- **full**: 完整增强 checklist、独立 acceptance 文档、必须走 review

> ⚠️ 如果用户显式要求走 full 流程，以用户选择为准。

## 子流程

### feat-design 技术设计

**输入**: REQ 文档 + ARCH 文档  
**输出**: `wiki/features/YYYY-MM-DD-{slug}/{slug}-design.md`

design.md 的 frontmatter：
```yaml
---
id: "login-feature"
type: feature
status: designing                # designing | done
title: "登录功能实现"
depends_on:
  - "../../requirements/user-auth.md"
  - "../../architecture/modules/auth-module.md"
created: "2026-04-25T12:00"
updated: "2026-04-25T14:00"
stale: false
---
```

**正文必须包含**:
1. 实现思路概述
2. 文件变更清单（新建/修改/删除 + 路径）— 此列表写入同目录 `impl-checklist.yaml`
3. 接口/类型定义
4. 测试策略
5. 风险与依赖

**设计完成后同时生成** `impl-checklist.yaml`（根据模式选择格式）：

#### Full 模式 checklist（增强格式）

适用于 >3 文件或 >100 行的改动：

```yaml
meta:
  feature_id: "{slug}"
  mode: full
  status: implementing            # designing | implementing | reviewing | done | abandoned
  created: "YYYY-MM-DDTHH:MM"     # 🤖 自动
  updated: "YYYY-MM-DDTHH:MM"     # 🤖 自动
  current_step: N                 # 当前进行到第几步

steps:
  - id: 1
    name: "步骤名称"
    status: pending               # pending | in_progress | done | blocked
    evidence: "完成证据/描述"      # done 时填写

files:
  - path: "src/services/auth.ts"
    status: pending               # pending | in_progress | done
    changes: "+120 -15"           # 完成后填入 diff 统计

security_check:
  status: pending                 # pending | passed | failed | waived

conflicts_with: []
```

#### Lite 模式 checklist（简化格式）

适用于 ≤3 文件且 ≤100 行的改动：

```yaml
meta:
  feature_id: "{slug}"
  mode: lite
  status: implementing            # designing | implementing | done
  created: "YYYY-MM-DDTHH:MM"     # 🤖 自动
  updated: "YYYY-MM-DDTHH:MM"     # 🤖 自动

files:
  - path: "src/utils/format.ts"
    status: pending               # pending | in_progress | done
    changes: null                 # 完成后可选填入

security_check:
  status: pending                 # pending | passed | failed | waived
```

**lite vs full 差异总结**：

| 特性 | lite | full |
|------|------|------|
| steps / current_step / evidence | ❌ 不需要 | ✅ 必须有 |
| files.changes | 可选（不强制填） | 必须 |
| conflicts_with | ❌ 不需要 | ✅ 需要 |
| acceptance 输出 | 合并到 design.md 末尾 | 独立 acceptance.md |
| review | 可选跳过（ff 通道） | 必须执行 |

**生成后校验**（两种模式共用）：
```
node wiki/tools/validate-yaml.mjs wiki/features/YYYY-MM-DD-{slug}/impl-checklist.yaml --schema impl_checklist
```

文档结构见 `references/feature-design.md`

### feat-impl 编码实现

**输入**: FEAT design 文档 + impl-checklist.yaml  
**输出**: 实际代码文件 + 更新的 checklist.yaml

**编码规则**:
- 先类型后实现，让编译器辅助检查
- 遵循项目现有约定（从已有代码学习风格）
- 小步提交，每个子功能点可独立验证
- 避免 any，使用明确类型

**每完成一个文件**:
- 更新 `impl-checklist.yaml` 对应条目的 `status: in_progress` → `done`
- **full 模式额外**: 填入 `changes: "+N -M"` (diff 统计)、`meta.current_step` +1
- 更新 `meta.updated` 时间戳（🤖 自动）
- **full 模式**: 运行校验（lite 模式可跳过）:
  ```
  node wiki/tools/validate-yaml.mjs wiki/features/{slug}/impl-checklist.yaml --schema impl_checklist
  ```
- 将 checklist 的顶层 `meta.status` 改为 `implementing`

**实现中异常处理**:

| 异常场景 | 处理方式 |
|---------|---------|
| 发现需求不清 | ↩ **回退到 req**: 补充需求后重新设计 |
| 设计方案不可行 | ↩ **回退到 feat-design**: 修改设计文档再继续 |
| 发现相关 bug | → **分支到 issue**: 创建 ISS，记录关联，继续或暂停 |
| 发现好模式 | → 触发 kb (规则见 `dev/SKILL.md` KB触发表): 记录 pattern（不要中断主流程） |

### feat-accept 验收测试

**输入**: 实现代码 + REQ 验收标准

**输出（按模式区分）**:
- **full 模式**: 独立文件 `wiki/features/YYYY-MM-DD-{slug}/{slug}-acceptance.md`
- **lite 模式**: 作为章节追加到 `{slug}-design.md` 末尾（见下方格式）

#### Full 模式 — 独立 acceptance 文档

输出: `wiki/features/YYYY-MM-DD-{slug}/{slug}-acceptance.md`

frontmatter：
```yaml
---
id: "login-feature-acceptance"
type: feature
status: done                     # 验收通过后设为 done
title: "登录功能验收报告"
depends_on:
  - "./login-design.md"
result: pass                    # pass | fail | conditional
created: "2026-04-26T16:00"     # 🤖 自动
updated: "2026-04-26T17:00"     # 🤖 自动
---
```

#### Lite 模式 — 合并到 design.md 末尾

在 `{slug}-design.md` 文末追加 `## 验收结果` 章节：

```markdown
## 验收结果

**验收时间**: YYYY-MM-DD HH:MM
**模式**: lite
**结果**: ✅ pass | ❌ fail | ⚠️ conditional

### 检查清单

| 类别 | 检查项 | 结果 |
|------|--------|------|
| 功能 | 主流程通、异常处理正确 | ✅/❌ |
| 质量 | 无 TS 错误、Lint 通过 | ✅/❌ |

### 备注
{可选：简要说明}
```

**两种模式共用验收标准**：

| 类别 | 检查项 |
|------|--------|
| 功能 | 所有验收标准满足、主流程通、异常处理正确、边界覆盖 |
| 质量 | 无 TS 错误、Lint 通过、无 console.log 残留、无遗留 TODO |
| 测试 | 单元测试通过、关键路径覆盖率达标 (full 模式必须) |
| 性能 | 无明显性能问题、无内存泄漏 (full 模式必须) |

**验收结果**:
- ✅ 通过 → checklist.yaml `meta.status: done`；更新上游 REQ 的 `status: implemented`
- ❌ 不通过 → ↩ 回退到 feat-impl 或 feat-design

**验收通过后的动作**:
- [ ] 更新 checklist `meta.status: done`
- [ ] **同步 roadmap 状态**（如果当前 feat 属于某个 roadmap）:
  ```
  # 更新 items.yaml 中对应项 status
  # 读取并修改 wiki/roadmaps/{roadmap-slug}/items.yaml
  # 将当前 feature 的 status 从 doing 改为 done
  
  # 如果是 roadmap 最后一项 feat，检查所有 features.status==done
  # 若全部 done，更新 roadmap 主文档 status: done
  ```
- [ ] 触发 kb: 记录有价值的 pattern 或 lesson (强制等级见 `dev/SKILL.md` KB触发表)
- [ ] **进入 review 流程** (**full 模式必须**, **lite 模式可选**):
  ```
  node wiki/tools/review-generate.mjs --feature {slug}
  ```
  → 生成 `review-report.yaml` → 进入 **review** 技能做五轴审查
- [ ] **lite ff 快速通道**: 验收通过后可直接进入 **ship** (跳过 review)

### feat-ff 快速通道（轻量实现）

**用途**: 跳过 design 和 acceptance，直接写代码。适用于**小改动**。

**触发条件（全部满足才可走 ff）**:

| 条件 | 判断 |
|------|------|
| 改动文件数 | ≤ 3 个文件 |
| 改动复杂度 | 单一功能点（不涉及新模块/新架构） |
| 无跨模块接口 | 不需要定义新的 API 契约 |
| 无上游依赖 | 不依赖其他未完成的 feat |
| 风险等级 | 不涉及数据迁移/安全/支付等关键域 |

**ff 流程**:

```
feat-ff: 直接实现
    │
    ▼
┌───────────────┐
│ 1. 创建目录    │ wiki/features/YYYY-MM-DD-{slug}/
└───────┬───────┘
        │
        ▼
┌───────────────┐     ┌───────────────┐
│ 2. 写 checklist│ ←→  │ 3. 直接编码   │ (边写边更新)
│    (极简版)    │     │               │
└───────┬───────┘     └───────┬───────┘
        │                     │
        └──────────┬──────────┘
                   ↓
          ┌───────────────┐
          │ 4. 自测通过?   │
          └───────┬───────┘
                  ↓Yes ✅ 完成
                  ↓No → 走完整流程 (design→impl→accept)
```

**ff 输出**:

只生成两个文件（不需要 design.md 和 acceptance.md）：

```yaml
# impl-checklist.yaml (ff 极简版)
status: done                       # 完成后直接设为 done
mode: ff                           # 标记为快速通道
files:
  - path: "src/utils/format.ts"
    status: done
  - path: "src/components/DateDisplay.tsx"
    status: done
security_check:
  status: pending                  # 涉及安全敏感代码时必须检查
conflicts_with: []
```

```yaml
# {slug}-design.md (ff 极简版 — 只保留 frontmatter + 一句话)
---
id: "{slug}"
type: feature
status: done
mode: ff                           # 标记为快速通道
title: "{标题}"
depends_on: []
created: "2026-04-26T15:00"
updated: "2026-04-26T15:30"
stale: false
---

{一句话描述做了什么}
```

**ff 规则**:
- 编码过程中发现改动比预期大 → **立即切换到完整流程**
- ff 完成后如果用户要求补设计文档 → 可以回补 design.md
- ff 不做正式 acceptance 测试，但必须自测主流程

## 流程状态机

```
                    ┌──────────────┐
                    │    开始      │
                    └──────┬───────┘
                           ↓
              ┌────────────┴────────────┐
              ↓                         ↓
       ┌──────────────┐          ┌──────────────┐
       │  满足 ff 条件?│──Yes──→ │   feat-ff    │
       └──────┬───────┘          │  (快速通道)   │
              ↓No                └──────┬───────┘
              ↓                         ↓ ✅
       ┌──────────────┐
       │  feat-design  │←────────┐
       └──────┬───────┘         │
              ↓                 │
       [设计完成?]               │
        ↓Yes   ↓No(↩回req)      │
              ↓                 │
       ┌──────────────┐         │
       │  feat-impl    │         │
       └──────┬───────┘         │
              ↓                 │
       [实现中发现问题?]          │
        ↓No    ↓Yes             │
        ↓    (↩design/req/issue) │
              ↓                 │
       ┌──────────────┐         │
       └────│  feat-accept  │─────────┘
            └──────┬───────┘
                   ↓
           [验收通过?]
            ↓Yes   ↓No(↩impl)
                   ↓
                ✅ 完成
```

## 与其他技能的协作

| 场景 | 动作 | 目标技能 |
|------|------|---------|
| 设计前需要确认需求 | ↩ 回退补充 | `req` |
| 实现前需要架构决策 | 前置调用 | `arch` |
| 实现中发现 bug | 分支创建 | `issue` |
| 实现中涉及敏感代码 | 嵌入式触发 | **security** (必须) |
| 验收通过后有经验可沉淀 | 触发 kb | `kb` (见 dev/SKILL.md KB触发表) |
| 验收通过后(非ff) | 生成报告 → 启动审查 | **review** → **ship** |
| 验收通过后(ff快速通道) | 跳过 review 直接发布 | **ship** |
| 改动范围大需回归测试 | 可选触发 | `feat-accept`(自身) |

## 输出规范

| 项目 | 格式 | 生成时机 |
|------|------|---------|
| Feature 目录 | `wiki/features/YYYY-MM-DD-{slug}/` | design 开始时 |
| 设计文档 | `{slug}-design.md` (含 frontmatter) | feat-design 完成 |
| 进度追踪 | `impl-checklist.yaml` (增强 schema) | design 时创建，impl 时持续更新 |
| 验收报告 | `{slug}-acceptance.md` (含 frontmatter) | feat-accept 完成 |
| 审查报告 | `{slug}-review-report.yaml` | accept 后由 review-generate.mjs 生成 |
