---
name: write-prd
description: Guide users through creating comprehensive PRDs using JTBD + User Story Mapping + User Journey Mapping methodology. Systematically transform user jobs into structured requirements documents. | 使用「JTBD + 用户故事地图 + 用户旅程图」方法论，系统性地将用户任务转化为结构化的需求文档。
---

# PRD Creation Workflow | PRD 创建工作流

You are guiding the user through a systematic **9-step workflow** to create a comprehensive Product Requirements Document (PRD) based on the **JTBD (Jobs-to-be-Done)** methodology combined with **User Story Mapping** and **User Journey Mapping**.

您正在引导用户完成一个系统化的 **9 步工作流程**，基于 **JTBD（Jobs-to-be-Done）** 方法论，结合**用户故事地图**和**用户旅程图**，创建全面的产品需求文档（PRD）。

## When to Use This Skill | 何时使用此技能

Trigger this skill when users mention:
- **English**: "write PRD", "create PRD", "generate PRD", "product requirements document", "requirements doc"
- **中文**: "写PRD", "创建PRD", "生成需求文档", "产品需求文档", "需求文档"

## Core Methodology | 核心方法论

**JTBD** → Defines WHY and WHAT job users need to complete
**User Story Map** → Maps the step-by-step journey from 0 to 1
**User Journey Map** → Identifies WHERE to focus (emotions, pain points)
**User Stories** → Converts insights into structured requirements
**PRD** → Formalizes everything into comprehensive documentation

**JTBD** → 定义为什么做、用户要完成什么任务
**用户故事地图** → 将任务从 0 到 1 的步骤展开
**用户旅程图** → 识别关键节点（情绪、痛点）
**用户故事** → 将洞察转化为结构化需求
**PRD** → 形成完整的需求文档

## Workflow Overview | 工作流程概览

Present this overview at the start, then execute steps sequentially:

在开始时展示此概览，然后按顺序执行各步骤：

```
Step 1: Initialize Context | 初始化上下文
  └─ Collect product info, users, requirements, output path

Step 2: Define JTBD | 定义 JTBD
  └─ Create JTBD statement with Context/Task/Outcome

Step 3: Create Story Map | 创建故事地图
  └─ Map backbone steps and layer features (MVP/Enhanced/Delight)

Step 4: Add Journey Layer | 添加旅程层
  └─ Overlay emotions, pain points, and experience key points

Step 5: Generate User Stories | 生成用户故事
  └─ Convert map insights into structured user stories

Step 6: Structure PRD | 结构化 PRD
  └─ Organize into formal PRD document with all sections

Step 7: Quality Check | 质量检查
  └─ Validate against methodology standards

Step 8: Output Files | 输出文件
  └─ Generate jtbd.md, story_map.md, prd.md

Step 9: Next Steps | 后续步骤
  └─ Suggest validation, iteration, or workshop facilitation
```

## Execution Instructions | 执行指令

### STEP 1: Initialize Workflow Context | 初始化工作流上下文

**Collect the following information:**

1. **Product/Project Name** | 产品/项目名称
   - What product or feature are we creating a PRD for?
   - 为哪个产品或功能编写 PRD？

2. **Target User Persona** | 目标用户画像
   - Who are the primary users? (roles, responsibilities, scenarios)
   - 主要用户是谁？（角色、职责、典型场景）

3. **Initial Requirements** | 原始需求描述
   - What are the preliminary requirements or business goals?
   - 初步需求或业务目标是什么？

4. **Existing Materials** (optional) | 现有文档（可选）
   - Any competitive analysis, user interviews, pain point lists?
   - 是否有竞品分析、用户访谈、痛点列表等素材？

5. **Output Directory** | 输出路径
   - Where should we save the generated files?
   - 文件应保存在哪里？
   - Suggest: `{project-root}/prd/{product-name-date}/`
   - 建议：`{项目根目录}/prd/{产品名称-日期}/`

6. **Multiple JTBDs?** | 多条 JTBD？
   - If user has multiple JTBDs, confirm which one to process first
   - 如果有多条 JTBD，确认本次处理哪一条
   - **Recommendation**: Process one JTBD completely before starting another
   - **建议**：一次完整处理一条 JTBD

**Output**: Confirm all context information with user before proceeding.

---

### STEP 2: Define JTBD | 定义 JTBD

**Guide user to create a JTBD statement using the standard format:**

**引导用户使用标准格式创建 JTBD 陈述：**

```markdown
When I am in [SPECIFIC CONTEXT],
I want to [COMPLETE A TASK],
So that I can [ACHIEVE OUTCOME / AVOID RISK].

当我在【具体情境】时，
我想要【完成某个任务】，
以便于【获得某个结果/避免某个风险】。
```

**Example | 示例:**

> When I **need to report project progress to my manager every week**,
> I want to **generate a "key tasks completion + risks" report in 10 minutes**,
> So that I can **quickly explain if the project will be delayed and secure resource support**.

> 当我**每周要向老板汇报项目进度**时，
> 我想要**在 10 分钟内生成一份"关键任务完成情况+风险"的报告**，
> 以便于**快速说明项目是否会延期，并争取资源支持**。

**Decompose JTBD into 3 Design Anchors | 将 JTBD 拆解为 3 个设计锚点:**

1. **Context | 情境**: What scenario/timing triggers this need?
2. **Task | 任务**: What specific action does the user need to complete?
3. **Outcome | 结果**: What value does the user gain after completion?

**Output Format | 输出格式:**

```markdown
## JTBD Definition | JTBD 定义

### Core Statement | 核心句式
> When I am in [context],
> I want to [task],
> So that I can [outcome].

### Design Anchors | 设计锚点
- **Context | 情境**: ...
- **Task | 任务**: ...
- **Outcome | 结果**: ...

### Design Validation Standard | 后续设计检验标准
> Every feature/flow/interface must answer:
> "Does this step help users complete this JTBD more smoothly?"

> 任何功能/流程/界面设计都要能回答：
> "这一步，是在帮用户更顺利完成这个 JTBD 吗？"
```

---

### STEP 3: Create User Story Map | 创建用户故事地图

**3.1 Draw Backbone (Top Layer) | 画主干任务线（上层）**

**Core Question**: From 0 to completing this JTBD, what key steps will users go through in chronological order?

**核心问题**：用户从 0 开始，要完成这个 JTBD，按时间会经历哪些关键步骤？

**Example | 示例**: Open product → Login → Select project → View overview → Drill into details → Export report

List 5-10 key steps from left to right in time order.

从左到右按时间顺序列出 5-10 个关键步骤。

**3.2 Hang Activities/Features (Middle Layer) | 在每一步下挂具体活动/功能（中层）**

Under each backbone step, list operations users might do or capabilities the system provides.

在每个主干步骤下，列出用户可能的操作或系统提供的能力。

**Example | 示例:**
- ④ View Progress Overview
  - Auto-summarize "completed/in-progress/delayed tasks"
  - Progress percentage chart
  - Risk task count alert

**3.3 Vertical Prioritization (Layering) | 纵向分优先级（分层）**

- **Layer 1 - MVP Must-Have**: Without this, cannot complete JTBD
- **Layer 2 - Enhanced Experience**: With this, efficiency significantly improves
- **Layer 3 - Delighter**: Nice-to-have, may not do in first release

- **第一层 - MVP 必须有**：没有就无法完成 JTBD
- **第二层 - 增强体验**：有了效率明显提升
- **第三层 - 锦上添花**：首期可不做

**Output Format | 输出格式:**

```markdown
## User Story Map | 用户故事地图

### Backbone Flow | 主干流程
1. [Step 1] → 2. [Step 2] → ... → N. [Step N]

### Feature Layering Details | 功能分层明细

#### Step 1: [Step Name]
- **MVP**:
  - Feature A
  - Feature B
- **Enhanced**:
  - Feature C
- **Delighter**:
  - Feature D

#### Step 2: [Step Name]
...
```

---

### STEP 4: Overlay User Journey Map | 叠加用户旅程图

**For each backbone step, add these dimensions:**

**为每个主干步骤补充以下维度：**

1. **User Goal | 用户目标**: What does the user want to achieve at this step?
2. **Current/Expected Emotion | 当前/预期情绪**: User's psychological state (anxious? calm? excited?)
3. **Main Pain Points/Risks | 主要痛点/风险**: Where things might go wrong, common complaints

**Output Format (Table) | 输出格式（表格）:**

```markdown
## User Journey Overlay | 用户旅程叠加

| Step | User Goal | Current/Expected Emotion | Main Pain Points/Risks |
|------|-----------|--------------------------|------------------------|
| ① Login | Quickly enter system | Frustrated if slow | High SSO failure rate |
| ② Select Project | Find project to report | Anxious if many projects | Slow search/messy list |
| ... | ... | ... | ... |
```

**Mark Experience Key Points | 标记体验关键节点:**

Use ⚠️ to mark steps with high emotional fluctuation or severe pain points. These are where design needs to focus optimization efforts.

在表格中用 ⚠️ 标出情绪波动大、痛点严重的步骤。这些节点是后续设计需要重点优化的地方。

---

### STEP 5: Generate User Stories | 生成用户故事

**Use standard User Story template:**

**使用标准用户故事模板：**

```markdown
As a [USER TYPE],
When [IN SPECIFIC CONTEXT / AT STORY MAP STEP],
I want to [COMPLETE AN ACTION IN SOME WAY],
So that I can [ACHIEVE JTBD OUTCOME / ALLEVIATE PAIN POINT].

作为【某类用户】，
当【处于某个情境/来到故事地图上的某一步】时，
我希望【通过某种方式完成某个动作】，
以便于【达成 JTBD 中的结果 / 缓解某个痛点】。
```

**Generation Rules | 生成规则:**

- One backbone step typically corresponds to 1-3 User Stories
- 一个主干步骤通常对应 1-3 条用户故事
- User Story sources:
  - **Who**: From JTBD role
  - **When/Context**: From JTBD + story map step
  - **What to do**: From story map activities/features
  - **Why**: From JTBD outcome + journey map emotions/pain points

**Example Output | 示例输出:**

```markdown
## User Story List | 用户故事列表

### For Step: ④ View Progress Overview

**US-001**
> As a **Project Manager**,
> When I **open the project overview page before weekly reporting**,
> I want to **see all key task completion ratios and delay risks on one page**,
> So that I can **judge project health in seconds and decide if I need to explain risks in the meeting**.

**Acceptance Criteria | 验收标准**:
- [ ] Page load time < 3 seconds
- [ ] Display task completion percentage (completed/total)
- [ ] Delayed tasks have obvious red indicators

### For Step: ⑤ View Delayed Tasks
...
```

---

### STEP 6: Structure into PRD | 结构化成 PRD

**Use standard PRD chapter structure:**

**使用标准 PRD 章节结构：**

```markdown
# Requirement Name: [Feature Name] (围绕 JTBD: [JTBD Brief])

## 1. Background & JTBD
- JTBD description (complete statement)
- User roles & usage scenarios
- Current pain points (from journey map)

## 2. User Journey & Main Flow (from story map)
- Backbone flow step list
- Simplified journey map (mark key emotions & pain points)

## 3. Functional Requirements (User Stories List)
### 3.1 [Module/Step Name]
- User Story 1 (with acceptance criteria)
- User Story 2
- ...

### 3.2 [Module/Step Name]
- User Story 3
- ...

## 4. Interaction & Interface Key Points
- Key interface sketches/prototype links for each step
- Where obvious feedback/prompts are needed (from emotion/pain point analysis)

## 5. Acceptance Criteria & Metrics
- Summary of acceptance conditions for each User Story
- Behavioral metrics: average time to complete XX, feature usage rate, error rate, etc.

## 6. Scope & Priority
- MVP scope (must-do this release)
- Enhanced features (next iteration)
- Delighters (TBD)

## 7. Risks & Dependencies
- Technical dependencies
- Business risks
- Questions to clarify
```

**Add Acceptance Criteria (AC) for each User Story:**

**为每条用户故事补充验收标准（AC）：**

Use Given-When-Then or simple Checklist format. Ensure testable and verifiable.

使用 Given-When-Then 或简单的 Checklist 格式。确保可测试、可验证。

---

### STEP 7: Quality Check | 质量检查

**Self-check Checklist (verify each item):**

**自检清单（请逐条验证）：**

- [ ] All feature designs can answer "Does this help users complete the JTBD?"
- [ ] User Story sources are traceable (can map to specific story map steps)
- [ ] High emotional fluctuation points in journey map have corresponding UX optimizations in PRD
- [ ] Every User Story has clear acceptance criteria
- [ ] Priority layering is clear (MVP / Enhanced / Delighter)

- [ ] 所有功能设计都能回答"是在帮用户完成 JTBD 吗？"
- [ ] 用户故事来源可追溯（能对应到故事地图的具体步骤）
- [ ] 旅程图中的高情绪波动点在 PRD 中有对应的体验优化设计
- [ ] 每条用户故事都有明确的验收标准
- [ ] 优先级分层清晰（MVP / 增强 / 锦上添花）

**Suggest PRD Validator Agent:**

If user wants automated validation, suggest:
> "Would you like me to run the PRD Validator agent to automatically check quality against all methodology standards?"

如果用户需要自动化验证，建议：
> "是否需要运行 PRD 验证代理，自动检查文档是否符合所有方法论标准？"

---

### STEP 8: Output Final Files | 输出最终产物

**Generate three files in the specified output directory:**

**在指定输出目录生成三个文件：**

1. **`jtbd.md`**: JTBD definition and design anchors
2. **`story_map.md`**: User story map + user journey overlay
3. **`prd.md`**: Complete PRD document

**File Structure | 文件结构:**

```
{output-directory}/
├── jtbd.md           # JTBD 定义与设计锚点
├── story_map.md      # 用户故事地图 + 用户旅程叠加
└── prd.md            # 完整 PRD 文档
```

Use the **Write** tool to create each file with the content generated in previous steps.

使用 **Write** 工具创建每个文件，内容来自前面步骤生成的内容。

---

### STEP 9: Next Steps & Iteration | 后续步骤与迭代

**Present completion summary and suggest next actions:**

**展示完成总结并建议后续行动：**

```markdown
## ✅ PRD Creation Complete | PRD 创建完成

### Generated Files | 已生成文件
- ✅ {path}/jtbd.md
- ✅ {path}/story_map.md
- ✅ {path}/prd.md

### Quality Status | 质量状态
- [X] JTBD defined with design anchors
- [X] Story map with MVP/Enhanced/Delighter layers
- [X] Journey map with emotions and pain points
- [X] User stories with acceptance criteria
- [X] Complete PRD with all sections

### Recommended Next Steps | 建议后续步骤

1. **Validate Quality | 验证质量**
   - Run PRD Validator agent for automated quality check
   - 运行 PRD 验证代理进行自动化质量检查

2. **Team Review | 团队评审**
   - Share with stakeholders for feedback
   - 与利益相关者分享以获取反馈

3. **Iterate | 迭代**
   - If JTBD changes fundamentally, re-run workflow
   - 如果 JTBD 发生根本性变化，重新运行工作流
   - For detail additions, directly edit existing documents
   - 如补充细节，可直接编辑现有文档

4. **Workshop Facilitation | 工作坊引导**
   - Use this PRD as basis for 2-3 hour team workshop
   - 使用此 PRD 作为 2-3 小时团队工作坊的基础
   - See references/workshop-guide.md for facilitation tips
   - 参见 references/workshop-guide.md 获取引导技巧

5. **Process Additional JTBDs | 处理其他 JTBD**
   - If you have more JTBDs, repeat Steps 2-8 for each
   - 如有更多 JTBD，对每条重复步骤 2-8
```

---

## Error Handling | 错误处理

### If user cannot provide clear JTBD | 如用户无法提供清晰的 JTBD

- Guide user to conduct user interviews or review existing pain point lists first
- 引导用户先做用户访谈或回顾已有痛点列表
- Provide 3-5 JTBD templates for reference (see `references/jtbd-framework.md`)
- 提供 3-5 个 JTBD 模板供参考（见 `references/jtbd-framework.md`）

### If certain steps lack pain point/emotion information | 如某些步骤缺乏痛点/情绪信息

- Mark as "To Be Validated" in journey map
- 在旅程图中标记为"待验证"
- Suggest conducting user testing or interviews to supplement
- 建议进行用户测试或访谈后补充

### If too many User Stories (>20) | 如用户故事过多（>20 条）

- Output in batches by backbone steps
- 按主干步骤分批输出
- Or output MVP layer User Stories first, Enhanced layer later
- 或先输出 MVP 层的用户故事，增强层后续补充

---

## Supporting Resources | 支持资源

For detailed methodology explanations, templates, and examples, refer to:

详细的方法论说明、模板和示例，请参考：

- **`references/jtbd-framework.md`** - JTBD methodology deep dive
- **`references/story-mapping.md`** - User Story Mapping guide
- **`references/journey-mapping.md`** - User Journey Mapping guide
- **`references/templates.md`** - All templates and formats
- **`examples/example-project-management.md`** - Complete worked example
- **`examples/example-templates.md`** - Template collection

---

## Key Principles | 关键原则

1. **JTBD is the North Star** - Every design decision must trace back to helping users complete the JTBD
2. **Progressive Disclosure** - Start with backbone, then add layers, then add details
3. **Evidence-Based** - Journey map emotions and pain points should come from real user research
4. **Traceability** - Every User Story should map to a specific story map step
5. **Iterative** - PRDs are living documents that evolve with user feedback

1. **JTBD 是北极星** - 每个设计决策都必须追溯到帮助用户完成 JTBD
2. **渐进式披露** - 先主干，再分层，再细节
3. **基于证据** - 旅程图的情绪和痛点应来自真实用户研究
4. **可追溯性** - 每条用户故事都应映射到具体的故事地图步骤
5. **迭代性** - PRD 是随用户反馈演进的活文档

---

## Execution Checklist | 执行检查清单

Before completing the workflow, ensure:

完成工作流前，确保：

- [ ] User has provided all context information (Step 1)
- [ ] JTBD has clear Context/Task/Outcome (Step 2)
- [ ] Story map has backbone + layered features (Step 3)
- [ ] Journey map has emotions + pain points (Step 4)
- [ ] User Stories have acceptance criteria (Step 5)
- [ ] PRD has all required sections (Step 6)
- [ ] Quality checklist passed (Step 7)
- [ ] All three files generated (Step 8)
- [ ] Next steps suggested (Step 9)

Now begin by presenting the workflow overview and asking the user for context information to start Step 1.

现在开始，先展示工作流程概览，然后询问用户上下文信息以启动步骤 1。
