# [learn-skills.dev](https://www.learn-skills.dev)

精选高质量 AI Agent Skills。搜索、安装、复制与分享。  
兼容 Claude Code、Cursor、OpenClaw 及其他 AI 编程工具。

**Web 应用：** [https://www.learn-skills.dev](https://www.learn-skills.dev) — 搜索、安装、复制与分享 AI Agent Skills。

**语言：** [English](README.md) · [简体中文](README.zh.md) · [繁體中文](README.tw.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md)

## 数据来源

### 当前提供方

- **[skills.sh](https://skills.sh)** — 社区精选技能排行榜
  - All Time (`/`) — 总安装量排名
  - Trending (`/trending`) — 近期增长排名
  - Hot (`/hot`) — 日安装量排名

### 计划中的提供方

- **GitHub Trending** — GitHub 上热门的技能仓库
- **Awesome Lists** — 精选的 awesome-* AI agent skills 列表

### 手动技能

未被任何提供方收录的技能可通过 `data/manual_skills.json` 手动添加：

```json
{
  "skills": [
    {
      "source": "owner/repo",
      "skillId": "skill-name",
      "name": "Skill Display Name",
      "installs": 1
    }
  ]
}
```

手动技能将：

- 从 GitHub 拉取 `SKILL.md`（使用标准技能文件夹检测）
- 以 `providerId: "manual"` 写入 `skills_index.json`
- **不会**被爬虫覆盖（多次运行后仍保留）
- **会去重**：若 skills.sh 之后收录了同一条手动技能，则优先使用 skills.sh 的数据

注意：`installs` 至少为 1（最小值）。

## 输出文件

爬虫在 `data/` 目录生成以下文件：

### `data/skills.json`

包含三个排行榜的完整技能数据：

```json
{
  "updatedAt": "2024-01-27T00:00:00.000Z",
  "allTime": [...],
  "trending": [...],
  "hot": [...]
}
```

### `data/skills_index.json`

面向网站的**全部**技能索引（由 `data/skills.json` 构建）：

- 当 `data/skills-md/` 下存在缓存的 `SKILL.md` 时，`description` 为指向 `description_en.txt` 的**路径**
- 包含 `skillMdPath`，便于网站拉取并渲染完整 Markdown
- 按 `id`（`<source>/<skillId>`）**去重**。若上游有重复，索引保留 `installsAllTime` 最大的一条

### `data/feed.json`

简化订阅格式（每个榜单前 50 条）。

会尝试通过拉取对应 GitHub `SKILL.md`（缓存在 `data/skills-md/`）为每条补充 `description`：

```json
{
  "title": "Skills Feed",
  "description": "Aggregated AI agent skills from multiple sources",
  "link": "https://github.com/user/skills_feed",
  "updatedAt": "2024-01-27T00:00:00.000Z",
  "topAllTime": [...],
  "topTrending": [...],
  "topHot": [...]
}
```

### `data/skills-md/`

从 GitHub 缓存的 `SKILL.md`，常见路径包括：

- `skills/<skillId>/SKILL.md`（最常见）
- `.claude/skills/<skillId>/SKILL.md`
- `.cursor/skills/<skillId>/SKILL.md`
- `.codex/skills/<skillId>/SKILL.md`
- `plugins/<plugin-name>/skills/<skillId>/SKILL.md`（插件式仓库常见，如 Expo）

存在 `SKILL.md` 时，爬虫还会生成：

- `description_en.txt`（从 SKILL.md  frontmatter 的 `description` 提取，若有）

默认只为榜单内技能拉取 `SKILL.md`，以保证每日任务速度。

若需同步 `data/skills.json` 中的**全部**技能，可执行：

```bash
SYNC_ALL_SKILL_MDS=1 bun run crawl
```

### `data/feed.xml`

RSS 2.0（XML），供 RSS 阅读器/订阅使用。

- 由当前爬取结果 + 上一份 `data/feed.json` 生成
- 仅在有实质变化（新条目/排名跃升）时发布，避免刷屏

## 使用方式

### 本地开发

```bash
# 安装依赖
bun install

# 运行爬虫
bun run crawl
```

提示：若希望更完整地覆盖 GitHub 上的 `SKILL.md`（含 `plugins/*/skills/...` 等插件路径），  
请设置 `GITHUB_TOKEN` 以降低 API 限流影响：

```bash
export GITHUB_TOKEN=ghp_xxx
bun run crawl
```

### GitHub Actions

推送到 GitHub 后，爬虫将：

1. 每日 UTC 0:00 自动运行
2. 支持手动触发（在 Actions 中点击 “Run workflow”）
3. 在推送到 main 分支时自动运行

## 在网站中使用

可通过 GitHub Raw URL 直接拉取数据：

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/skills.json
```

或使用 jsDelivr CDN（通常更快）：

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/skills.json
```

### RSS 订阅（推荐）

订阅 RSS：

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/feed.xml
```

或通过 jsDelivr：

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/feed.xml
```

### 示例代码

```typescript
// Next.js 中
const SKILLS_DATA_URL = 'https://cdn.jsdelivr.net/gh/your-username/skills-crawler@main/data/skills.json';

export async function getSkillsData() {
  const res = await fetch(SKILLS_DATA_URL, {
    next: { revalidate: 3600 } // 每小时重新验证
  });
  return res.json();
}
```

## 说明

- 数据每日更新
- 请遵守各提供方的服务条款
- 仅供个人学习与研究使用

## 贡献

想新增技能数据源？欢迎 PR！可参考仓库中现有 provider 实现。
