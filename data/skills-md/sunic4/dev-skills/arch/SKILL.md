---
name: "arch"
description: "系统架构设计与技术决策。当需要进行技术选型、系统设计、接口定义或架构决策时调用此技能。输出存储到 wiki/architecture/。"
---

# Arch - 架构设计

## 职责
需求输入 → 技术调研 → 方案设计 → 决策记录 (ADR)

## 触发条件
- req 输出后需要系统设计方案
- 涉及技术选型/框架选择/架构模式决策
- 需要定义模块接口/数据流/状态管理方案
- 用户直接询问"怎么设计"/"用什么技术"

## 前置条件
- 必须有对应的 REQ 文档（或用户明确的设计目标）
- 如果上游 REQ 的 frontmatter 中 `stale: true`，**先同步 REQ 再继续**

## 工作流程

### Pre-Check: 历史决策检索（调研前）

在开始技术调研前，先检查**正式目录**中是否已有相关决策记录：

```
Grep pattern: "{决策领域关键词}"
target:
  - wiki/knowledge/decisions/*.md         ← 只读正式目录
  - wiki/architecture/decisions/*.md
```

**如果找到匹配的 ADR 或 decision**:
→ 直接引用，在新的 ADR 中注明"基于 ADR-XXX 的延续/修正"
→ **跳过重复调研**（除非决策已过时或场景不同）

**目的**: 避免对同一问题反复做技术选型。

### Step 1: 技术调研（如需要）
```
外部资料 → wiki/raw/research/{topic}.md
```
仅当涉及不熟悉的技术时进行，不要过度调研

### Step 2: 方案设计

输出到 `wiki/architecture/`，文档类型：

| 类型 | 路径 | 内容 |
|------|------|------|
| 系统总览 | `overview.md` | 技术栈、分层、模块清单（项目级，首次创建） |
| ADR 决策 | `decisions/ADR-{NNN}.md` | 单个技术决策的完整记录 |
| 模块设计 | `modules/{name}-module.md` | 单个模块的接口、依赖、文件结构 |

每个输出文档必须包含 frontmatter：

```yaml
---
id: "system-overview"             # 或 "state-mgmt" / "auth-module"
type: architecture
status: proposed                  # proposed | accepted | implemented | superseded | deprecated
title: "{标题}"
depends_on:
  - "../requirements/user-auth.md"   # 关联的需求文档
created: "2026-04-25T11:00"
updated: "2026-04-26T11:00"
stale: false
---
```

文档结构见 `references/architecture-documents.md`

### Step 3: 变更传播

ARCH 文档被修改时：

#### 1. 更新自身 frontmatter
- 改 `updated` 时间戳
- 设 `stale: true`（如果是重大变更）

#### 2. 找下游依赖者（Grep 按需扫描）
```
Grep pattern: "depends_on.*{当前ARCH id}"
target: wiki/features/**/design.md
```

#### 3. 标记下游 FEAT stale + 提示
> ⚠️ 架构已变更，以下特性实现可能受影响:
> - wiki/features/xxx/design.md

## ADR 决策流程

### 何时写 ADR
- 技术选型（框架、库、工具）
- 架构模式选择（分层、事件驱动、模块化）
- 重要约束决策（性能、安全、兼容性）

### ADR 必须包含
1. 背景：为什么需要做这个决策
2. 备选方案：至少 2 个选项 + 优缺点
3. 选择结果及理由
4. 后果：正面影响、负面影响、风险

### ADR 状态流转
```
proposed → discussed → accepted → implemented
           ↘ rejected
accepted → superseded (被新决策替代)
         → deprecated (不再相关)
```

## 与其他技能的协作

| 场景 | 下一步 | 条件 |
|------|--------|------|
| 设计完成，可以编码 | → `feat` | 方案已确定，接口已定义 |
| 设计中发现需求不清 | ↩ 回 `req` | 补充需求细节后重新设计 |
| 决策有参考价值 | → `kb` (可选) | ADR 同步到 kb/decisions/ |
| 多个需求共享同一架构 | 关联多个 REQ | 在 depends_on 中列出所有 REQ 路径 |

## 输出规范

| 项目 | 格式 |
|------|------|
| ADR 编号 | kebab-case 语义化名, 如 state-mgmt / auth-strategy / api-versioning (含 frontmatter) |
| 模块文件 | kebab-case: `{slug}-module.md` (含 frontmatter) |
| 总览文件 | 仅一份: `overview.md` (含 frontmatter) |
