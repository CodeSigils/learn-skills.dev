---
name: "retro"
description: "项目复盘与技能使用评估。当项目结束、迭代完成或用户要求复盘/总结/回顾时调用。生成技能使用报告和改进建议。"
---

# Retro - 项目复盘

## 职责

**技能使用统计 → 流程完整性检查 → 问题识别 → 改进建议 → 知识沉淀**

Retrospect 是项目结束时的"收尾者"，评估整个开发过程中技能的使用情况，识别问题并提出改进建议。

## 触发条件

| 条件 | 说明 |
|------|------|
| 项目正式结束 | 用户明确表示项目完成 |
| 迭代周期结束 | Sprint/里程碑完成 |
| 用户显式要求 | "复盘一下"、"总结项目"、"回顾一下" |
| 定期复盘 | 建议：每 2-4 周或每个大版本后 |

## 复盘流程

```
触发复盘
    │
    ▼
┌─────────────────────┐
│ Step 1: 数据收集     │
│ 扫描 wiki/ 目录结构   │
│ 统计各技能产出文件    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Step 2: 技能覆盖检查 │
│ 检查各技能是否被使用  │
│ 识别跳过的技能       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Step 3: 流程完整性   │
│ 检查每个技能的执行深度│
│ 识别未完成的流程     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Step 4: 流程衔接检查 │
│ 检查技能间转换是否正确│
│ 识别悬空/回退场景    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Step 5: 问题识别     │
│ 收集执行中的问题     │
│ 分析根本原因         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Step 6: 代码质量审计 │
│ 检查代码风格一致性   │
│ 识别反模式          │
│ 评估模板适用性       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Step 7: 生成报告     │
│ 输出复盘报告 YAML    │
│ 提出改进建议         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Step 8: 知识沉淀     │
│ 将复盘发现写入 kb    │
│ 更新技能定义（如需）  │
│ 更新模板（如需）      │
└─────────────────────┘
```

## Step 1: 数据收集

扫描以下目录，收集统计数据：

```
wiki/
├── requirements/        → req 技能产出
├── architecture/        → arch 技能产出
├── features/           → feat 技能产出
├── issues/             → issue 技能产出
├── reviews/            → review 技能产出
├── knowledge/          → kb 技能产出
├── roadmap/            → roadmap 技能产出
└── AGENTS.md           → init/ship 维护
```

**收集内容**：
- 各目录文件数量
- 文件创建时间分布
- 文件状态分布（如有 status 字段）

## Step 2: 技能覆盖检查

### Checklist

| 技能 | 检查项 | 做/没做 | 备注 |
|------|--------|---------|------|
| init | 项目初始化时调用 | ☐ | |
| req | 需求阶段使用 | ☐ | 如跳过：是否因需求简单？ |
| arch | 架构设计使用 | ☐ | 如跳过：是否因无需架构决策？ |
| roadmap | 大需求拆解使用 | ☐ | 如跳过：是否因无大需求？ |
| feat | 功能实现使用 | ☐ | |
| issue | Bug 修复使用 | ☐ | 如跳过：是否因无 Bug？ |
| review | 代码审查使用 | ☐ | 如跳过：是否因 lite/ff 模式？ |
| security | 安全检查使用 | ☐ | |
| ship | 发布部署使用 | ☐ | |
| kb | 知识沉淀使用 | ☐ | |

### 跳过技能分析

对于每个跳过的技能，判断：

| 跳过原因 | 是否合理 | 建议 |
|---------|---------|------|
| 不适用当前项目 | ✅ 合理 | 无 |
| 不知道有这个技能 | ❌ 需改进 | 加强技能文档/onboarding |
| 技能流程太繁琐 | ❌ 需改进 | 考虑简化流程或增加 lite 模式 |
| 忘记调用 | ❌ 需改进 | 加强流程衔接提示 |

## Step 3: 流程完整性检查

### req 技能完整性

| 检查项 | 做/没做 |
|--------|---------|
| 生成了需求文档 `wiki/requirements/{slug}.md` | ☐ |
| 执行了 deep-dive 追问（≥3 个问题） | ☐ |
| 文档包含验收标准 | ☐ |
| 文档包含技术约束 | ☐ |
| status 字段存在且有效 | ☐ |

### arch 技能完整性

| 检查项 | 做/没做 |
|--------|---------|
| 生成了 ADR 文档 | ☐ |
| ADR 包含背景/决策/后果 | ☐ |
| 定义了接口契约（如有） | ☐ |
| 更新了架构图（如有） | ☐ |

### feat 技能完整性

| 检查项 | 做/没做 |
|--------|---------|
| 正确选择了模式（full/lite/ff） | ☐ |
| 生成了 `impl-checklist.yaml` | ☐ |
| full 模式：执行了 design → impl → accept | ☐ |
| lite 模式：执行了 impl → accept | ☐ |
| ff 模式：执行了快速实现 | ☐ |
| 验收时逐项检查了 checklist | ☐ |
| 最终 status = done | ☐ |

### issue 技能完整性

| 检查项 | 做/没做 |
|--------|---------|
| 执行了边界判定 | ☐ |
| 生成了 `issue-report.yaml` | ☐ |
| 执行了 report → analyze → fix | ☐ |
| 修复后执行了回归检查 | ☐ |

### review 技能完整性

| 检查项 | 做/没做 |
|--------|---------|
| 生成了 `review-report.yaml` | ☐ |
| 完成了五轴评审 | ☐ |
| 给出了明确的 verdict | ☐ |
| request_changes 时追踪到修复 | ☐ |

### ship 技能完整性

| 检查项 | 做/没做 |
|--------|---------|
| 检查了所有 feat 的 checklist 状态 | ☐ |
| 生成了 `rollback-plan.yaml` | ☐ |
| 更新了 `CHANGELOG.md` | ☐ |
| 更新了 `AGENTS.md` | ☐ |

## Step 4: 流程衔接检查

### 衔接正确性

| 转换点 | 检查项 | 做/没做 |
|--------|--------|---------|
| req → arch/feat/roadmap | 有明确的触发动作 | ☐ |
| feat-accept → review | full 模式自动进入 review | ☐ |
| feat-accept → ship | ff 模式直接进入 ship | ☐ |
| review → ship/feat | 根据 verdict 正确路由 | ☐ |
| roadmap items ↔ feat | 状态同步更新 | ☐ |

### 异常场景

| 场景 | 检查项 | 做/没做 | 备注 |
|------|--------|---------|------|
| 流程悬空 | 出现不知道下一步的情况 | ☐ | 记录具体场景 |
| 流程回退 | review 不通过返回 feat | ☐ | 记录回退原因 |
| 流程跳跃 | 跳过某个必需步骤 | ☐ | 记录原因 |

## Step 5: 问题识别

### 问题分类

| 类别 | 检查项 | 做/没做 | 具体内容 |
|------|--------|---------|---------|
| 技能定义不清 | 遇到不知道如何执行的情况 | ☐ | |
| 流程不适配 | 现有流程无法满足需求 | ☐ | |
| 工具 Bug | 工具执行出错 | ☐ | |
| 文档缺失 | 找不到需要的文档 | ☐ | |
| 知识未沉淀 | 解决问题后未记录 | ☐ | |
| 绕过技能 | 直接操作而非使用技能 | ☐ | |

### 根因分析（5 Whys）

对于每个识别出的问题，执行 5 Whys 分析：

```
问题: {问题描述}
  │
  ▼ Why 1: {原因1}
  │
  ▼ Why 2: {原因2}
  │
  ▼ Why 3: {原因3}
  │
  ▼ Why 4: {原因4}
  │
  ▼ Why 5: {根本原因}
```

## Step 6: 代码质量审计

**目的**: 审计项目代码质量，为改进 `codestyle.md` 和 `AGENTS.md` 提供依据。

### 6.1 代码风格一致性检查

检查代码库是否遵循 `codestyle.md` 中定义的规范：

| 检查项 | 检查方法 | 一致性 | 问题记录 |
|--------|---------|--------|---------|
| 命名规范 | 扫描文件名/变量名/函数名 | ☐ 一致 / ☐ 不一致 | |
| 目录结构 | 检查是否符合约定 | ☐ 一致 / ☐ 不一致 | |
| 导入顺序 | 检查 import 语句顺序 | ☐ 一致 / ☐ 不一致 | |
| 代码格式 | 运行 linter 检查 | ☐ 一致 / ☐ 不一致 | |
| 类型使用 | 检查类型注解覆盖率 | ☐ 一致 / ☐ 不一致 | |

### 6.2 反模式检测

扫描代码库，识别常见反模式：

| 反模式类别 | 检测方法 | 发现数量 | 示例文件 |
|-----------|---------|---------|---------|
| 禁止的用法 | 搜索 codestyle.md 中禁止的模式 | | |
| 代码重复 | 检测相似代码块 | | |
| 过长函数 | 函数行数超过阈值 | | |
| 过深嵌套 | 嵌套层级超过阈值 | | |
| 未处理异常 | catch 块为空或仅打印日志 | | |
| 硬编码 | 魔法数字/字符串 | | |
| 循环依赖 | 模块依赖图检测 | | |

### 6.3 最佳实践遵循度

检查是否遵循语言/框架的最佳实践：

| 实践 | 检查项 | 遵循度 | 备注 |
|------|--------|--------|------|
| 错误处理 | 统一的错误处理策略 | ☐ 高 / ☐ 中 / ☐ 低 | |
| 日志规范 | 结构化日志、敏感信息脱敏 | ☐ 高 / ☐ 中 / ☐ 低 | |
| 测试覆盖 | 单元测试/集成测试覆盖率 | ☐ 高 / ☐ 中 / ☐ 低 | |
| 安全实践 | 输入验证、权限检查 | ☐ 高 / ☐ 中 / ☐ 低 | |
| 性能优化 | 懒加载、缓存、批量操作 | ☐ 高 / ☐ 中 / ☐ 低 | |

### 6.4 模板适用性评估

评估 `init` 时选择的模板是否适合项目实际情况：

| 评估项 | 模板定义 | 实际情况 | 是否需要调整 |
|--------|---------|---------|-------------|
| 命名约定 | {从模板} | {从代码} | ☐ 是 / ☐ 否 |
| 目录结构 | {从模板} | {从代码} | ☐ 是 / ☐ 否 |
| 技术栈描述 | {从模板} | {实际使用} | ☐ 是 / ☐ 否 |
| 禁止事项 | {从模板} | {发现的违规} | ☐ 是 / ☐ 否 |

### 6.5 生成改进建议

根据审计结果，生成对 `codestyle.md` 和 `AGENTS.md` 的改进建议：

```yaml
code_quality_audit:
  style_consistency:
    score: 85  # 0-100
    issues:
      - type: naming_inconsistency
        description: "部分组件文件使用 camelCase 而非 PascalCase"
        files: ["src/components/userProfile.tsx", "src/components/navBar.tsx"]
        suggestion: "统一使用 PascalCase 命名组件文件"
  
  anti_patterns:
    count: 5
    details:
      - type: unhandled_promise
        location: "src/services/api.ts:45"
        suggestion: "添加 .catch() 处理"
      - type: hardcoded_value
        location: "src/config/constants.ts:12"
        suggestion: "提取到环境变量"
  
  best_practices:
    error_handling: high
    logging: medium
    test_coverage: low
    security: high
    performance: medium
  
  template_improvements:
    codestyle_md:
      - action: "add_rule"
        section: "禁止事项"
        content: "❌ 禁止在组件文件中使用 camelCase 命名"
      - action: "update_section"
        section: "测试约定"
        content: "增加覆盖率要求说明"
    agents_md:
      - action: "update_section"
        section: "技术栈"
        content: "补充实际使用的状态管理方案"
      - action: "add_command"
        section: "常用命令"
        content: "npm run test:coverage"
```

### 6.6 输出到知识库

将审计发现写入 `wiki/knowledge/raw/code-quality-audit-{date}.yaml`，供 `kb` 技能整理后发布。

## Step 7: 生成报告

### 报告格式

生成 `wiki/retrospect/{YYYY-MM-DD}-retrospect-report.yaml`：

```yaml
meta:
  project_name: "{项目名}"
  retrospect_date: "YYYY-MM-DD"
  period_start: "YYYY-MM-DD"
  period_end: "YYYY-MM-DD"
  participants: []

statistics:
  skills_used:
    init: 1
    req: 5
    arch: 2
    feat: 12
    issue: 3
    review: 8
    security: 4
    ship: 3
    kb: 6
    roadmap: 1
  skills_skipped: []
  files_created:
    requirements: 5
    features: 12
    issues: 3
    reviews: 8
    knowledge: 6

coverage:
  - skill: init
    used: true
    skipped_reason: null
  - skill: req
    used: true
    skipped_reason: null
  - skill: arch
    used: false
    skipped_reason: "项目无架构变更需求"

completeness:
  - skill: feat
    total_invocations: 12
    fully_completed: 10
    partially_completed: 2
    incomplete: 0
  - skill: review
    total_invocations: 8
    fully_completed: 8
    partially_completed: 0
    incomplete: 0

transitions:
  - from: req
    to: feat
    count: 4
    issues: 0
  - from: feat
    to: review
    count: 8
    issues: 1
    issue_detail: "1次 review 不通过返回 feat 修复"

issues:
  - id: I1
    category: skill_definition
    description: "feat-lite 模式的验收标准不够清晰"
    severity: medium
    root_cause: "SKILL.md 中 lite 模式的 accept 步骤描述模糊"
    suggestion: "补充 lite 模式的验收 checklist"
  - id: I2
    category: tool_bug
    description: "validate-yaml.mjs 在 Windows 下路径解析错误"
    severity: high
    root_cause: "路径分隔符未统一处理"
    suggestion: "已修复，使用 path.normalize()"

improvements:
  - priority: high
    target: feat/SKILL.md
    action: "补充 lite 模式验收标准"
  - priority: medium
    target: dev/SKILL.md
    action: "增加更多意图识别关键词"
  - priority: low
    target: kb/SKILL.md
    action: "补充归档触发条件"

knowledge_captured:
  - title: "React useEffect 依赖正确写法"
    category: pattern
    source: issue-fix
  - title: "避免在循环中调用 setState"
    category: lesson
    source: feat-impl

next_actions:
  - "更新 feat/SKILL.md 补充 lite 验收标准"
  - "将 2 条知识条目整理到正式目录"
  - "安排下次复盘时间：2 周后"
```

### 报告摘要输出

```
📊 项目复盘报告 - {项目名}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 技能覆盖
  使用: init, req, feat, issue, review, ship, kb (7/10)
  跳过: arch (无架构变更), roadmap (无大需求), security (未涉及敏感数据)

📈 使用统计
  feat: 12 次 (full: 4, lite: 6, ff: 2)
  review: 8 次 (通过: 7, 需修改: 1)
  issue: 3 次 (已修复: 3)

⚠️ 发现问题
  - [中] feat-lite 验收标准不清晰
  - [高] validate-yaml Windows 路径问题 (已修复)

📝 改进建议
  1. [高] 更新 feat/SKILL.md 补充 lite 验收标准
  2. [中] 更新 dev/SKILL.md 增加意图关键词
  3. [低] 更新 kb/SKILL.md 补充归档条件

💡 知识沉淀
  - 新增 2 条知识条目待整理

📅 下次复盘: {YYYY-MM-DD}
```

## Step 8: 知识沉淀

### 写入 kb/raw/

将复盘中发现的有价值经验写入 `wiki/knowledge/raw/`：

```
wiki/knowledge/raw/
└── {YYYYMMDD-HHMM}-retrospect-{slug}.md
```

**写入内容**：
- 流程改进经验
- 工具使用技巧
- 常见问题解决方案
- 技能使用最佳实践
- 代码质量审计发现

### 更新技能定义

如果复盘中发现技能定义需要改进：

1. 在报告中记录改进建议
2. 询问用户是否立即更新 SKILL.md
3. 如用户同意，执行修改并记录变更

### 更新模板

根据代码质量审计结果，更新 `init/references/templates/` 中的模板：

| 触发条件 | 动作 |
|---------|------|
| 发现新的常见反模式 | 在模板的"禁止事项"中添加 |
| 发现新的最佳实践 | 在模板的相应章节添加 |
| 命名约定与实际不符 | 更新模板的命名约定 |
| 技术栈描述过时 | 更新模板的技术栈描述 |

**模板更新流程**：

1. 从审计结果中提取改进建议
2. 确定需要更新的模板文件
3. 询问用户是否更新模板
4. 如用户同意，更新模板并记录变更日志

**变更日志格式**：

```yaml
# wiki/knowledge/raw/template-changelog-{date}.yaml
changes:
  - date: "2024-01-15"
    template: "languages/typescript/codestyle.md"
    action: "add_rule"
    section: "禁止事项"
    content: "❌ 禁止在组件文件中使用 camelCase 命名"
    reason: "复盘发现多个组件文件命名不一致"
    source: "retro-2024-01-15"
```

## 与其他技能的关系

| 技能 | 关系 |
|------|------|
| dev | 读取 dev 的路由表，检查流程衔接 |
| kb | 将复盘发现写入 kb，读取已有知识 |
| init | 检查 AGENTS.md 索引完整性 |
| ship | 检查 CHANGELOG 更新情况 |
| 所有技能 | 统计使用情况，检查执行完整性 |

## 注意事项

1. **客观记录**：只记录事实，不做主观评价
2. **聚焦改进**：问题识别后必须有改进建议
3. **闭环追踪**：上次复盘的改进项需在本次检查完成情况
4. **知识优先**：复盘中发现的经验优先沉淀到 kb
5. **定期执行**：建议每个迭代或每 2-4 周执行一次
