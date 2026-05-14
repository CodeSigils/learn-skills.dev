---
name: kanban
description: "使用 /kanban 命令管理看板任务的全生命周期：初始化看板、创建 TASK-NNN 任务、执行阶段（plan/execute/evaluate）、归档完成、查看状态/进度、恢复中断任务、多迭代工作流。当用户提到 kanban、看板、TASK-NNN、/kanban 命令、任务创建/归档/恢复、或任何看板任务管理意图时使用此技能。"
---

# Kanban 多 Agent 编排系统

基于 FSM 的任务编排框架，将需求分析、编码执行、多角色评估、自迭代整合为标准化流程。

## Python 解释器约定

本文档中所有 `<py> -m core` 命令的 `<py>` 表示 `.kanban/config.json` 中 `python_bin` 字段的值。
编排器在执行命令前必须：读取 config.json → 提取 python_bin → 替换 `<py>` 为该值。

默认值: `python3`（当 config.json 未配置时）。

## 命令路由

### 自然语言路由

系统支持两种命令输入方式: **精确命令** 和 **自然语言**。路由优先级如下:

1. **优先匹配精确命令格式** -- 如果用户输入匹配 `/kanban <command>` 的精确格式 (如 `/kanban status`、`/kanban run TASK-001`)，直接进入对应命令的执行流程
2. **自然语言解析（LLM 推理）** -- 如果精确匹配失败，调用 `<py> -m core nlp` 获取命令列表和路由指导，由当前 LLM 推理用户意图并映射到对应命令。

#### 自然语言解析流程

```
1. <py> -m core nlp "$user_input"  → 返回 {"input": "...", "routing_guidance": {...}, "available_commands": [...]}
2. 当前 LLM 根据 routing_guidance + input 语义推理最匹配的命令
3. 直接执行匹配到的精确命令
```

#### 路由规则（不可绕过）

`routing_guidance` 字段提供意图检测和路由建议，编排器**必须遵循**：

| 意图 | 条件 | 路由到 | 示例 |
|------|------|--------|------|
| `work` | 含工作动词 + 无 task_id | `create` → `run` | "帮我实现贪食蛇" → 先创建任务再执行 |
| `work` | 含工作动词 + 有 task_id | `run` | "帮我处理 TASK-053" → 继续执行该任务 |
| `query` | 含查询动词 | `status` / `show` | "看看当前进度" → 显示状态 |
| `ambiguous` | 无法判断 | 询问用户 | 由编排器判断或 AskUserQuestion |

**硬性约束：** 当 `routing_guidance.intent == "work"` 时，编排器**禁止**直接执行工作内容，必须先路由到 `create` 创建任务再 `run` 执行。

---

### 精确命令列表

当用户调用 `/kanban` 时，解析子命令并执行:

```
/kanban init                                    # 初始化 .kanban/ 目录
/kanban create "<title>" [--desc "<desc>"] [--auto-mode <flags...>]  # 创建任务（flags: brainstorm|iteration|lightweight|all）
/kanban status                                  # 查看看板状态
/kanban show <task_id>                          # 查看任务详情
/kanban run <task_id>                           # 运行任务 (完整 FSM 循环)
/kanban run <task_id> --phase <phase>           # 从指定阶段运行
/kanban decide <task_id> --action <action>      # 用户决策
/kanban clean <task_id>                         # 清理指定已归档任务
/kanban clean --all                             # 清理所有已归档任务
/kanban clean --before <date>                   # 清理指定日期前的归档任务
/kanban recover [<task_id>]                     # 崩溃恢复
/kanban resume <task_id>                        # 恢复中断的任务
/kanban rollback <task_id>                      # 回滚中断的任务
/kanban evolve-skills                           # 查看 Skills 演化历史
/kanban score <task_id>                         # 查看评分
/kanban summary <task_id>                       # 迭代摘要
/kanban feedback <task_id>                      # 分析归档 inbox 反馈
/kanban inbox add <task_id> "<text>"            # 向任务 inbox.md 添加反馈项
/kanban inbox archive <task_id>                 # 归档已完成项到 inbox-archive.md
/kanban time [<task_id>]                        # 查看任务执行耗时
/kanban tokens <task_id>                        # 查看任务 Token 消耗
/kanban dashboard [start|stop|status|restart]   # 启动/停止 Dashboard
/kanban version list                            # 查看版本历史
/kanban version record <version> [--title ...] [--task TASK-NNN]  # 记录版本
/kanban subtask start <task_id> <subtask_id>   # 标记 subtask 开始
/kanban subtask done <task_id> <subtask_id>    # 标记 subtask 完成
/kanban progress <task_id>                      # 查看任务进度
/kanban knowledge search <keyword> [--tag <分类>] [--task <TASK-ID>]  # 搜索知识库
```

## 编排器决策清单（Orchestrator Decision Checklist）

编排器在每个阶段转换前**必须**逐项核对以下清单。这是防止流程跳跃、遗漏门禁的核心机制。

### 全阶段通用检查

- [ ] 当前阶段的所有 `required_artifacts` 已产出？→ 否则 Guard 阻止转换
- [ ] `<py> -m core guard check-artifacts "$task_id" <phase>` 返回 pass？→ 否则补全产物
- [ ] 转换前调用了 `<py> -m core workflow transition "$task_id" <next_phase>`？→ **禁止手动跳阶段**

### Plan → Plan Review

- [ ] spec.md 已产出（brainstorming 完成或合理跳过）？含功能需求、非功能需求、验收标准、模块设计
- [ ] plan.md 已由 writing-plans 产出？含实施策略、subtask 列表、TDD 步骤（非指针/摘要）
- [ ] task_breakdown.json 已生成（含 dependencies + parallelizable + file_ownership）？

### Plan Review → QA Spec

- [ ] plan_review_report.json 已产出（6 维度或串行回退）？
- [ ] 总分 >= `workflow.json plan_review.quality_gate.pass_threshold`？不达标 → 修订 plan.md 重试（最多 `max_rounds` 轮）

### QA Spec → Spec Review

- [ ] test_spec.md 已由 kanban-qa subagent 产出？→ **编排器禁止自行生成**
- [ ] spec_review_report.json 已由 kanban-test-spec-reviewer subagent 产出？→ **编排器禁止自行评审**
- [ ] 总分 >= `workflow.json spec_review.quality_gate.pass_threshold`？不达标 → 回到 qa_spec 修订（最多 `max_rounds` 轮）

### Execute → Evaluate

- [ ] 所有 subtask 已完成？→ progress.json 中每个 subtask status=completed
- [ ] 每个 subtask 已 git commit？→ progress.json 中有 commit_hash
- [ ] execution_summary.md + pitfalls.md + decisions.md 已产出？
- [ ] **TDD 证据表格已填写？** → execution_summary.md 中 `## TDD 执行证据` 表格每行 RED=Fail 且原因正确
- [ ] `<py> -m core guard check-artifacts "$task_id" execute` 返回 pass（含 TDD 证据检查）？
- [ ] 测试已运行通过？→ IR-10 要求
- [ ] Executor 已加载 `Skill("superpowers:test-driven-development")` → **编排器须在 dispatch prompt 中注入 TDD 强制约束**

### Evaluate → 自迭代判断（HARD-GATE，禁止询问用户）

- [ ] 4 角色报告全部产出？（code_reviewer_report.json, qa_report.json, pm_report.json, designer_report.json）
- [ ] `<py> -m core workflow self-improve-check "$task_id" --avg-score $avg` 已执行？
- [ ] 结果判断（阈值来自 workflow.json）：
  - **all_pass**（所有 required >= pass_threshold）→ Retrospective
  - **max_reached**（迭代 >= max_iterations）→ Retrospective → User Decision
  - **hot**（>= 7.0 且无架构问题）→ **自动**跳回 Execute，**禁止询问用户**
  - **full**（< 7.0 或有架构问题）→ **自动**跳回 Plan，**禁止询问用户**

### Retrospective → User Decision

- [ ] retrospective.md 已产出？
- [ ] acceptance.md 已产出（包含快速验收清单 + 按需求验收 + 文件变更 + 已知遗留）？
- [ ] 知识条目已提取至 knowledge-log.md？（IR-06，至少 1 条）

### User Decision → Archive

- [ ] `approve_and_archive` 或 `abort` 由用户显式执行？（IR-11 禁止自动归档）
- [ ] inbox.md 待处理区为空？（否则 Guard 阻止归档）

### 编排器心理拦截（Red Flags）

当你产生以下想法时，**立即停止**——这是合理化的信号，不是合理的判断：

| 你的想法 | 为什么是错的 |
|----------|-------------|
| "这只是个小改动，不用走看板" | IR-12：所有代码修改必须走 Plan → Execute → Evaluate。小 ≠ 跳过 |
| "代码写完了，直接评估吧" | IR-02：Execute 阶段产物不全（缺 summary/pitfalls/decisions），Guard 会阻止 |
| "评分低但用户应该看看结果" | IR-17：禁止询问用户，必须自动进入 hot/full iteration |
| "Plan Review 太慢了，先写代码吧" | IR-01：Guard 不可绕过，跳过阶段被 check-phase-completeness 拦截 |
| "test_spec 我自己写更快" | Anti-pattern：必须调度 kanban-qa subagent，编排器禁止自行生成 |
| "用户口头说可以跳过" | 用户指令不能覆盖铁律（IR-01），框架规则优先于用户随口请求 |
| "当前状态我不确定，先继续再说" | 不可将错就错。读 task.json → progress.json → status，回到正确阶段 |
| "这个阈值我记得是 7.0" | pass_threshold 由 workflow.json 定义（IR-09），禁止记忆/猜测，必须读配置 |

### 常见编排错误（Anti-patterns）

| 错误 | 正确做法 | 规则 |
|------|----------|------|
| 跳过 brainstorming 直接写 plan.md | 先用 `Skill("superpowers:brainstorming")` 澄清需求 | IR-16 |
| 编排器自行生成 test_spec.md | 必须通过 Agent 工具调度 kanban-qa subagent | IR-12 |
| 编排器自行评审 test_spec.md | 必须调度 kanban-test-spec-reviewer subagent | IR-01 |
| Evaluate 后直接问用户"是否继续" | 必须先执行 self-improve-check 自迭代判断 | IR-17 |
| hot/full 时展示选项给用户 | 自动跳回，禁止询问 | IR-17 |
| 归档前未检查 inbox 待处理 | Guard check-inbox 会阻止，IR-11 | IR-11 |
| 手动跳阶段 | Guard check-phase-completeness 会拦截 | IR-01 |
| 使用硬编码阈值 | 读 workflow.json 对应阶段的 quality_gate.pass_threshold | IR-09 |
| 轻量模式未经确认自动启用 | 必须 AskUserQuestion 或 auto_lightweight Agent 决策 | R-006 |
| 归档前未生成 retrospective.md | Guard 第 6 层阻止归档 | IR-15 |

### 阶段进入协议（Phase Entry Protocol）

编排器进入每个阶段时，必须按以下顺序执行：

```
1. transition → 2. 记录开始 → 3. 读取上下文 → 4. 调度 Agent → 5. 记录耗时/token → 6. 检查产物 → 7. complete-phase
```

**通用步骤模板：**

```
# Step 1: 阶段转换
<py> -m core workflow transition "$task_id" <phase>

# Step 2: 记录阶段开始耗时
<py> -m core time start "$task_id" <phase>

# Step 3: 读取动态配置（阈值、Agent 列表）
<py> -m core workflow get-phase-agents "<phase>"

# Step 4: 调度 Agent（按 workflow.json 中 agents 数组配置）
#  每个 Agent 完成后记录 token 和耗时:
#  <py> -m core tokens track "$task_id" <phase> --agent <role> --tokens <total_tokens>
#  <py> -m core time track "$task_id" <phase> --agent <role> --elapsed <seconds>

# Step 5: 记录阶段结束耗时
<py> -m core time end "$task_id" <phase>

# Step 6: Guard 产物检查
<py> -m core guard check-artifacts "$task_id" <phase>

# Step 7: 阶段完成
<py> -m core workflow complete-phase "$task_id"
```

**不确定时的恢复路径：** 如果编排器不确定当前状态或发现步骤遗漏：
1. 读取 `{task_dir}/task.json` → 查看 `phase`、`history`、`iteration` 字段
2. 读取 `{task_dir}/progress.json` → 查看各 subtask 完成状态
3. 执行 `<py> -m core status` → 获取 CLI 层面的任务状态
4. 如发现阶段跳跃 → 回到正确阶段重新执行，不可将错就错

---

## 命令速查与参考

详细实现见 [`references/commands.md`](references/commands.md)——编排器在需要查看具体步骤时按需读取。

### 创建与运行

| 命令 | 用途 |
|------|------|
| `/kanban init` | 初始化 .kanban/ 目录 + Agent 符号链接 + 基础设施检查 |
| `/kanban create "<title>" [--desc "..."] [--auto-mode ...]` | 创建任务。must AskUserQuestion 确认 auto_mode（除非用户已传 --auto-mode） |
| `/kanban run <task_id> [--phase <phase>]` | 运行任务 FSM 循环。--phase 指定起始阶段 |

### FSM 阶段流转（按顺序，禁止跳过）

| 阶段 | 核心动作 | 关键产物 |
|------|---------|----------|
| **Plan Step A** | `Skill("superpowers:brainstorming")` 需求澄清 | spec.md（含需求+设计） |
| **Plan Step B** | `Skill("superpowers:writing-plans")` 实施计划 | plan.md（含 complete TDD steps), task_breakdown.json |
| **Plan Review** | 6 维度并行评审（或串行回退） | plan_review_report.json |
| **QA Spec** | kanban-qa subagent 生成测试用例 | test_spec.md |
| **Spec Review** | kanban-test-spec-reviewer subagent 评审 | spec_review_report.json |
| **Execute** | kanban-executor subagent + `Skill("superpowers:test-driven-development")` RED→GREEN→REFACTOR | 代码 + execution_summary（含 TDD 证据）/pitfalls/decisions |
| **Evaluate** | 4 角色并行评估（code_reviewer/qa/pm/designer） | 4 份角色报告 JSON |
| **自迭代判断** | self-improve-check → all_pass/max_reached/hot/full | 自动跳转（IR-17） |
| **Retrospective** | 3 Agent 并行复盘 | retrospective.md, acceptance.md, 知识条目 |
| **User Decision** | 用户 approve_and_archive 或 abort | — |
| **Archive** | merge worktree + 清理 + 移动到 archive/ | IR-07, IR-11, IR-14 |

### 查询与监控

| 命令 | 用途 |
|------|------|
| `/kanban status` | 活跃任务状态 |
| `/kanban show <task_id>` | 任务详情 |
| `/kanban score <task_id>` | 评分详情 |
| `/kanban summary <task_id>` | 迭代摘要 |
| `/kanban progress <task_id>` | subtask 进度 |
| `/kanban time [<task_id>]` | 阶段耗时 |
| `/kanban tokens <task_id>` | Token 消耗 |

### 用户交互

| 命令 | 用途 |
|------|------|
| `/kanban decide <task_id> --action <action>` | approve_and_archive / abort / restart_from_plan / restart_from_execute |
| `/kanban feedback <task_id>` | 分析 inbox 反馈 |
| `/kanban inbox add <task_id> "<text>"` | 添加反馈 |
| `/kanban inbox archive <task_id>` | 归档已处理反馈 |

### 维护

| 命令 | 用途 |
|------|------|
| `/kanban recover [<task_id>]` | 崩溃恢复 |
| `/kanban resume <task_id>` | 从检查点恢复中断任务 |
| `/kanban rollback <task_id>` | 回滚到上一安全点 |
| `/kanban clean <task_id>\|--all\|--before <date>` | 清理归档任务 |
| `/kanban evolve-skills` | 查看 Skill 演化历史 |
| `/kanban version list` / `record` | 版本管理 |
| `/kanban knowledge search <kw>` | 搜索知识库 |
| `/kanban dashboard [start\|stop]` | Dashboard 管理 |

> **Python CLI:** 所有命令底层通过 `<python_bin> -m core <command>` 执行。首次 init 确定 python_bin（用户指定或创建 venv）。详见 `references/commands.md`。

---

## FSM 流转总览

```
Plan A (brainstorming)  →  Plan B (writing-plans)
  │  spec.md + plan.md + task_breakdown.json
  ▼
Plan Review (6 维评审)  ──→  plan_review_report.json
  ▼
QA Spec (kanban-qa subagent)  ──→  test_spec.md
  ▼
Spec Review (kanban-test-spec-reviewer)  ──→  spec_review_report.json
  ▼
Execute (TDD: RED→GREEN→REFACTOR)  ──→  code + execution_summary(含 TDD 证据)/pitfalls/decisions
  ▼
Evaluate (4 角色并行)  ──→  4 份角色报告 JSON
  ▼
自迭代判断 (HARD-GATE — 禁止询问用户)
  ├─ all_pass ──────→  Retrospective → User Decision → Archive
  ├─ max_reached ───→  Retrospective → User Decision → Archive
  ├─ hot ───────────→  Execute（自动，iter N+1，重新执行 TDD 循环）
  └─ full ──────────→  Plan（自动，iter N+1）
```

<HARD-GATE>
阶段顺序不可跳过。`complete-phase` 自动验证 history 包含全部前置阶段。
跳过任何阶段 → Guard 拦截 → 必须回退到正确阶段。不可将错就错。
</HARD-GATE>

- hot/full 自动跳转时**禁止**展示选项给用户
- Retrospective 仅在 all_pass/max_reached 时可达；User Decision 仅在自迭代用尽后可达
- 阶段阈值（pass_threshold、max_rounds、max_iterations）从 workflow.json 读取，禁止硬编码

---



## 规则按需加载

- `.claude/rules/kanban-rules.md` 由 Claude Code 自动注入上下文（IR-01~17 + R-001~006）
- `.claude/skills/kanban/references/` 下的参考文档**按需查阅**，不要预加载全部
- 具体命令实现细节 → 读 [`references/commands.md`](references/commands.md)

---

## Agent 调度规范

Agent 调度基于 `workflow.json` 的 `agents` 数组动态进行。每个阶段的 agent 配置从 `<py> -m core workflow get-phase-agents "<phase>"` 动态获取，编排器按配置调度，未定义时回退到内置默认行为。

各阶段的 Agent 调度模板已在上方各阶段章节中给出。此处仅补充通用约束。

### 自定义 Agent（agent_file）

workflow.json 的每个 agent 条目支持 `agent_file` 字段，指向项目自定义的 Agent 文件：

```json
{
  "id": "evaluate",
  "agents": [
    {
      "role": "code_reviewer",
      "agent_file": ".claude/agents/my-reviewer.md",
      "required": true
    }
  ]
}
```

**编排器调度规则：**
1. 如果 agent 条目有 `agent_file` → 使用该路径的 Agent 文件（调度时传入 file_path）
2. 如果 agent 条目有 `agent_type` 且无 `agent_file` → 使用 `agents/{agent_type}.md`
3. 如果两者都无 → 使用 `agents/kanban-{role}.md`

**自定义 Agent 约束：**
- role 保持不变（评分维度映射、报告命名依赖 role）
- 自定义 agent 必须兼容对应阶段的输入/输出规范
- 只读约束（`disallowedTools: [Write, Edit]`）对自定义 agent 同样生效

### 项目结构约定

`.kanban/config.json` 中的 `output_dir` 字段定义产出代码的根目录名。默认值: `"src"`。
task-name 使用下划线（Python 导入兼容）。

### 评估 Agent 调度要点

- 4 个评估角色从 `get-phase-agents evaluate` 动态获取，`run_in_background=true` 并行启动
- 评估 Agent 的 prompt 中包含预加载步骤（先列文件再读取），减少并行 I/O 冲突
- `required=false` 的评估 agent 评分不影响 pass_threshold 判断
- 评估类 Agent 通过 `disallowedTools: [Write, Edit]` 实现只读约束

---

## 路径规范

框架统一使用以下目录结构，Python CLI 内部处理所有路径解析:

```
task_dir(task_id)          # 任务目录: .kanban/tasks/TASK-NNN/
task_file(task_id)         # 任务 JSON: .kanban/tasks/TASK-NNN/task.json
report_dir(task_id, iter)  # 迭代产物目录: .kanban/tasks/TASK-NNN/iteration-N/
dispatch_dir(task_id)      # Dispatch 目录: .kanban/tasks/TASK-NNN/dispatch/
inbox_file(task_id)        # Inbox 文件: .kanban/tasks/TASK-NNN/inbox.md
archive_dir(task_id)       # 归档目录: .kanban/archive/TASK-NNN/
archive_task_file(task_id) # 归档 JSON: .kanban/archive/TASK-NNN/task.json
```

Python CLI 自动兼容新旧两种目录格式，优先检测新格式。

---

## 错误处理

- Guard 阻止时: 输出 "GUARD BLOCKED: {reason}"，停止当前阶段
- 产物缺失时: 提示 Agent 补全缺失的文件
- Agent 失败时: 记录到 history，标记 task 为 error 状态
- Worktree 冲突时: 提示用户手动解决

## 产物路径规则

内聚目录结构 (当前版本):

```
.kanban/
  config.json                    # 项目配置
  workflow.json                  # FSM 定义
  index.json                     # 看板索引
  tasks/TASK-NNN/
    task.json                    # 任务状态
    inbox.md                     # 用户反馈入口
    spec.md                      # Plan 产物（任务级，含需求+设计，不随迭代变化）
    plan.md                      # Plan 产物（任务级，含完整 TDD 实施步骤）
    task_breakdown.json          # Plan 产物（任务级，机器可读索引）
    retrospective.md             # 复盘文档（任务级，总结所有迭代）
    dispatch/
      TASK-NNN-execute.json      # Executor 调度上下文
      TASK-NNN-code_reviewer.json
      TASK-NNN-qa.json
      TASK-NNN-pm.json
      TASK-NNN-designer.json
    iteration-1/
      execution_summary.md       # Execute 产物
      execution_pitfalls.md      # Execute 产物
      execution_decisions.md     # Execute 产物
      framework_assessment.json  # 框架自评估产物
      code_reviewer_report.json
      qa_report.json
      pm_report.json
      designer_report.json
  archive/TASK-NNN/
    task.json                    # 归档后的任务 JSON
    inbox.md
    spec.md                      # 任务级文档归档
    plan.md
    task_breakdown.json
    retrospective.md
    iteration-1/
      ...
```

旧版目录结构兼容:
- 旧格式: `tasks/TASK-NNN.json`, `reports/TASK-NNN/`, `dispatch/`
- 框架自动检测并兼容旧格式，Python CLI 初始化时自动执行迁移
