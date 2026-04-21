---
name: Boss Resume Analyzer
description: Analyzes candidate resumes from recruitment emails, downloads PDF attachments, extracts text, matches against job requirements, and produces concise hiring reports.
---

# BOSS直聘简历分析技能

从企业邮箱中自动读取BOSS直聘转发的简历邮件，下载PDF附件，提取文本，对照岗位需求进行候选人筛选，输出精简的招聘建议报告。

## 依赖

- **imap-smtp-email 技能**：用于连接邮箱、搜索邮件、下载附件
  - 技能路径：`/agent/.agents/skills/imap-smtp-email/`
  - 配置文件：`/agent/.agents/skills/imap-smtp-email/.env`
  - IMAP命令：`node scripts/imap.js <command>`
- **pdftotext**：用于从PDF中提取文本（系统已预装）
- **岗位需求文档**：`/agent/hiring/job_requirements.md`

## 工作流程

### Step 1：获取新简历邮件

在邮箱中搜索BOSS直聘简历邮件。

**⚠️ 重要：2026-04-08起，BOSS直聘已改为单封单份简历直推到INBOX**
- 新格式：每个候选人一封邮件，主题格式「候选人名 | X年，应聘 岗位名 | 深圳XX-XXK【BOSS直聘】」，1个PDF附件
- 旧格式（已废弃）：HR批量转发到Sent Messages，一封邮件含多个PDF

```bash
cd /agent/.agents/skills/imap-smtp-email

# 优先检查 INBOX（新简历直推到这里）
node scripts/imap.js check --limit 20 --mailbox INBOX

# 也检查 Sent Messages 和专用文件夹（旧格式兼容）
node scripts/imap.js check --limit 10 --mailbox "Sent Messages"
node scripts/imap.js check --limit 10 --mailbox "其他文件夹/BOSS直聘简历"
```

筛选方法：主题包含「BOSS直聘」或「应聘」，且attachments数组非空（含.pdf附件）。

**重要**：记录已处理过的邮件UID到 `/agent/hiring/processed_uids.json`，避免重复分析。

### Step 2：下载简历PDF

```bash
node scripts/imap.js download <uid> --mailbox "<mailbox>" --dir /agent/hiring/resumes/
```

### Step 3：提取简历文本

```bash
pdftotext "/agent/hiring/resumes/<filename>.pdf" - 2>/dev/null
```

注意：BOSS直聘的PDF简历通常包含大量水印噪声（1-4个字符的随机字符串行）。提取后需过滤：
- 移除仅包含1-4个字母数字字符的行
- 移除看起来像水印的长hash字符串行
- 保留有实际内容的行

### Step 4：读取岗位需求

读取 `/agent/hiring/job_requirements.md` 获取当前在招岗位的：
- 必备技能清单
- 加分项
- 评分权重
- 红旗/黄旗/绿旗标准

### Step 5：逐份分析并生成报告

对每份简历进行评估，关注以下维度：
1. **学历**：学校层次、专业相关度
2. **工作经验**：年限、行业匹配度、技术栈匹配度
3. **核心技能**：与岗位必备技能的重叠度
4. **项目亮点**：有无与AI Agent/MCP/OT等核心方向相关的实战项目
5. **风险因素**：跳槽频率、行业跨度、期望薪资是否超出范围

### Step 6：输出报告

报告格式分两部分，要求简洁有力，不要写成论文：

#### 第一部分：推荐人选（最合适的候选人）

对于每一位推荐面试的候选人，输出：

```
## ⭐ [候选人姓名] — 投递岗位：xxx

**为什么推荐：**
- 闪光点1（一句话说清楚）
- 闪光点2
- 闪光点3

**面试关注点：**
需要验证的地方，用1-2句话说明

**建议提问（3题）：**
1. [具体的深度面试问题，不要泛泛而谈]
2. [紧扣候选人简历中的项目/经历来提问]  
3. [考察与岗位核心要求的匹配度]
```

#### 第二部分：其他候选人速览

```
## 📋 其他候选人（共X人）

| 姓名 | 投递岗位 | 结论 | 一句话原因 |
|------|---------|------|-----------|
| xxx  | xxx     | ❌不匹配 | 无AI经验，纯传统前端 |
| xxx  | xxx     | 🔶待定  | 有潜力但经验不足，可留意 |
```

保持简洁。不匹配的人一句话说清原因即可，不要展开。

## 文件路径约定

| 文件 | 路径 |
|------|------|
| 岗位需求 | `/agent/hiring/job_requirements.md` |
| 简历PDF | `/agent/hiring/resumes/` |
| 已处理UID | `/agent/hiring/processed_uids.json` |
| 分析报告 | `/agent/hiring/reports/YYYY-MM-DD.md` |

## Step 7：推送到企业微信群

分析报告完成后，通过企业微信群机器人 Webhook 推送到指定群聊。

### 配置

- Webhook配置文件：`/agent/hiring/.wecom_webhook`
- 推送脚本：`/agent/hiring/wecom_bot.sh`

### 推送内容

1. **Markdown摘要**：推荐/待定/不匹配人数 + Top候选人亮点（企微markdown限4096字节）
2. **完整报告文件**：上传当日分析报告MD文件
3. **推荐候选人简历原件**：上传推荐面试候选人的PDF简历

### API说明

```bash
# 发送Markdown消息
curl "$WEBHOOK_URL" -H 'Content-Type: application/json' -d '{"msgtype":"markdown","markdown":{"content":"..."}}'  

# 上传文件获取media_id
curl -X POST "$UPLOAD_URL" -F "media=@file.pdf;filename=file.pdf"

# 发送文件消息
curl "$WEBHOOK_URL" -H 'Content-Type: application/json' -d '{"msgtype":"file","file":{"media_id":"..."}}'  
```

### 限制

- 消息频率：20条/分钟（每次发送间隔至少2秒）
- markdown内容最大4096字节
- 文件大小5B~20MB
- media_id有效期3天
- 企微webhook markdown不支持表格（非v2），用引用/列表代替

### 执行

```bash
bash /agent/hiring/wecom_bot.sh /agent/hiring/reports/YYYY-MM-DD.md /agent/hiring/resumes/
```

## 注意事项

- BOSS直聘简历PDF有水印，提取文本时需要过滤噪声
- IMAP中文SUBJECT搜索不可靠，优先用attachment数量和发件人来筛选
- 有些简历是纯图片PDF（如王旭的简历），pdftotext无法提取，需标记为"无法解析"
- 一封邮件可能包含多份简历（如25份打包在一封邮件中）
- 记得更新 `processed_uids.json` 避免重复处理
- 报告生成后自动推送企微群（Step 7），推荐候选人简历附件一并发送
