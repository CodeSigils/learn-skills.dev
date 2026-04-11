---
name: ljg-card
description: "Content caster (鑄). Transforms content into PNG visuals. Six molds: -l (default) long reading card, -i infograph, -m multi-card reading cards (1080x1440), -v visual sketchnote, -c comic (manga-style B&W), -w whiteboard (marker-style board layout). Output to ~/Downloads/. Use when user says '鑄', 'cast', '做成圖', '做成卡片', '做成資訊圖', '做成海報', '視覺筆記', 'sketchnote', '漫畫', 'comic', 'manga', '白板', 'whiteboard'. Replaces ljg-cards and ljg-infograph."
user_invocable: true
version: "1.7.0"
---

# ljg-card: 鑄

將內容鑄成可見的形態。內容進去，PNG 出來。模具決定形狀。

## 引數

| 引數 | 模具 | 尺寸 | 說明 |
|------|------|------|------|
| `-l`（預設） | 長圖 | 1080 x auto | 單張閱讀卡，內容自動撐高 |
| `-i` | 資訊圖 | 1080 x auto | 內容驅動的自適應視覺佈局 |
| `-m` | 多卡 | 1080 x 1440 | 自動切分為多張閱讀卡片 |
| `-v` | 視覺筆記 | 1080 x auto | 手繪風格 sketchnote，動態選擇風格路線 |
| `-c` | 漫畫 | 1080 x auto | 日式黑白漫畫風格，動態選擇漫畫家視覺語言 |
| `-w` | 白板 | 1080 x auto | 白板馬克筆風格，結構化框圖+箭頭+彩色標記 |

## 約束

本 skill 輸出為視覺檔案（PNG），不適用 L0 中的 Org-mode、Denote 和 ASCII-only 規範。

## 共享基礎

### 獲取內容

- URL --> WebFetch 獲取
- 貼上文字 --> 直接使用
- 檔案路徑 --> Read 獲取

### 檔案命名

從內容提取標題或核心思想作為 `{name}`（中文直接用，去標點，≤ 20 字元）。

### 截圖工具

```bash
node ~/.claude/skills/ljg-card/assets/capture.js <html> <png> <width> <height> [fullpage]
```

依賴：`~/.claude/skills/ljg-card/node_modules/` 中的 playwright。如報錯：

```bash
cd ~/.claude/skills/ljg-card && npm install playwright && npx playwright install chromium
```

### Footer

- 左側：logo + 李繼剛（已硬編碼在模板中）
- 右側：內容來源（可選）——有明確來源時顯示（如作者名、arxiv ID、網站名等），無來源時留空。使用 `{{SOURCE_LINE}}` 變數：有來源時填 `<span class="info-source">來源文字</span>`，否則空字串。適用於 `-l`、`-i`、`-v`、`-c`、`-w` 模具（`-m` 多卡無 footer，不適用）。

### 交付

1. 報告檔案路徑

## 品味準則

**所有模具共享**。執行任何模具前，先 Read `references/taste.md`，作為視覺質量底線貫穿全流程。

核心：反 AI 生成痕跡——禁 Inter 字型、禁純黑、禁三等分卡片、禁居中 Hero、禁 AI 文案腔、禁假資料。

## 執行

根據引數選擇模具，Read `references/taste.md` + 對應的 mode 檔案，按步驟執行：

### -l（預設）：長圖

Read `references/mode-long.md`，按其步驟執行。

模板：`assets/long_template.html`

### -i：資訊圖

Read `references/mode-infograph.md`，按其步驟執行。

模板：`assets/infograph_template.html`

### -m：多卡

Read `references/mode-poster.md`，按其步驟執行。

模板：`assets/poster_template.html`

### -v：視覺筆記

Read `references/mode-sketchnote.md`，按其步驟執行。

模板：`assets/sketchnote_template.html`

### -c：漫畫

Read `references/mode-comic.md`，按其步驟執行。

模板：`assets/comic_template.html`

### -w：白板

Read `references/mode-whiteboard.md`，按其步驟執行。

模板：`assets/whiteboard_template.html`
