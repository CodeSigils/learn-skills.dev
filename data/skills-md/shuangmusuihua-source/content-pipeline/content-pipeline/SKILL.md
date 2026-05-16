---
name: content-pipeline
description: |
  内容处理流水线：翻译 → 去AI味 → 多平台排版。
  当用户提供英文网页链接或本地文本，需要翻译为中文并发布到微信公众号、今日头条等平台时使用。
  支持流程：获取内容 → 翻译 → 人性化处理 → 多平台格式化 → 预览。
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch
  - Skill
  - AskUserQuestion
metadata:
  trigger: 翻译英文内容并转换为多平台排版格式
  pipeline:
    - translate: 英文翻译为中文 Markdown
    - humanize: 去除 AI 写作痕迹
    - format: 多平台排版（微信/头条）
---

# Content Pipeline: 内容处理流水线

将英文内容转换为中文，优化表达，并输出为多平台排版格式。

## 支持的输入

- **网页链接** - 英文文章 URL
- **本地文件** - txt、md 等文本文件
- **直接粘贴** - 用户直接提供的英文文本

## 支持的输出平台

| 平台 | 代码 | 风格 |
|------|------|------|
| 微信公众号 | wechat | 暖色调、米色背景、印刷级排版 |
| 今日头条 | toutiao | 白底黑字、红色强调、现代简洁 |

---

## 工作流程

### 步骤 1：获取内容

根据输入类型选择方式：

- **URL** → 使用 WebFetch 工具获取网页内容
- **本地文件** → 使用 Read 工具读取文件
- **直接文本** → 直接使用

### 步骤 2：翻译

调用 `skills/translate.md` 进行翻译：

- 英文 → 中文
- 输出 Markdown 格式
- 保留原文结构（标题、列表、代码块等）
- 专业术语保留英文并加中文注释

**调用方式：**
```
Skill(skill: "content-pipeline:translate")
```

### 步骤 3：去除 AI 味

调用 `humanizer-zh` skill：

- 识别 AI 写作模式
- 重写问题片段
- 注入自然表达

### 步骤 4：选择平台

使用 AskUserQuestion 询问用户：

```
问题：请选择目标发布平台
选项：
- 微信公众号（暖色调、米色背景）
- 今日头条（白底黑字、红色强调）
- 两个都要
```

### 步骤 5：格式化输出

根据用户选择调用对应格式化 skill：

- 微信公众号 → `skills/wechat.md`
- 今日头条 → `skills/toutiao.md`
- 两个都要 → 分别生成两个 HTML 文件

### 步骤 6：预览

使用 `open` 命令打开生成的 HTML 文件：

```bash
open /path/to/output.html
```

### 步骤 7：发布指导

预览确认后，用户手动发布到对应平台：

**微信公众号：**
1. 登录 mp.weixin.qq.com
2. 进入素材管理 → 新建图文
3. 全选复制 HTML 内容 → 粘贴
4. 保存 / 发布

**今日头条：**
1. 登录 mp.toutiao.com
2. 发布文章 → 粘贴内容
3. 选择分类 → 发布

---

## 输出文件命名

- 微信公众号：`{article-name}-wechat.html`
- 今日头条：`{article-name}-toutiao.html`

---

## 快速使用示例

**示例 1：翻译网页**

```
用户：https://example.com/english-article
```

流程：获取网页 → 翻译 → 去AI味 → 询问平台 → 生成HTML → 预览

**示例 2：本地文件**

```
用户：翻译 ~/Documents/article.txt 并转成微信样式
```

流程：读取文件 → 翻译 → 去AI味 → 微信格式 → 预览

**示例 3：直接文本**

```
用户：把这段英文翻译成中文，发到今日头条：
[粘贴英文内容]
```

流程：翻译 → 去AI味 → 头条格式 → 预览

---

## 子 Skills

本 plugin 包含以下子 skills，可单独调用：

| Skill | 功能 | 调用方式 |
|-------|------|----------|
| translate | 英文翻译为中文 Markdown | Skill(skill: "content-pipeline:translate") |
| wechat | 微信公众号格式化 | Skill(skill: "content-pipeline:wechat") |
| toutiao | 今日头条格式化 | Skill(skill: "content-pipeline:toutiao") |

---

## 注意事项

1. **翻译质量** - 保持原文含义，专业术语双语标注
2. **AI 痕迹** - 翻译后的文本通常有明显 AI 味，必须调用 humanizer-zh
3. **平台兼容** - 微信需用 table 实现背景色，头条可直接用 div
4. **预览确认** - 生成后必须打开浏览器让用户确认效果
