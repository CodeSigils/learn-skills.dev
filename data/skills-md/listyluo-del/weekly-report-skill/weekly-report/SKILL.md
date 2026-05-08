---
name: weekly-report
version: 1.0.0
description: |
  AI 私人秘书：工作周报管理。支持创建周报、追加工作事项、查看进度、生成摘要并推送到飞书。
  当用户提到「周报」「工作进展」「本周做了什么」「帮我记录」「推送进度」「weekly report」时使用。
  子命令：setup（初始化配置）、new（新建本周周报）、add（追加事项）、status（查看进度）、push（推送摘要）。
argument-hint: "<setup|new|add|status|push> [内容]"
metadata:
  requires:
    bins: ["lark-cli"]
  author: listy
---

# weekly-report — AI 私人秘书周报管理

## 前置条件

- lark-cli 已安装并完成飞书授权
- 首次使用需运行 `/weekly-report setup` 完成配置

## 配置文件

配置存储在 `~/.claude/weekly-report-config.json`，结构如下：

```json
{
  "folder_token": "飞书云盘文件夹 token",
  "folder_name": "工作进展",
  "user_id": "ou_xxxx（用于接收推送的 open_id）",
  "push_chat_id": "oc_xxxx（可选，推送到群）",
  "naming_format": "YYYY-W{week} 工作进展 (MM.DD-MM.DD)",
  "dimensions": ["组织优化", "产品建设", "运营能力", "管理能力", "个人学习"],
  "current_doc_token": "当前周报文档 token"
}
```

## 命令路由

根据用户输入的子命令或意图，执行对应操作：

| 子命令 / 意图 | 操作 |
|--------------|------|
| `setup` | 初始化配置（引导用户设置文件夹、维度、推送对象） |
| `new` | 新建本周周报文档 |
| `add <内容>` | 将内容归类到对应维度并追加到当周文档 |
| `status` | 读取当周周报，汇报各维度进度 |
| `push` | 读取周报 → 生成摘要 → 推送到飞书（个人或群） |
| 无子命令 | 显示帮助信息 |

## 执行流程

### setup — 初始化配置

1. 检查 `~/.claude/weekly-report-config.json` 是否存在
2. 如不存在，引导用户完成以下配置：
   - 飞书云盘文件夹：询问是否新建还是指定已有文件夹
   - 周报维度：提供默认模板（组织优化/产品建设/运营能力/管理能力/个人学习），允许自定义
   - 推送对象：询问推送给自己（需 open_id）还是推送到群（需 chat_id）
3. 写入配置文件

**创建文件夹命令：**
```bash
lark-cli drive +create-folder --name "{文件夹名}"
```

### new — 新建本周周报

1. 读取配置文件
2. 计算当前 ISO 周数和日期范围（周一到周日）
3. 按配置的维度生成 markdown 模板
4. 创建飞书文档：
```bash
lark-cli docs +create --title "{标题}" --folder-token "{folder_token}" --markdown @{临时文件}
```
5. 更新配置文件中的 `current_doc_token`
6. 返回文档链接

**命名格式示例：** `2026-W19 工作进展 (05.05-05.11)`

### add — 追加工作事项

1. 读取配置文件，获取 `current_doc_token`
2. 分析用户输入的内容，判断归属哪个维度
3. 用 replace_range 模式更新对应章节：
```bash
lark-cli docs +fetch --doc "{doc_token}" --scope keyword --keyword "{维度标题}"
lark-cli docs +update --doc "{doc_token}" --mode replace_range --selection-by-title "## {维度}" --markdown "{更新后内容}"
```

**归类逻辑：**
- 涉及组织架构、团队合并、人员调动 → 组织优化
- 涉及产品方案、项目进度、技术建设 → 产品建设
- 涉及流程、SOP、协作、运营质量 → 运营能力
- 涉及干部管理、招聘、培训、考核 → 管理能力
- 涉及个人学习、考试、技能提升 → 个人学习
- 不确定时 → 询问用户

### status — 查看当前进度

1. 读取配置文件，获取 `current_doc_token`
2. 拉取文档内容：
```bash
lark-cli docs +fetch --doc "{doc_token}" --jq ".data.markdown"
```
3. 按维度整理进度，标注状态（✅ 已完成 / ⏳ 进行中）
4. 列出本周重点待推进事项
5. 以简洁格式输出给用户

### push — 生成摘要并推送

1. 执行 `status` 流程获取进度
2. 生成结构化摘要（markdown 格式）
3. 推送到飞书：

**推送给个人：**
```bash
lark-cli im +messages-send --as bot --user-id "{user_id}" --markdown "{摘要内容}"
```

**推送到群：**
```bash
lark-cli im +messages-send --as bot --chat-id "{push_chat_id}" --markdown "{摘要内容}"
```

4. 消息末尾附上文档链接

**摘要格式模板：**
```markdown
📋 **W{周数} 工作进展 ({日期范围})**

**{维度1}**
• 事项1 ✅
• 事项2 ⏳

**{维度2}**
• ...

---
⏰ 本周重点推进：xxx | xxx
📄 [完整周报文档]({doc_url})
```

## 注意事项

- bot 身份发送消息需要 bot 已加入目标群
- 文档创建使用 `--markdown @文件` 方式，需先写入临时文件再引用（相对路径）
- 每周一执行 `new` 时，自动归档上周文档（更新 current_doc_token）
- 如果 `current_doc_token` 为空或文档不存在，提示用户先执行 `new`
