---
name: requirements-analysis
description: 需求分析与确认流程，明确需求边界，确保无歧义、无遗漏
---

# 需求分析与确认

## 依赖规范
#[[file:../rules/review-base.md]]
#[[file:../rules/git-workflow.md]]
#[[file:../rules/project-structure.md]]

## 目的
明确需求边界，确保无歧义、无遗漏，为设计提供可靠输入。

## 输入
- 原始描述：需求方提供的文字、原型、口述，或对话上下文

## 步骤

> 每个步骤先输出标题，再输出结果

- 需求整理：用 Given/When/Then 描述每条需求，检查漏洞、矛盾、缺少分支
- 需求确认：标记不明确或有风险的需求点，逐一与需求方确认
- 范围界定：明确 MVP 范围，排除本期不做的内容
- 写入文档：按输出要求写入文档（路径遵守 `project-structure` 文档存放规范）
- 执行 review：遵守 `review-base`，通过后才进入下一阶段
- 提交：review 通过后按 `git-workflow` 提交

## 输出
- 需求清单：每条含 Given/When/Then
- 范围边界：本期做什么、不做什么

## Review 检查清单

- Given/When/Then：每条需求完整，无逻辑漏洞
- 无矛盾：无矛盾或冲突的需求
- 边界覆盖：异常场景和边界情况已覆盖
- 范围清晰：MVP 范围边界清晰

## 阶段结束

下一阶段：`software-design`

#[[file:../rules/stage-gate.md]]
