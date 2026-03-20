---
name: figma-to-code
description: >
  Convert Figma designs into production-ready HTML+CSS through a structured 5-phase
  pipeline with visual QA. Use when the user wants to convert a Figma design into code,
  slice a Figma mockup into a web page, or code a Figma URL. Triggers on: Figma URL
  (figma.com/design/...), "figma to code", "切版", "slicing", "convert design",
  "implement this design", "code this mockup". Requires Figma MCP server connection.
---

# Figma to Code

將 Figma 設計稿透過 5 階段 Pipeline 轉換為 HTML+CSS。

## Prerequisites

嘗試呼叫任一 Figma MCP 工具（如 `get_metadata`）。

- **工具不可用** → 告知「需要先連線 Figma MCP server」，然後 **STOP**。
- **工具可用** → 進入 Phase 1。

Figma MCP 工具用法：`references/figma-mcp-guide.md`（視為權威來源）。

---

## Phase 1: 專案設定收集（Inversion Pattern）

**GATING: DO NOT 進入 Phase 2，直到所有 12 項設定確認完畢。**

載入 `references/project-settings.md`，逐一詢問工程師 12 項設定。每次一項，附帶選項與預設建議。

工程師說「用預設」→ 採用預設值，回覆「已使用預設值：{值}」。

收集完成後輸出摘要表格，詢問「確認以上設定，或指出需要修改的項目。」

**CHECKPOINT: 工程師確認摘要 → 進入 Phase 2。**

---

## Phase 2: 設計稿偵察

### Step 2.1: 取得 Figma URL

請工程師貼上 Figma 設計稿 URL。依 `references/figma-mcp-guide.md` 解析 `fileKey` 和 `nodeId`。

### Step 2.2: 讀取節點樹

呼叫 `get_metadata(fileKey, nodeId)`。

### Step 2.3: 列出主要 Frame

提取所有頂層 frame：

```
區塊列表：
1. [frame-name] — [尺寸] — [簡述]
2. [frame-name] — [尺寸] — [簡述]
```

### Step 2.4: 確認區塊切分

讓工程師操作：**確認** / **合併**（多個→一個）/ **拆分**（一個→多個）。

產出最終區塊切分清單：

```
[1] header — node-id: xxx
[2] hero-section — node-id: xxx
[3] features — node-id: xxx
```

**CHECKPOINT: 工程師確認區塊切分 → 進入 Phase 3。**

---

## Phase 3: 逐區塊轉換

按區塊切分清單依序處理。DO NOT 跳過任何區塊。

### 每個區塊的處理流程

**Step 3.1: 取得設計數據**

呼叫 `get_design_context(fileKey, nodeId)`。記錄 code、hints、Code Connect 映射。

依 `references/figma-mcp-guide.md` 的「代碼適配規則」決定如何使用回傳數據。

**Step 3.2: 取得截圖**

呼叫 `get_screenshot(fileKey, nodeId)`。保留作為視覺參考。

**Step 3.3: 生成 HTML + CSS**

依據 Phase 1 設定生成代碼：

1. **結構（HTML）** — 根據語義標籤偏好、class 命名風格、註釋標記設定
2. **樣式（CSS）** — 根據 CSS 方法論、單位偏好，從 hints 提取顏色/字型/間距。優先使用 design token 或 CSS 變數
3. **格式** — 根據產物格式（內嵌或分離）和檔案命名規則

**Step 3.4: 視覺比對（Reviewer Pattern）**

載入 `references/visual-qa-checklist.md`，執行「區塊級」比對流程。

- CRITICAL 或 HIGH 偏差 → 修正代碼，說明修正內容
- 回報：「區塊 [N] [name] — [PASS / 修正了 X 項]」

**CHECKPOINT: 所有區塊轉換完成 → 進入 Phase 4。**

---

## Phase 4: 圖片資源匯出

### Step 4.1: 識別可匯出資源

掃描設計稿中所有圖片和 icon：

```
可匯出資源：
1. [node-name] — 類型: icon — 建議格式: SVG
2. [node-name] — 類型: photo — 建議格式: WebP
```

### Step 4.2: 匯出圖檔

根據工程師的圖片格式偏好匯出。icon → SVG 優先，照片 → 依偏好選 PNG 或 WebP。存放至指定路徑。

### Step 4.3: 匯出備案

API 匯出失敗時，提供手動匯出指引：

```
1. 在 Figma 選取 [node-name]
2. 右側面板 → Export → [格式] → [倍率]
3. 存放至 [路徑]/[檔名]
```

**CHECKPOINT: 所有資源匯出完成（或提供手動指引）→ 進入 Phase 5。**

---

## Phase 5: 組裝與驗收

### Step 5.1: 組裝所有區塊

按結構順序組合 HTML 和 CSS：
- 建立整頁 HTML 結構
- 合併 CSS（避免命名衝突）
- 引入匯出圖片路徑
- 如有 CSS reset/base style，在最前面引入

### Step 5.2: 響應式設計

根據 Phase 1 斷點定義加上 media query。調整重點：多欄→單欄、導航→漢堡選單、字型/間距比例縮放。

### Step 5.3: 最終視覺驗收（Reviewer Pattern）

呼叫 `get_screenshot` 取得完整頁面截圖。

載入 `references/visual-qa-checklist.md`，執行「頁面級」比對流程。

- 任何 CRITICAL FAIL → 修正後重新比對
- 輸出驗收報告：

```
## 驗收報告

| 嚴重度 | 項目 | 狀態 | 備註 |
|--------|------|------|------|
| CRITICAL | 佈局結構 | PASS/FAIL | — |
| HIGH | 間距一致 | PASS/WARN | — |
| ... | ... | ... | ... |

結果：[PASS / 修正後通過 / 需要人工確認]
```

**FINAL CHECKPOINT: 驗收 PASS → 交付成品給工程師。**
