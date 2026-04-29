---
name: wechat-article-downloader
description: "This skill should be used when the user wants to batch-download articles from a WeChat Official Account and save them as Word (.docx) files with embedded images. Trigger phrases include: 下载公众号文章, 抓取公众号, 保存微信公众号文章, 批量下载公众号, or any request that specifies an account name, a date range, and a local save path for WeChat articles."
---

# 微信公众号文章批量下载 Skill（Word版）

## 概述

本 Skill 支持按指定时间段批量下载微信公众号正文，**输出为 Word 文件（.docx）**，文章中的图片会自动下载并嵌入文档。文件名格式：`YYYY-MM-DD-文章标题.docx`，保存到用户指定的本地目录。**不抓取留言/评论**。

---

## 执行前必做：参数校验

**在执行任何下载操作之前，必须先确认用户已提供以下三个参数，缺一不可：**

| 参数 | 说明 | 示例 |
|------|------|------|
| `公众号名称` | 微信公众号的完整名称 | 饕餮海投资 |
| `文章发布时间段` | 起始日期 ~ 结束日期（YYYY-MM-DD） | 2026-04-01 ~ 2026-04-30 |
| `文件保存路径` | 本地绝对路径 | D:\AI\claw\饕餮海投资 |

如果用户只提供了部分信息，**停止执行，直接提示用户补充缺失的参数**，示例：

> "请补充以下信息后再继续：
> - ❌ 缺少文章发布时间段（请提供起止日期，如 2026-01-01 ~ 2026-04-30）
> - ❌ 缺少文件保存路径（如 D:\output\articles）"

三个参数都确认后，再进入下载流程。

---

## 依赖安装

首次使用前检查并安装依赖：

```bash
pip install requests beautifulsoup4 lxml playwright python-docx
playwright install chromium
```

**关键依赖说明：**
- `python-docx`：生成 Word 文档并嵌入图片
- `playwright`：使用无头浏览器访问微信原文，提取完整 HTML（含图片）
- `requests`：下载微信 CDN 图片（需携带 Referer 头）

---

## 核心脚本

脚本位置：`scripts/download_articles.py`

**基本用法：**

```bash
python scripts/download_articles.py \
  --account "公众号名称" \
  --start   "YYYY-MM-DD" \
  --end     "YYYY-MM-DD" \
  --output  "D:/保存路径"
```

**参数说明：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--account` | ✅ | 公众号名称 |
| `--start` | ✅ | 起始日期（含），格式 YYYY-MM-DD |
| `--end` | ✅ | 结束日期（含），格式 YYYY-MM-DD |
| `--output` | ✅ | 本地保存目录（不存在则自动创建） |
| `--source` | ❌ | 文章列表来源，`sogou`（默认）或 `jintiankansha` |

---

## 执行流程

1. **校验参数** — 确认三个必填参数完整且合法（日期格式、路径可写）
2. **获取文章列表**
   - 默认来源：搜狗微信搜索（`--source sogou`），逐页翻页，遇到早于起始日期则停止
   - 备用来源：jintiankansha.me（需 JS 渲染，适合需要更完整历史文章的场景）
3. **逐篇访问** — 使用 Playwright（headless Chromium）访问微信原文，提取：
   - 发布日期（从 `oriCreateTime` 变量或 `#publish_time` 元素）
   - 正文 HTML（从 `#js_content` 元素），**包括所有图片的 `data-src` 属性**
4. **下载图片** — 将微信 CDN 图片（`mmbiz.qpic.cn` 等）下载到 `{保存目录}/_images/` 子目录
5. **时间过滤** — 只保存在 `[start, end]` 范围内的文章，不符合的跳过，不创建文件
6. **生成 Word 文件** — 文件名 `YYYY-MM-DD-文章标题.docx`，内容结构：
   - 标题（Heading 1，宋体 22pt）
   - 元信息（公众号、发布日期、原文链接）
   - 完整正文（含嵌入图片，居中显示，宽度自适应）
   - **字体统一使用宋体 10.5pt，行距 1.5 倍**
   - **样式保留**：加粗（`<strong>`/`<b>`/`font-weight:bold`）、斜体（`<em>`/`<i>`）、字体颜色（CSS `color` 属性）、下划线、字号等均需保留
   - **超链接保留**：原文中的 `<a>` 标签必须生成为 Word 可点击的超链接（蓝色带下划线），链接文字保留原有样式（如加粗、颜色等）
7. **生成日志** — 下载目录下自动生成 `_下载日志.txt`，记录每篇文章状态

---

## 图片处理机制

微信文章的图片存放在 `data-src` 属性中（延迟加载），脚本的处理方式：

1. **在 Playwright 中执行 JS**：将所有 `<img>` 的 `data-src` 复制到 `src`，同时过滤掉 `data:image/*` 占位符（移除无真实图片URL的img标签）
2. **下载真实图片**：使用 `requests` 下载，携带 `Referer: https://mp.weixin.qq.com/` 头
3. **格式兼容**：自动检测图片真实格式（GIF/WEBP等），对 python-docx 不兼容的格式自动转为 PNG
4. **嵌入 Word**：通过 `python-docx` 的 `run.add_picture()` 将图片居中插入段落，宽度自适应（5英寸）
5. **去重机制**：根据 URL 的 MD5 哈希生成文件名，避免重复下载
6. **图片目录**：图片保存在 `{保存目录}/_images/` 子目录下，请勿手动删除（Word 文件引用了本地图片路径）

---

## 注意事项

- **留言/评论**：微信评论只在客户端内可见，外部无法可靠获取。**本 Skill 不抓取留言，也不在文件中生成留言区块。**
- **图片格式**：支持 jpg/png/gif/webp/svg 等常见格式；小于 100 字节的图片会被跳过（通常是占位符）
- **反爬限制**：搜狗/微信对频繁访问有速率限制，脚本内置随机延时（1.5~3.5 秒/篇），如遇到验证码请手动处理后重试
- **文章数量多时**：建议改用 `--source jintiankansha` 以获取更完整的历史文章列表
- **文件名冲突**：同一天多篇同名文章，后下载的会覆盖，建议检查日志
- **付费文章**：微信付费文章只展示开头部分，脚本会正常下载但内容不完整（属正常行为）

---

## 完成后

下载完成后，向用户汇报：
- 成功下载篇数
- 跳过篇数（含原因：超出时间段 / 无法获取日期 / 正文为空）
- 失败篇数
- 保存目录路径
- 图片目录路径
- 日志文件路径
