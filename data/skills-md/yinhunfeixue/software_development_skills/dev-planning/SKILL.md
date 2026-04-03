---
name: dev-planning
description: 技术方案确认、开发规划、公共模块设计
---

# 开发规划和准备

## 依赖规范
#[[file:../rules/review-base.md]]
#[[file:../rules/git-workflow.md]]
#[[file:../rules/coding-standards.md]]
#[[file:../rules/ui-design.md]]
#[[file:../rules/project-structure.md]]
#[[file:../task-breakdown/SKILL.md]]

## 目的
对齐技术方案，完成任务拆解和公共模块设计，降低开发阶段不确定性。

## 输入
- 设计文档：模块划分方案和设计决策记录，或对话上下文

## 步骤

> 每个步骤先输出标题，再输出结果

- 技术对齐：
  - 收集倾向：询问开发者的技术倾向（语言、框架、已有约束等）
  - 给出建议：结合需求、设计和开发者输入，给出最佳实践建议并附理由
  - 确认方案：由开发者确认或调整，最终确定技术方案
- UI 设计（仅 web 项目）：技术方案确认后，若为 web 项目，询问开发者是否需要出设计图；如需要，遵守 `ui-design` 中的规范
- 任务拆解：按 `task-breakdown` skill 的步骤执行，输出任务清单和依赖关系表
- 项目框架：根据技术方案初始化项目，包含基础配置和依赖安装
- .gitignore：检查是否已有 `.gitignore`，若没有则根据技术栈生成
- 公共模块：识别公共模块，输出接口规范，确认后在本阶段优先开发；必须包含使用文档和统一演示入口页面
- 规范约定：约定 `coding-standards`，后续开发强制执行
- 环境变量：创建 `.env.example`，区分 dev/staging/prod，说明每个变量用途，敏感值不提交仓库
- 写入文档：按输出要求写入文档（路径遵守 `project-structure` 文档存放规范）
- 执行 review：遵守 `review-base`，通过后才进入下一步
- 提交：review 通过后按 `git-workflow` 提交

## 输出
- 技术方案：确认后的技术方案
- 任务清单：功能任务清单，已拆解到可独立开发和 review
- 公共模块：清单 + 接口规范 + 使用文档 + 演示入口页面

## Review 检查清单

- 技术方案：已确认
- 任务拆解：每个任务可独立开发和 review
- 公共模块：清单完整，接口规范已输出，有使用文档和演示入口页面
- 规范约定：`coding-standards` 已确认
- 环境变量：已区分 dev/staging/prod，不硬编码

## 阶段结束

下一阶段：`coding`

#[[file:../rules/stage-gate.md]]
