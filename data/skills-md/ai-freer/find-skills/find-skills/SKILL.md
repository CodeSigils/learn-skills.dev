---
name: find-skills
description: |
  搜索和安装外部 Skills 的统一入口。双源并行搜索：skills.sh（主源，大生态）+ ClawHub（补充源，OpenClaw 定制）。
  当以下情况时使用：
  (1) 用户要求搜索、查找、发现新的 skill
  (2) 用户要求安装外部 skill
  (3) 当前已有 skill 无法满足需求，需要扩展能力
  (4) 用户提到 "find skill"、"搜 skill"、"有没有 xxx 的 skill"
---

# Find Skills — 双源并行搜索

## 搜索策略

**并行搜索，合并结果。** 不是 fallback，是同时查两个源。

### 源 1：skills.sh（主源）

大生态，跨 IDE/agent 通用，下载量即质量信号。

```bash
# 搜索
npx -y skills find "<query>"

# 安装（全局，所有 agent）
npx -y skills add <owner/repo@skill> --global --all

# 查看已安装
npx -y skills ls
```

安装路径：`~/.openclaw/workspace-lisa/skills/` 或全局 `~/.openclaw/skills/`

### 源 2：ClawHub（补充源）

OpenClaw 社区定制 skill，与 gateway/channel/plugin 深度集成。

```bash
# 搜索
clawhub search "<query>"

# 安装
clawhub install <skill-name>

# 查看已安装
clawhub list
```

## 执行流程

1. 收到搜索请求后，**同时**执行 `npx -y skills find` 和 `clawhub search`
2. 合并结果，按相关性 + 下载量排序呈现
3. 如果某个源报错（rate limit 等），用另一个源的结果兜底
4. 安装前检查是否已有同名/同功能 skill 避免重复

## 安装后

- 确认 SKILL.md 存在且 description 合理
- 运行 `npx -y skills ls` 确认已注册
- 如有安全顾虑，检查 skill 内容后再启用

## 注意

- skills.sh 的 `find` 命令是交互式的，用 pipe 或重定向处理
- ClawHub 有 rate limit，遇到限流直接跳过，不阻塞流程
- 两个源的 skill 格式兼容，都是 SKILL.md + 可选资源的标准结构
