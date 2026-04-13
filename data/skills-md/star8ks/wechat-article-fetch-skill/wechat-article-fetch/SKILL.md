---
name: wechat-article-fetch
description: >
  Fetches WeChat public account articles (微信公众号文章) from mp.weixin.qq.com URLs and extracts
  title, author, account name, publish date, and full article body as clean markdown.
  Use this skill whenever the user pastes a mp.weixin.qq.com link and wants to read, summarize,
  translate, analyze, or extract information from a WeChat article — even if they don't
  explicitly ask for "fetching" or "scraping". Also use it when integrating WeChat article
  content into CMS systems, documents, or databases.
---

# 微信公众号文章抓取

## 快速使用

```bash
# Markdown 输出
python3 $CLAUDE_SKILL_DIR/scripts/fetch.py "<文章链接>"

# JSON 输出（无外部依赖）
python3 $CLAUDE_SKILL_DIR/scripts/fetch.py "<文章链接>" --json
```

没有 Python 时，用 curl + Python3 one-liner（macOS 内置）：

```bash
curl -s \
  -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" \
  "<文章链接>" | \
  python3 -c "
import sys, re, html
page = sys.stdin.read()
m = re.search(r'id=\"js_content\"[^>]*>(.*?)</div>\\s*<div', page, re.S)
if m:
    text = re.sub(r'<[^>]+>', '', m.group(1))
    print(re.sub(r'\\n{3,}', '\\n\\n', html.unescape(text)).strip())
"
```

Markdown 输出依赖 `html2markdown`（`brew install html2markdown`），未安装时自动降级为纯文本。

---

## 常见失败原因

**普通 fetch 工具直接请求会返回 302**，因为默认 UA 被识别为爬虫，脚本已内置桌面 Chrome UA 解决这个问题。

**返回 200 但内容是验证拦截页**（「当前环境异常，完成验证后即可继续访问」）才是更常见的坑。脚本会检测并报错。解决方法：

1. **换 IP** — 云服务器/VPN 出口 IP 经常被封，切换到家庭宽带或手机热点
2. **等几分钟重试** — 频率限制是临时的
3. **用 `agent-browser` skill** — 真实浏览器能直接绕过验证，也是查看图片/排版等视觉内容的唯一方式

---

## 已知限制

- 图片链接可访问但可能随时间失效
- 视频嵌入无法提取
- 需关注才能阅读的文章正文会为空
