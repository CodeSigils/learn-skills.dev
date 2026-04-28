---
name: "dev"
description: "AI 编程工作流根入口，路由到正确的子技能(req/arch/roadmap/feat/issue/kb/onboard)。当用户不知道用哪个技能或首次使用时调用此技能。"
---

# Dev - 工作流根入口

## 职责
意图识别与技能路由

## 触发条件
- 用户不知道该调用哪个技能
- 首次使用或项目初始化
- 用户描述模糊，需要澄清后路由

## Wiki 目录结构

```
wiki/
├── raw/                  # 原始输入 (user-inputs / research / references)
├── requirements/         # 需求文档 (slug 命名)
├── architecture/         # 架构设计 (overview / decisions / modules)
├── roadmaps/             # 大需求拆解规划 (一个 roadmap 一个目录)
├── features/             # 特性开发记录 (一个 feature 一个目录)
├── issues/               # 问题修复记录
├── knowledge/            # 知识库 (两阶段: raw → 正式目录)
│   ├── raw/              # 阶段1: 原始写入区 (各技能写到这里，不可被检索)
│   ├── patterns/         # 阶段2: 正式发布区 (可被读取)
│   ├── lessons/
│   ├── decisions/
│   ├── references/
│   └── _archive/         # 归档 (过时但保留)
```

## 统一 Frontmatter 规范（所有输出文档必须遵守）

每个 wiki 输出文档的 YAML frontmatter 必须包含以下字段：

```yaml
---
id: "{slug}"                    # ✋ 手动填写: 唯一标识
type: requirement | architecture | feature | issue | knowledge  # ✋ 手动填写
status:                          # ✋ 手动填写 (见下方状态枚举)
title: ""                        # ✋ 手动填写: 人类可读标题
depends_on: []                   # ✋ 手动填写: 上游文档路径列表 (相对 wiki/ 根目录)
created: "YYYY-MM-DDTHH:MM"     # 🤖 自动生成: 文档首次创建时由工具自动填充
updated: "YYYY-MM-DDTHH:MM"     # 🤖 自动更新: 每次文档修改时自动刷新
stale: false                     # 🤖 自动标记: 上游变更时自动设为 true
---
```

**自动化说明**：
- **🤖 自动字段** (`created` / `updated` / `stale`)：由技能执行时自动填充和更新，**无需手动维护**
- **✋ 手动字段** (`id` / `type` / `status` / `title` / `depends_on`)：创建文档时必须手动填写
- 实际编写时只需关注 5 个手动字段，减少机械性工作

### 各 type 的 status 枚举

| type | 可选 status |
|------|------------|
| **requirement** | draft → reviewing → approved → implemented → deprecated |
| **architecture** | proposed → accepted → implemented → superseded → deprecated |
| **feature** | designing → implementing → done → abandoned |
| **issue** | reported → analyzing → fixing → fixed → closed → wontfix |
| **knowledge** | draft → verified |

### Feature 目录结构（特殊）

feature 不用单文件，用一个目录承载所有相关文档。**根据变更规模自动选择 lite 或 full 模式**（详见 `feat` 技能 § 模式选择）：

```
wiki/features/YYYY-MM-DD-{slug}/
├── {slug}-design.md              # 含 frontmatter (lite: 含验收+review; full: 仅设计)
├── impl-checklist.yaml           # 实现进度追踪 (lite: 简化格式 / full: 增强格式)
├── {slug}-acceptance.md          # 仅 full 模式 (含 frontmatter, 验收结果)
└── {slug}-review-report.yaml     # 仅 full 模式 (代码审查结果, review 技能生成)
```

**lite 模式实际产出**（≤3 文件, ≤100 行）：
```
wiki/features/YYYY-MM-DD-{slug}/
├── {slug}-design.md              # 设计 + 验收结果(末尾追加) + Code Review(可选)
└── impl-checklist.yaml           # 简化版 (无 steps/evidence/conflicts)
```

**full 模式完整产出**（>3 文件或 >100 行）：
```
wiki/features/YYYY-MM-DD-{slug}/
├── {slug}-design.md              # 设计文档
├── impl-checklist.yaml           # 增强版 (含 steps/evidence/conflicts)
├── {slug}-acceptance.md          # 独立验收报告
└── {slug}-review-report.yaml     # 独立审查报告
```

`impl-checklist.yaml` 格式（详见 `feat` 技能 § checklist 格式）：
```yaml
meta:
  feature_id: "{slug}"
  status: implementing            # designing | implementing | reviewing | done | abandoned
  created: "YYYY-MM-DDTHH:MM"
  updated: "YYYY-MM-DDTHH:MM"
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

## 路由规则

### Step 1: 关键词快速匹配（置信度 ≥ 80% 直接路由）

| 意图关键词 | 路由目标 | 典型表达 |
|-----------|---------|---------|
| 初始化/新项目/搭建/骨架 | `init` | "初始化项目"、"生成 wiki 骨架" |
| 新功能/需求/想要/做个xx | `req` | "我要做个登录功能"、"新增一个需求" |
| 大需求/系统/平台/整套 | `roadmap` | "我要一个权限系统"、"做一套支付流程" |
| 架构/设计/方案/选型/技术栈 | `arch` | "系统怎么设计"、"用什么状态管理" |
| 实现/写代码/开发/编码 | `feat` | "实现这个功能"、"帮我写这段代码" |
| 重构/优化代码/整理/改进结构/代码优化 | `feat` (lite/full) | "重构一下这个模块"、"优化代码结构"、"整理代码" |
| bug/报错/报了/出错/不正常 | `issue` | "有个bug"、"控制台报错了" |
| 审查/review/代码评审/PR/MR | `review` | "review 一下"、"代码审查"、"准备提交 PR" |
| 安全/漏洞/加密/认证/权限 | `security` | "安全检查"、"security audit"、"有没有漏洞" |
| 发布/部署/上线/ship/tag | `ship` | "发布到生产"、"deploy一下"、"打个 tag 上线" |
| 记录/经验/知识/沉淀/踩坑 | `kb` | "记一下这个经验"、"沉淀到知识库" |

**roadmap vs req 的区分**:
- `req`: 单一功能点，1-2 个模块，可直接实现
- `roadmap`: 大需求，≥ 3 个模块，需要先拆解规划

### Step 2: 置信度 < 80% → 必须澄清

使用 AskUserQuestion 确认意图，常见歧义场景：

| 模糊输入 | 澄清问题 |
|---------|---------|
| "帮我看看这个代码" | 这是 code review(feat)、debug(issue)、还是学习(kb)？ |
| "这个功能有问题" | 是 bug 修复(issue)、需求不合理(req)、还是需要重构(feat)？ |
| "改进一下体验" | 是新需求(req)、重构优化(feat)、还是架构调整(arch)？ |
| "修一下并增加xx" | 以修复为主(issue) 还是以新功能为主(feat)？ |
| "重构一下" | 小范围重构(feat-lite) 还是涉及架构变更(arch)？ |

### Step 3: 根据回答精确路由

### Step 4: KB 预检索（路由后、进入子技能前）

在分发到目标技能前，先搜索**正式目录**中是否有相关经验（不含 raw/ 和 _archive/）：

```
Grep pattern: "{路由目标关键词}"
target:
  - wiki/knowledge/patterns/*.md
  - wiki/knowledge/lessons/*.md
  - wiki/knowledge/decisions/*.md
  - wiki/knowledge/references/*.md
```

如果找到相关条目：
> 📚 找到 {N} 条相关知识:
> - `wiki/knowledge/patterns/xxx.md` — {标题}
> - `wiki/knowledge/lessons/yyy.md` — {标题}
> 已将上下文传递给后续技能。

**跳过条件**: init 路由时跳过（无相关上下文）

## 主流程

### 项目初始化
```
dev → init(生成 wiki/ 骨架 + AGENTS.md)
```

## KB 嵌入式触发表（权威定义）

**所有子技能的 KB 触发规则以此表为准，子技能不得重复定义或覆盖。**

**原则：默认不记录（opt-in），仅在有明确价值时主动写入。避免 raw/ 膨胀和整理负担。**

| 来源技能 | 触发时机 | 记录类型 | 强制等级 | 说明 |
|---------|---------|---------|---------|------|
| `feat-impl` | 发现可复用模式 (<5min 解决) | pattern | **可选** | 有明显复用价值时才写，不中断主流程 |
| `feat-impl` | 棘手问题解决 (>15min) | lesson | **应做** | 解决后评估价值，有价值则写，无价值跳过并注明原因 |
| `feat-accept` | 验收中发现通用经验 | pattern / lesson | **可选** | 有明确复用场景时才记录 |
| `issue-fix` | bug 有普遍性/典型性 | lesson | **应做** | 同类问题可能再次出现时记录，一次性问题跳过 |
| `arch` | ADR 决策有长期参考价值 | decision | 可选 | ADR 本身已记录时引用即可 |
| `req` | 需求分析中的通用方法论 | pattern | 可选 | |

**强制等级含义**:
- **必须**: 不写则视为流程未完成。修复/解决后立即执行，不得推迟。
- **应做**: 评估后有价值才写，无合理理由跳过时需注明原因。
- **可选**: 仅在有明显、明确的长期价值时写入。默认不写。

**默认行为原则**: 不记一条无用的，也不漏掉一条确实有价值的。质量 > 数量。

## KB 读写矩阵（完整视图）

**核心规则: 各技能写入 `raw/`，只能读取正式目录（patterns/lessons/decisions/references/）。`raw/` 中的内容对其他技能不可见。**

| 技能 | 写入目标 | 读取目标 | 检索时机 |
|------|---------|---------|---------|
| **dev** | — | patterns+lessons+decisions+references | 路由后、进子技能前 (Step 4) |
| **req** | **raw/patterns** (可选) | **patterns** (只读整理后) | 深挖前 (Step 1.5) |
| **arch** | **raw/decisions** (可选) | **decisions + ADRs** (只读整理后) | 调研前 (Pre-Check) |
| **roadmap** | — | — | — |
| **feat** | **raw/patterns**(可选) + **raw/lessons**(应做) | **patterns+lessons** (只读整理后) | design/impl前 (Step 6，有明确需求时) |
| **issue** | **raw/lessons** (应做) | **lessons+patterns** (只读整理后) | analyze前 (issue-kb-retrieve，有明确需求时) |
| **kb** | raw (输入) → 正式目录 (输出) | **raw/** (整理输入) + 全部正式目录 (去重对照) | 整理触发时 |

**检索目标不含 `raw/` 和 `_archive/`。只有 kb 技能自身在整理时才读取 raw/。**

### 特性引入流程（小需求）
```
dev → req(收集需求) → arch(架构决策) → feat(design→impl→accept) → review(五轴审查) → ship(发布)
     ↓                  ↓                    ↓                      ↓                ↓
   写入 frontmatter    写入 frontmatter     checklist.yaml         review-report     tag+部署
                                                                     │
                                                                     security(门禁)
```

### 特性引入流程（大需求）
```
dev → req(收集需求) → roadmap(拆解规划) → arch(接口契约) → feat(item-1) → ... → review → ship
                         ↓                ↓
                   items.yaml          更新 status
```

**req vs roadmap 判定**: 见 Step 1 路由表中的区分规则

### 问题修复流程
```
dev → issue(report→analyze→fix) → [回归检查] → [可选: kb 记录 lesson]
                                ↓
                        [可选: review] (影响面大时)
```

### 发布流程
```
review approved → ship(git规范→安全门禁→changelog→部署策略→冒烟测试→监控确认)
                       ↑
                   security(final check)
```

### 知识沉淀流程
```
dev → kb(记录→分类) 或 在其他流程中嵌入式触发
```

## 变更传播机制（按需扫描，不用集中索引）

当任何文档被修改时：

### 1. 更新自身 frontmatter
- 改 `updated` 时间戳
- 如果是重大变更，设 `stale: true`

### 2. 找到下游依赖者（用 Grep 按需查找）
```
Grep pattern: "depends_on.*{当前文档id或路径}"
target: wiki/**/*.md
```
找到所有引用了本文档的下游文件。

### 3. 标记下游 stale
对每个找到的下游文档：
- 将其 frontmatter 中 `stale` 改为 `true`
- 更新其 `updated` 时间戳

### 4. 提示用户
> ⚠️ {文档ID} 已变更，以下关联文档可能需要同步更新:
> - {下游文档路径列表}

## YAML 文件读取规范（上下文控制）

**原则**: Agent 不得直接 Read 全量 YAML 文件，必须通过 `read-yaml.mjs` 脚本按需提取字段，控制上下文膨胀。

```bash
# 脚本位置: skills/init/references/tools/read-yaml.mjs

# 用法 1: 精确字段查询（推荐）
node read-yaml.mjs <file.yaml> --query "field1,field2"

# 用法 2: 数组展开
node read-yaml.mjs <file.yaml> --query "files[*].path"        # 所有元素的 path
node read-yaml.mjs <file.yaml> --query "files[?status==pending]"  # 过滤条件

# 用法 3: 快速摘要（~8 行输出）
node read-yaml.mjs <file.yaml> --summary

# 用法 4: 多文件冲突检测（flat 格式）
node read-yaml.mjs "wiki/features/*/impl-checklist.yaml" --query "meta.status,files[*].path" --flat
```

### 各阶段推荐查询

| 阶段 | 目的 | 推荐查询 | 预期输出量 |
|------|------|---------|-----------|
| **冲突检测** | 获取活跃 feat 的文件列表 | `meta.status,files[*].path` | ~5 行/文件 |
| **Review 评估** | 变更范围统计 | `--summary` 或 `files[*].path,steps[*].status` | ~10 行 |
| **Roadmap 对齐** | 获取优先级和依赖 | `items[*].title,items[*].status,items[*].priority` | ~8 行 |
| **状态检查** | 快速判断进度 | `meta.status,meta.current_step` | ~2 行 |
| **Ship 前置** | 检查所有门禁 | `security_check.status,meta.status` | ~3 行 |

### 反模式（禁止）

- ❌ 直接 `Read` 工具加载完整 `.yaml` 文件（可能数百行）
- ❌ 不用 `--query` / `--summary` 参数运行脚本
- ✅ 始终指定需要的字段，最小化上下文

## 冲突检测机制（局部扫描）

feat-impl 开始前执行：

### 1. 找到所有活跃 feature
```
Grep pattern: "status: implementing"
target: wiki/features/*/impl-checklist.yaml
```

### 2. 对比 files 列表
```bash
# 用脚本提取所有活跃 feat 的文件列表（每文件 ~5 行输出）
node skills/init/references/tools/read-yaml.mjs "wiki/features/*/impl-checklist.yaml" \
    --query "meta.status,files[*].path" --flat
```
将结果中的 `files[*].path` 与当前 feat 的 files 列表对比，检查路径重叠。

### 3. 有冲突则警告
```
⚠️ 检测到文件冲突:
  - src/components/Login.tsx 被 FEAT-002 同时修改
选项: [A] 等待对方完成  [B] 协调拆分文件  [C] 强制继续(风险自负)
```

## 原始信息存储规则

| 信息类型 | 存储路径 | 命名格式 |
|---------|---------|---------|
| 用户输入 | `wiki/raw/user-inputs/` | `YYYYMMDD-HHMMSS-{slug}.md` |
| 网络调研 | `wiki/raw/research/` | `{topic}.md` |
| 参考资料 | `wiki/raw/references/` | `{topic}.md` |

## 与各子技能的协作关系

| 上游技能 | 本技能动作 | 下游技能 | 触发条件 |
|---------|-----------|---------|---------|
| (无) | 接收用户输入 | onboard/req/arch/roadmap/feat/issue/review/security/ship/kb | 根据路由结果 |
| 首次使用 | 调用 | `onboard` | wiki/ 目录不存在或不完整 |
| req 完成(小需求) | 检查是否需要 arch | arch | 需求涉及系统设计 |
| req 完成(大需求) | 调用 | `roadmap` | 需求涉及 ≥ 3 模块或多迭代 |
| roadmap approved | 同步接口契约到 arch | `arch` + `feat` | 接口定义完成 |
| roadmap item 就绪 | 逐个启动 | `feat` | 按 p0→p1→p2 顺序 |
| arch 完成 | 检查是否可以 feat | feat | 架构已确定 |
| feat accept 通过 | 启动审查 | **review** | 非 ff 场景必须 |
| feat accept 通过(ff) | 可跳过 review 直接到 | **ship** | 小改动快速通道 |
| **review** approved | 启动发布 | **ship** | verdict == approved |
| **review** request_changes | 返回修复 | feat | 有 must 级 finding |
| **security** fail | 阻止发布 | — | ship Step 2 门禁不通过 |
| feat 完成 | 检查是否有可沉淀的知识 | kb (可选) | 发现好模式/踩坑 |
| issue 完成 | 检查是否需要回归测试 | feat-accept (可选) | 改动范围大 |
| issue 完成(影响面大) | 建议审查 | **review** (可选) | 核心模块修复 |

## 流程衔接责任矩阵

**原则：每个流程转换都有明确的"谁负责触发"和"谁负责执行"，避免悬空状态。**

| 转换点 | 触发责任方 | 执行动作 | 校验机制 |
|--------|-----------|---------|---------|
| req → arch | **dev** (路由判定) | dev 检查 req status==approved 后自动路由到 arch | arch 前置检查 req.stale==false |
| req → feat (跳过 arch) | **dev** (路由判定) | dev 判定需求简单后直接路由到 feat | feat 前置检查 req.stale==false |
| req → roadmap | **dev** (路由判定) | dev 判定大需求后路由到 roadmap | roadmap depends_on 引用 req |
| feat-accept → review (full) | **feat** (accept 子流程) | feat-accept 通过后自动调用 `review-generate.mjs` 并进入 review | review 前置检查 checklist.meta.status==done |
| feat-accept → review (lite) | **feat** (accept 子流程，可选) | feat 提示用户"是否需要 review"，用户确认后进入 | 同上 |
| feat-accept → ship (ff) | **feat** (accept 子流程) | ff 验收通过后直接进入 ship | ship 前置检查 checklist.mode==ff |
| review approved → ship | **review** (Step 3) | review 生成 verdict==approved 后提示进入 ship | ship Step 1 检查 review-report.yaml 存在 |
| review request_changes → feat | **review** (Step 3) | review 生成 verdict==request_changes 后返回 feat 修复 | feat 检查 review-report 中 action_items |
| feat 完成 → roadmap items 更新 | **feat** (accept 子流程) | feat-accept 通过后，更新关联 roadmap 的 items.yaml 中对应项 status=done | roadmap 前置检查 items.yaml |
| roadmap 最后一项 feat 完成 → roadmap done | **feat** (accept 子流程) | 最后一个 feat 完成时，检查 roadmap items.yaml 是否全部 done，是则更新 roadmap status=done | items.yaml 所有 features.status==done |
| issue 完成 → 回归检查 | **issue** (fix 子流程) | issue-fix 完成后自动执行回归检查清单 | 回归检查清单全部通过 |
| ship 完成 → AGENTS.md 更新 | **ship** (Step 3) | ship 更新 changelog 后同步更新 AGENTS.md 文档索引 | init Step 6 验证索引 |

**悬空状态检测**：如果任何文档的 status 长时间未变更（如 implementing 超 3 天），dev 路由时应提示用户确认是否需要继续。

## 技能清单（10 个）

| 技能 | 用途 | 输出位置 |
|------|------|---------|
| **init** | 项目初始化，生成骨架+模板+AGENTS.md | `wiki/` 全目录 + 项目根 `AGENTS.md` |
| **req** | 需求收集、分析、深挖 | `wiki/requirements/{slug}.md` |
| **arch** | 架构设计、技术决策 (ADR) | `wiki/architecture/{overview,decisions,modules}/` |
| **roadmap** | 大需求拆解、模块规划、接口契约 | `wiki/roadmaps/{slug}/` |
| **feat** | 特性设计、实现、验收（含 ff 快速通道） | `wiki/features/YYYY-MM-DD-{slug}/` |
| **issue** | 问题诊断、修复、回归 | `wiki/issues/{slug}-report.md` |
| **review** ★ | 五轴代码审查（正确性/安全/性能/可维护性/测试） | `wiki/features/*/review-report.yaml` |
| **security** ★ | 三层边界安全检查（输入/应用/基础设施） | `security-check.yaml` (附加到目标目录) |
| **ship** ★ | 发布部署（git规范/CI-CD门禁/灰度发布/回滚预案） | tag + changelog + `rollback-plan.yaml` |
| **kb** | 知识沉淀、模式复用（两阶段: raw→正式目录） | `wiki/knowledge/{patterns,lessons,...}/` |

★ = 本次新增
