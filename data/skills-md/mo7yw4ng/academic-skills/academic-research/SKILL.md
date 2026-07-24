---
name: academic-research
description: "Complete academic research skill suite covering the full pipeline: paper reading (read/explain papers with storytelling), idea generation (brainstorm research directions), experiment design (plan experiments, ablation, baselines), proof writing (mathematical proofs, LaTeX theorems), paper writing (draft to camera-ready for top venues like NeurIPS/ICLR/ACL), paper review (structured 4-step review with scoring), and professor fit analysis (evaluate advisors, cold emails, interview strategy). Use when the user wants the full research workflow or is unsure which specialized skill to pick. Trigger keywords: academic research suite, research pipeline, read paper, brainstorm, experiment design, prove, write paper, review, professor fit, advisor, cold email, LaTeX, research, NeurIPS, ICLR, ACL, arXiv, 讀論文, 寫論文, 審稿, 實驗設計, 數學證明, 研究方向, 教授分析, 選指導教授."
license: MIT
compatibility: Works with Claude Code, ChatGPT/Codex CLI, Cursor, Gemini CLI, and other Agent Skills clients.
metadata:
  author: research-skills
  version: "2.0.0"
---

# Academic Research Skills Suite

一套完整的學術研究 Skill 套件，涵蓋從論文閱讀到撰寫、審稿的完整研究流程。

本 skill 是**路由入口**：根據使用者意圖，改用（或引導載入）對應的專門 skill。各 skill 安裝後彼此獨立，以 **skill name** 協作，不依賴 monorepo 相對路徑。

---

## Skill 路由表

| 觸發條件 | Skill name | 說明 |
|----------|------------|------|
| 讀論文、解釋論文、paper reading、看不懂這篇 | `paper-reading` | 太奶角色論文導讀（繁中） |
| 想 idea、brainstorm、研究方向、下一步做什麼 | `idea-generation` | 發散→搜索→收斂三階段構思 |
| 實驗設計、ablation、baseline、跑什麼實驗 | `experiment-design` | 實驗設計與規劃 |
| 數學證明、prove、theorem、推導 | `proof-writer` | 理論推導與數學證明 |
| 寫論文、paper writing、improve my paper、LaTeX | `paper-writing` | 論文撰寫（頂會標準） |
| review、審稿、reviewer 會怎麼說、這篇能上嗎 | `paper-review` | 4 步驟學術審稿 |
| 教授分析、professor fit、選指導教授、cold email、申請策略 | `professor-fit-analyzer` | 教授適配度分析與申請策略 |

**指引**：

1. 若已安裝對應 skill，直接載入該 skill 並依其指示執行。
2. 若僅安裝本 suite skill，依下方 Pipeline 與共享資源完成任務；並提示使用者可用 `npx skills add <owner/repo> --skill <name>` 安裝專門 skill。
3. 需求橫跨多個 skill 時，依 Pipeline 順序處理。

---

## Skill Pipeline

```
professor-fit-analyzer ─┐
                        ↓
paper-reading ──→ idea-generation ──→ experiment-design
      │                                       │
      ↓                                       ↓
paper-review ←── paper-writing ←──── proof-writer
      │                 ↑
      └─────────────────┘  (revision cycle)
```

---

## 語言慣例

- **預設語言**: 繁體中文（分析、解釋、討論）
- **英文場景**: LaTeX 生成、正式審稿輸出、數學符號與定理名稱
- **學術詞彙**: 參考 [references/chinese-academic-glossary.md](references/chinese-academic-glossary.md) 確保一致性

---

## 共享資源

- [references/chinese-academic-glossary.md](references/chinese-academic-glossary.md) — 中英學術詞彙對照
- [references/conference-standards.md](references/conference-standards.md) — 各頂會格式標準
- [references/researcher-philosophies.md](references/researcher-philosophies.md) — 研究者哲學與寫作風格
