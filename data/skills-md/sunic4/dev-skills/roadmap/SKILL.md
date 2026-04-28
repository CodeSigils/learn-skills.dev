---
name: "roadmap"
description: "大需求拆解与规划。当用户提出的需求涉及多个模块、多个迭代周期、或需要先做架构层设计时调用。将一个大需求拆成子 feature 清单，定义接口契约和共享协议，作为 req → feat 之间的规划层。"
---

# Roadmap - 大需求拆解与规划

## 职责
把一个**大需求**拆成可独立执行的 **子 feature 列表**，附带：
- 模块划分（概设）
- 接口契约（架构层详设）
- 子 feature 拆解清单（含优先级和依赖关系）

## 触发条件
以下任一情况触发 roadmap 而非直接进 feat：
- 需求涉及 **≥ 3 个模块/子系统**
- 预估工作量 **> 1 个迭代周期**
- 用户明确说"系统"、"平台"、"整套"等词
- 需要先做**跨模块接口设计**才能开始实现
- 需求本身包含 **≥ 3 个可独立交付的功能点**

## 执行流程

```
用户输入大需求
    │
    ▼
┌─────────────────┐
│ Step 1: 规模评估 │ ← 判断是否需要 roadmap
└────────┬────────┘
         │
    ┌────┴────┐
    │ ≤2 模块? │──是──→ 直接走 req → arch → feat (不需要 roadmap)
    └─────────┘
         │ 否
         ▼
┌─────────────────┐
│ Step 2: 模块划分 │ ← 拆成子系统/模块
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Step 3: 接口契约 │ ← 定义模块间通信协议
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Step 4: 拆子feature│ ← 生成可执行的 feature 清单
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Step 5: 输出     │ ← 写入 wiki/roadmaps/
└─────────────────┘
```

### Step 1: 规模评估

| 维度 | 小需求 (直接 feat) | 大需求 (走 roadmap) |
|------|-------------------|---------------------|
| 涉及模块数 | 1-2 | ≥ 3 |
| 文件改动量 | < 10 | ≥ 10 |
| 迭代周期 | < 3 天 | ≥ 3 天 |
| 功能点数 | 1-2 | ≥ 3 |
| 是否需跨模块接口 | 否 | 是 |

**判断**: 任一维度命中"大需求"列 → 走 roadmap。

### Step 2: 模块划分（概设）

输出到 `wiki/roadmaps/{slug}/` 目录：

```yaml
---
id: "{slug}"
type: roadmap
status: planning                # planning | approved | in-progress | done | abandoned
title: "{标题}"
depends_on:
  - "../requirements/{req-slug}.md"
created: "YYYY-MM-DDTHH:MM"
updated: "YYYY-MM-DDTHH:MM"
stale: false
---
```

**模块划分规则**:

1. 按**职责边界**分（不是按文件/组件分）
   - ✅ 认证模块 / 支付模块 / 通知模块
   - ❌ 登录页面 / 注册页面 / 忘记密码页面（这些是一个模块的 UI）

2. 每个模块输出一张卡片：

```markdown
## 模块: {名称}

| 属性 | 值 |
|------|-----|
| 职责 | 一句话描述该模块负责什么 |
| 边界 | 输入是什么，输出是什么，不做什么 |
| 依赖 | 依赖哪些其他模块 |
| 复杂度 | high / medium / low |
| 风险点 | 已识别的技术风险 |

### 核心能力列表
- [ ] 能力 1
- [ ] 能力 2
- [ ] ...
```

3. 模块间画依赖图（ASCII）：

```
                    ┌──────────┐
                    │  前端 UI  │
                    └────┬─────┘
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │  认证服务  │ │  用户服务  │ │  权限服务  │
        └────┬─────┘ └────┬─────┘ └────┬─────┘
             │            │            │
             ▼            ▼            ▼
        ┌──────────────────────────────────┐
        │           数据存储层               │
        └──────────────────────────────────┘
```

### Step 3: 接口契约（架构层详设）

对每个**跨模块交互**定义接口：

```markdown
## 接口: {名称}

| 属性 | 值 |
|------|-----|
| 方向 | A → B（谁调谁）|
| 协议 | HTTP REST / gRPC / 内部函数 / Event |
| 格式 | JSON / Protobuf / TypeScript 类型 |
| 认证 | 如何鉴权 |
| 幂等性 | 是否支持重复调用 |

### Request
{字段定义}

### Response
{字段定义 + 错误码}

### Error Cases
| 场景 | HTTP码 | 错误信息 | 处理方式 |
|------|--------|---------|---------|
| 未认证 | 401 | ... | 重定向登录 |
| 参数非法 | 400 | ... | 返回具体字段错误 |
| 服务不可用 | 503 | ... | 重试/降级 |
```

**关键原则**:
- 只定义**跨模块**接口，模块内部实现细节留给各 feat 的 design.md
- 接口一旦被下游 feat 使用，变更必须走 ADR 流程
- 共享类型/常量放在 `wiki/architecture/shared-types.md`

### Step 4: 拆子 Feature 清单

生成 `items.yaml`:

```yaml
# wiki/roadmaps/{slug}/items.yaml
roadmap: "{slug}"

features:
  - id: "{feat-slug-1}"              # 如 user-registration
    title: "用户注册"
    priority: p0                     # p0(阻塞) / p1(重要) / p2(优化)
    depends_on: []                   # 同一 roadmap 内的其他 feat id
    estimated_files: 5               # 预估改动文件数
    modules: ["auth-service", "db"]  # 涉及的模块
    status: todo                     # todo | doing | done | skipped

  - id: "{feat-slug-2}"              # 如 email-verification
    title: "邮箱验证"
    priority: p0
    depends_on: ["user-registration"] # 等注册完成后才能验证
    estimated_files: 4
    modules: ["auth-service", "notification-service"]
    status: todo

  - id: "{feat-slug-3}"
    title: "..."
    ...

shared_tasks:                        # 所有 feat 共享的前置工作
  - id: setup-auth-module
    title: "搭建认证模块骨架"
    status: todo
    blocks: ["user-registration", "email-verification"]  # 阻塞哪些 feat
```

**拆分规则**:

| 规则 | 说明 |
|------|------|
| **单一职责** | 每个 feat 只做一个内聚的功能点 |
| **可独立验收** | 每个 feat 完成后可以单独测试和上线 |
| **依赖最小化** | 减少 feat 间的 depends_on，允许并行开发 |
| **粒度适中** | 单个 feat 预估 0.5~3 天完成。过大继续拆，过小合并 |
| **P0 先行** | p0 feat 无 depends_on 或只依赖已完成的 feat |

### Step 5: 输出结构

```
wiki/roadmaps/{slug}/
├── {slug}-roadmap.md        # 主文档：概设 + 模块划分 + 接口契约 + 依赖图
├── items.yaml               # 子 feature 清单 + 优先级 + 依赖关系
└── drafts/                  # 设计草稿（可选）
    ├── {draft-name}-1.md
    └── {draft-name}-2.md
```

**主文档模板** (`{slug}-roadmap.md`):

```markdown
---
id: "{slug}"
type: roadmap
status: planning
title: "{标题}"
depends_on:
  - "../requirements/{req-slug}.md"
created: "2026-04-26T10:00"
updated: "2026-04-26T10:00"
stale: false
---

# {标题}

## 背景
{为什么需要这个 roadmap，关联的需求是什么}

## 模块划分
{Step 2 的产出}

## 接口契约
{Step 3 的产出}

## 子 Feature 清单
{引用 items.yaml，或在此处列出摘要表}

## 里程碑
| 阶段 | 目标 | 包含 feat | 预期产出 |
|------|------|-----------|---------|
| Phase 1 | 核心流程跑通 | feat-a, feat-b | 可用但缺边界处理 |
| Phase 2 | 完善体验 | feat-c, feat-d | 生产可用 |
| Phase 3 | 优化增强 | feat-e | 性能/监控完善 |

## 风险与缓解
| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| ... | ... | ... |
```

## 与其他技能的关系

### 上游
- **req**: roadmap 的输入来自 req 产出的需求文档（通过 frontmatter `depends_on` 关联）

### 下游
- **arch**: roadmap 中的接口契约应同步写入 architecture/decisions/ 和 shared-types.md
- **feat**: roadmap 的 items.yaml 中每个 feat 项对应一个独立的 feat 工作流

### 执行顺序

```
req → roadmap → arch(接口契约) → feat(item-1) → feat(item-2) → ...
                  ↓
              更新 items.yaml status
```

**执行规则**:
1. roadmap approved 后，按 p0 → p1 → p2 顺序逐个启动 feat
2. 每个 feat 完成后更新 `items.yaml` 对应项的 status 为 `done`
3. 所有 feat 完成后，roadmap status 设为 `done`
4. 如果某个 feat 在实施中发现需要调整方案，回退到 roadmap 修改 items.yaml 再继续

**状态同步机制（feat ↔ roadmap）**:

| 事件 | 责任方 | 动作 | 校验 |
|------|--------|------|------|
| feat-accept 通过 | **feat** | 更新关联 roadmap 的 `items.yaml` 中对应项 `status: done` | 读取 items.yaml 确认更新成功 |
| feat-accept 通过（最后一个 feat） | **feat** | 额外检查 items.yaml 所有 features.status==done，若是则更新 roadmap 主文档 `status: done` | 读取 roadmap frontmatter 确认 |
| feat 被放弃 (abandoned) | **feat** | 更新 items.yaml 对应项 `status: skipped`，检查是否阻塞下游 feat | 如阻塞则提示用户 |
| feat 实施中发现需调整方案 | **feat** | 回退到 roadmap，修改 items.yaml（新增/拆分/调整依赖） | 修改后重新校验依赖链无环 |
| roadmap 接口契约变更 | **roadmap** | 标记所有未完成 feat 的 design.md `stale: true` | Grep 检查下游 |

**items.yaml 更新模板**:
```bash
# feat 完成后执行
node wiki/tools/read-yaml.mjs wiki/roadmaps/{slug}/items.yaml --query "features[*].id,features[*].status"
# 确认当前 feat 的 status 已更新为 done
```

## 变更传播

roadmap 变更时检查：
- Grep `"depends_on.*roadmaps/{slug}"` → 标记关联 feat stale
- 如果接口契约变更 → 同时标记关联 arch 文档 stale
