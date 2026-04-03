---
name: writing-skills
description: Skill 编写指南，创建新 skill 时遵守此规范
---

# Skill 编写指南

## 目录结构

```
skills/
  <skill-name>/
    SKILL.md       ← 必须，skill 入口文件
```

## 命名规范

- 文件夹名：小写字母 + 连字符，例如 `code-review`、`task-breakdown`
- `name` 字段：必须和文件夹名一致
- 风格：用名词或动词短语，简洁明确

## SKILL.md 格式

```markdown
---
name: <skill-name>
description: <一句话说明用途和触发时机>
---

# <标题>

## 依赖规范
#[[file:../rules/<规则文件>.md]]
#[[file:../<其他skill>/SKILL.md]]

## 目的
<一句话说明目标>

## 输入
- <输入项>

## 步骤

> 每个步骤先输出标题，再输出结果

- <步骤 1>
- <步骤 2>

## 输出
- <输出项>

## Review 检查清单
- <检查项>
```

## 编写规则

- description：说清楚"什么时候用"，Kiro 靠它决定是否激活 skill
- 依赖规范：列出所有引用的 rules 和其他 skill，确保单独使用时能加载完整上下文
- 步骤：加上"每个步骤先输出标题，再输出结果"，防止 AI 跳步
- 引用一致：文字里提到的规范名称，必须在依赖规范里有对应的 `#[[file:]]`
- 写入文档：如果步骤涉及写文档，加上"路径遵守 `project-structure` 文档存放规范"
- 阶段结束：如果是流程阶段 skill，末尾加"下一阶段"和 stage-gate 引用

## 规则文件

通用规则放在 `skills/rules/` 目录，不是独立 skill，被其他 skill 通过 `#[[file:]]` 引用：

```
skills/rules/
  <rule-name>.md
```

规则文件同样需要 frontmatter（name + description），但不需要步骤和输出。
