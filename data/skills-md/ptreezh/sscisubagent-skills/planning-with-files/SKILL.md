---
name: planning-with-files
description: 基于文件的规划和进度跟踪技能，为研究项目提供结构化的任务规划、进度监控和发现记录功能
version: 1.0.0
author: socienceAI.com
license: MIT
tags: [planning, project-management, progress-tracking, research-methodology, file-based-workflow]
compatibility: Claude 3.5 Sonnet and above
metadata:
  domain: research-project-management
  methodology: file-based-planning
  complexity: intermediate
  integration_type: supporting_tool
  last_updated: "2026-01-23"
allowed-tools: [python, bash, read_file, write_file]
---

# Planning with Files 技能

## 概述

Planning with Files 技能为研究项目提供基于文件的规划和进度跟踪功能。该技能遵循 "planning with files" 理念，通过三个核心文件（任务计划、进度跟踪、发现记录）来管理系统性研究项目的执行过程。

## 使用时机

当用户请求以下操作时使用此技能：

- 研究项目的结构化规划
- 任务进度的系统性跟踪
- 研究发现的规范化记录
- 多阶段研究流程的管理
- 与其他研究技能的集成规划

## 快速开始

当用户请求项目规划时：

1. **初始化**：创建规划工作空间和三个核心文件
2. **规划**：制定详细的任务计划和时间线
3. **跟踪**：记录每日进度和里程碑
4. **记录**：整理研究发现和洞察
5. **监控**：评估项目状态和完成度

## 核心功能（渐进式披露）

### 主要功能

- **工作空间初始化**：创建规划所需的目录结构和文件
- **任务规划**：生成结构化的任务计划文档
- **进度跟踪**：维护项目进度和时间记录
- **发现记录**：整理研究过程中的关键发现

### 次要功能

- **状态监控**：实时评估项目完成度
- **文件同步**：确保各文档间的一致性
- **里程碑管理**：标记关键节点和成就
- **风险跟踪**：记录潜在风险和缓解措施

### 高级功能

- **集成接口**：与其他研究技能的无缝集成
- **自动生成**：基于研究方法论的模板生成
- **进度预测**：基于历史数据的完成时间预测
- **报告生成**：汇总项目状态和成果

## 详细指令

### 第一阶段：工作空间初始化
- 创建基础目录结构
- 生成三个核心文件（task_plan.md, progress.md, findings.md）
- 设置初始研究参数和目标

### 第二阶段：任务规划
- 定义研究主题和方法论
- 制定阶段性任务和里程碑
- 估算时间和资源需求
- 识别潜在风险和缓解策略

### 第三阶段：进度跟踪
- 定期更新任务完成状态
- 记录时间投入和资源消耗
- 跟踪里程碑达成情况
- 调整计划以应对变化

### 第四阶段：发现记录
- 文档化关键研究发现
- 记录理论洞察和模式识别
- 整理问题和假设
- 验证点的记录和跟踪

### 第五阶段：监控与调整
- 评估项目整体进度
- 识别瓶颈和延误因素
- 调整计划和资源分配
- 准备阶段性报告

### 第六阶段：集成与协作
- 与其他研究技能的协调
- 数据和文档的共享机制
- 团队协作的跟踪
- 成果整合和验证

## 参数

- `action`: 执行的操作 (initialize, update-task, log-progress, record-finding, get-status)
- `research_topic`: 研究主题
- `methodology`: 研究方法论 (grounded-theory, field-analysis, ant, etc.)
- `workspace_dir`: 工作空间目录
- `task_description`: 任务描述
- `time_spent`: 花费时间（小时）
- `finding`: 记录的发现
- `category`: 发现类别

## 示例

### 示例 1: 初始化扎根理论研究
User: "为'中国科技企业创新策略'扎根理论研究创建规划"
Response: 初始化工作空间，生成三文件结构，制定GT特化任务计划。

### 示例 2: 更新进度
User: "记录今天完成了开放编码的前两轮"
Response: 更新进度文件，标记相关任务完成，记录时间投入。

### 示例 3: 记录发现
User: "记录在访谈中发现的'面子文化'影响因素"
Response: 在发现记录文件中添加新条目，分类为理论洞察。

## 质量标准

- 遵循系统性规划原则
- 保持文档间的逻辑一致性
- 确保进度跟踪的实时性
- 提供有意义的状态指标
- 支持研究方法论的特定需求

## 输出格式

```json
{
  "summary": {
    "action_performed": "initialize",
    "workspace_location": "./planning_workspace",
    "files_created": 3,
    "completion_percentage": 0
  },
  "details": {
    "task_plan": {
      "file_path": "task_plan.md",
      "tasks_total": 24,
      "tasks_completed": 0
    },
    "progress_tracker": {
      "file_path": "progress.md",
      "milestones": ["Phase 1: Literature Review"]
    },
    "findings_log": {
      "file_path": "findings.md",
      "entries_count": 0
    }
  },
  "metadata": {
    "timestamp": "2026-01-23T10:30:00",
    "version": "1.0.0"
  }
}
```

## 资源

- Planning with Files 方法论文献
- 项目管理最佳实践
- 研究方法论规划指南
- 文件驱动工作流示例

## 完成标志

完成 Planning with Files 集成应包括：

1. 成功创建规划工作空间
2. 生成三个核心文档
3. 正确初始化研究参数
4. 建立有效的跟踪机制
5. 与其他技能的集成接口

---

*此技能为研究项目提供结构化的规划和跟踪框架，确保研究过程的系统性和可追溯性。*