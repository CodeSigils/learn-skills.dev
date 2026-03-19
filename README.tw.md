<div align="center">

<h1><a href="https://www.learn-skills.dev">learn-skills.dev</a></h1>

<p>精選高品質 AI Agent Skills。搜尋、安裝、複製與分享。<br>
適用於 Claude Code、Cursor、OpenClaw 及其他 AI 程式工具。</p>

<p><strong>Web 應用：</strong> <a href="https://www.learn-skills.dev">https://www.learn-skills.dev</a> — 搜尋、安裝、複製與分享 AI Agent Skills。</p>

<p>
<a href="./README.md">English</a> | <a href="./README.zh.md">简体中文</a> | 繁體中文 |
<a href="./README.ja.md">日本語</a> |
<a href="./README.ko.md">한국어</a> |
<a href="./README.fr.md">Français</a> |
<a href="./README.de.md">Deutsch</a> |
<a href="./README.es.md">Español</a> |
<a href="./README.it.md">Italiano</a> |
<a href="./README.ru.md">Русский</a> |
<a href="./README.ar.md">العربية</a>
</p>

</div>

## 資料來源

### 目前提供方

- **[skills.sh](https://skills.sh)** — 社群精選技能排行榜
  - All Time (`/`) — 總安裝量排名
  - Trending (`/trending`) — 近期成長排名
  - Hot (`/hot`) — 日安裝量排名

### 規劃中的提供方

- **GitHub Trending** — GitHub 上熱門的技能儲存庫
- **Awesome Lists** — 精選的 awesome-* AI agent skills 清單

### 手動技能

未被任何提供方收錄的技能可透過 `data/manual_skills.json` 手動新增：

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

手動技能將：

- 從 GitHub 擷取 `SKILL.md`（使用標準技能資料夾偵測）
- 以 `providerId: "manual"` 寫入 `skills_index.json`
- **不會**被爬蟲覆寫（多次執行後仍保留）
- **會去重**：若 skills.sh 之後收錄同一筆手動技能，則優先使用 skills.sh 的資料

注意：`installs` 至少為 1（最小值）。

## 輸出檔案

爬蟲在 `data/` 目錄產生以下檔案：

### `data/skills.json`

包含三個排行榜的完整技能資料：

```json
{
  "updatedAt": "2024-01-27T00:00:00.000Z",
  "allTime": [...],
  "trending": [...],
  "hot": [...]
}
```

### `data/skills_index.json`

面向網站的**全部**技能索引（由 `data/skills.json` 建構）：

- 當 `data/skills-md/` 下有快取的 `SKILL.md` 時，`description` 為指向 `description_en.txt` 的**路徑**
- 包含 `skillMdPath`，方便網站擷取並呈現完整 Markdown
- 依 `id`（`<source>/<skillId>`）**去重**。若上游有重複，索引保留 `installsAllTime` 最大的一筆

### `data/feed.json`

簡化摘要格式（每個榜單前 50 筆）。

會嘗試透過擷取對應 GitHub `SKILL.md`（快取於 `data/skills-md/`）為每筆補上 `description`：

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

從 GitHub 快取的 `SKILL.md`，常見路徑包括：

- `skills/<skillId>/SKILL.md`（最常見）
- `.claude/skills/<skillId>/SKILL.md`
- `.cursor/skills/<skillId>/SKILL.md`
- `.codex/skills/<skillId>/SKILL.md`
- `plugins/<plugin-name>/skills/<skillId>/SKILL.md`（外掛式儲存庫常見，如 Expo）

存在 `SKILL.md` 時，爬蟲還會產生：

- `description_en.txt`（從 SKILL.md frontmatter 的 `description` 擷取，若有）

預設只為榜單內技能擷取 `SKILL.md`，以維持每日工作速度。

若需同步 `data/skills.json` 中的**全部**技能，可執行：

```bash
SYNC_ALL_SKILL_MDS=1 bun run crawl
```

### `data/feed.xml`

RSS 2.0（XML），供 RSS 閱讀器／訂閱使用。

- 由目前爬取結果 + 上一份 `data/feed.json` 產生
- 僅在有實質變化（新項目／排名躍升）時發布，避免洗版

## 使用方式

### 本機開發

```bash
# 安裝相依套件
bun install

# 執行爬蟲
bun run crawl
```

提示：若希望更完整涵蓋 GitHub 上的 `SKILL.md`（含 `plugins/*/skills/...` 等外掛路徑），  
請設定 `GITHUB_TOKEN` 以降低 API 限流影響：

```bash
export GITHUB_TOKEN=ghp_xxx
bun run crawl
```

### GitHub Actions

推送到 GitHub 後，爬蟲將：

1. 每日 UTC 0:00 自動執行
2. 支援手動觸發（在 Actions 中點選「Run workflow」）
3. 在推送到 main 分支時自動執行

## 在網站中使用

可透過 GitHub Raw URL 直接擷取資料：

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/skills.json
```

或使用 jsDelivr CDN（通常更快）：

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/skills.json
```

### RSS 訂閱（建議）

訂閱 RSS：

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/feed.xml
```

或透過 jsDelivr：

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/feed.xml
```

### 範例程式碼

```typescript
// 在 Next.js 中
const SKILLS_DATA_URL = 'https://cdn.jsdelivr.net/gh/your-username/skills-crawler@main/data/skills.json';

export async function getSkillsData() {
  const res = await fetch(SKILLS_DATA_URL, {
    next: { revalidate: 3600 } // 每小時重新驗證
  });
  return res.json();
}
```

## 說明

- 資料每日更新
- 請遵守各提供方的服務條款
- 僅供個人學習與研究使用

## 貢獻

想新增技能資料來源？歡迎 PR！可參考儲存庫中現有的 provider 實作。
