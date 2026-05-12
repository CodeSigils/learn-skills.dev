---
name: lesson-quiz
version: 1.0.0
description: Claude Code 单模块互动测验。Use when asked to "quiz me on hooks", "test my knowledge of lesson 3", "lesson quiz", "practice quiz for MCP", "do I understand skills", or similar Chinese requests.
---

# 课程测验（Lesson Quiz）

这是一个针对单个 Claude Code lesson 的完整互动测验 skill，用于检查用户对某一课的理解程度。

## 使用说明

### Step 1: 确认 lesson

如果用户提供了参数，就映射到 lesson 目录：

- `01` / `slash-commands` / `commands` → `01-slash-commands`
- `02` / `memory` → `02-memory`
- `03` / `skills` → `03-skills`
- `04` / `subagents` / `agents` → `04-subagents`
- `05` / `mcp` → `05-mcp`
- `06` / `hooks` → `06-hooks`
- `07` / `plugins` → `07-plugins`
- `08` / `checkpoints` → `08-checkpoints`
- `09` / `advanced-features` / `advanced` → `09-advanced-features`
- `10` / `cli` → `10-cli`

如果用户没提供参数，使用 AskUserQuestion 分 2-3 轮让用户选择 lesson。

---

### Step 2: 读取 lesson 与题库

先读取：

- `<lesson-directory>/README.md`
- `references/question-bank.md`

优先使用题库中该 lesson 的预置题。  
如果题库不足 8 题，可根据 lesson README 补充生成，但必须保持与 lesson 内容一致。

---

### Step 3: 询问测验时机

用 AskUserQuestion 询问用户当前是在：

1. `Before (pre-test)`
2. `During (progress check)`
3. `After (mastery check)`

不同 timing 会影响结果解读。

---

### Step 4: 出题

- 每次固定 8 题
- 每轮 2 题，共 4 轮
- 混合概念题和实践题
- 每题使用 AskUserQuestion，提供 3-4 个选项
- 每轮用户答完后，立即给出本轮逐题反馈：是否答对；如果答错，给出正确答案和简短解释
- 每题展示前必须随机打乱选项顺序，不要照搬题库里的 A/B/C/D 顺序，也不要固定把正确答案放在第一项
- 打乱后要记录正确答案对应的新位置，最终评分按打乱后的真实答案判定

每题必须包含这些信息：

- `category`
- `question`
- `options`
- `correct`
- `explanation`
- `review`

记录用户答案；每轮反馈不替代最终结果，所有 4 轮结束后仍要统一评分。

---

### Step 5: 评分与结果输出

每题答对记 1 分，总分 8 分。

等级：

- 8：Mastered
- 6-7：Proficient
- 4-5：Developing
- 2-3：Beginning
- 0-1：Not yet

输出格式必须包含：

```markdown
## 课程测验结果：[课程名称]

**得分：N/8** — [等级]
**测验时机**: [学习前 / 学习中 / 学习后]
**答题拆分**: 概念题正确 N 道，实践题正确 N 道

### 单题结果
| # | 类型 | 问题摘要 | 你的回答 | 结果 |

### 错题复盘
**Q[N]: [问题]**
- 你的回答:
- 正确答案:
- 解释:
- 复习建议:

### 按测验时机给出的反馈
[根据 pre-test / progress check / mastery check 给不同反馈]

### 推荐下一步
- [继续下一课 / 回看哪一节 / 重测 / 深入解释]
```

---

### Step 6: 根据 timing 解释结果

#### 如果是学前测验

- 把成绩解释为“学习前基线”
- 强调用户接下来应重点关注哪些主题

#### 如果是学习中检查

- 把成绩解释为“阶段性进度检查”
- 明确哪些点已经掌握、哪些点要补

#### 如果是学后测验

- 把成绩解释为“lesson mastery check（课程掌握度检查）”
- 如果分数高，建议进入下一课
- 如果分数一般，列出明确回看点

---

### Step 7: 提供后续动作

最后再用 AskUserQuestion 让用户选择：

1. `Retake this quiz`
2. `Quiz another lesson`
3. `Explain a topic I missed`
4. `Done`

如果选第三项，先问错题编号，再读取该 lesson README 的相关部分，用中文解释并给例子。

## 输出要求

- 中文表达清晰
- 保留关键英文术语
- 错题解释必须具体
- 复习建议要明确到 lesson 或章节
- 不要把测验做成泛泛聊天
