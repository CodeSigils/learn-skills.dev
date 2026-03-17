---
name: commit
description: "Quick git commit with auto-generated or specified message. Use when user says /commit, wants to commit changes, or needs to create a git commit. Trigger command: /commit."
argument-hint: "[optional: commit message]"
disable-model-invocation: true
allowed-tools: Bash(git show:*)
model: haiku
---

# Commit — 快速 Git 提交

创建 git commit，支持指定 message 或自动生成。

## 当前仓库状态

```
!`git status`
```

## 暂存区 Diff

```
!`git diff --staged`
```

## Steps

1. 根据上方 `git status` 输出判断：
   - 若无 staged 改动 → 提示用户先 `git add`，**立即结束**
2. 根据上方 `git diff --staged` 输出生成 commit message（**纯推理，不调用任何命令**）：
   - 若提供了 `$ARGUMENTS` → 直接使用
   - 否则 → 分析 diff 生成符合 Conventional Commits 的 message
3. **必须调用 Bash 工具**执行：`git commit -m "<message>"`（禁止模拟输出）
4. **必须调用 Bash 工具**执行：`git show --stat --pretty=format:"✓ Committed: %s (%h)" -1`，将真实输出展示给用户

## Commit Message 格式

格式：`<type>[optional scope]: <description>`

常用 type：
- `feat` — 新功能（触发 minor 版本）
- `fix` — Bug 修复（触发 patch 版本）
- `docs` — 文档变更
- `style` — 代码格式（不影响逻辑）
- `refactor` — 重构（非 feat/fix）
- `perf` — 性能优化
- `test` — 测试相关
- `build` — 构建系统/依赖
- `ci` — CI 配置
- `chore` — 其他杂项
- `revert` — 回滚

规则：
- 简洁但有描述性，第一行不超过 72 字符
- scope 可选：`feat(auth): add OAuth2 login`
- 破坏性变更：type 后加 `!` 或 footer 写 `BREAKING CHANGE: <描述>`

示例：
- `feat: add user authentication with JWT`
- `fix(api): handle null response from upstream`
- `feat!: remove deprecated /v1/users endpoint`

## 输出

直接展示 Step 4 的 Bash 真实输出，不得手动拼接或模拟。
