---
name: literature
description: 文献全链路技能。前置：多源导出题录合并与去重（见 references/multi-source-retrieval.md）。四种模式：(1) 检索；(2) 阅读与综述；(3) LaTeX 插入 \cite{}；(4) 生成 BibTeX。另见 non-zotero-bibliography.md（EndNote/Word 等）。系统综述筛选与 PRISMA 见 systematic-review-lite 技能。
---

# 文献技能（检索 + 阅读/综述 + 引用 + BibTeX）

## 模式选择

| 模式 | 适用场景 | 输出/动作 |
|------|----------|-----------|
| **多源检索与题录合并**（推荐前置） | 多数据库导出 RIS/Bib、可重复检索说明、合并去重 | 见 [references/multi-source-retrieval.md](references/multi-source-retrieval.md)；可选 `scripts/dedupe_bibtex.py` |
| **检索** | 「找文献」「关键词扩展」「Zotero 检索」 | 扩展关键词、检索结果列表、可选脚本 zotero_searcher / zotero_export_bibtex |
| **阅读与综述** | 「读这篇 PDF」「总结文献」「综述重写」「related work 素材」 | 阅读笔记、横向比较、综述段落、BibTeX（改写模式） |
| **插入引用** | 「给这段加引用」「插入 \cite{}」「润色引用句」 | 润色后的 LaTeX 段落含 \cite{key} 或 \cite{key1,key2} |
| **生成 BibTeX** | 「把参考文献列表转成 BibTeX」「生成 .bib」 | BibTeX 条目、简称规则见 references |

根据用户表述选择模式；可串联（如 **多源合并去重 → 检索/阅读 → 插入引用 → 生成 BibTeX**）。读取 PDF 时联动 `pdf` 技能。

**系统综述**（纳入/排除标准、PRISMA 流程记录）请使用 **`systematic-review-lite`** 技能，与本书写类模式互补。

**非 Zotero / 纯 Word 管线**见 [references/non-zotero-bibliography.md](references/non-zotero-bibliography.md)。

目录占位符与环境变量见仓库根目录 [README.md](../../../README.md)（默认 `{{THESIS_DIR}}/references/zotero.bib`）。

---

## 多源检索与题录合并（与「检索」模式配合）

当需要从多个数据库**可重复地**构建题录池时：

1. 在各库使用记录的检索式导出 **RIS 或 BibTeX**；
2. 合并为单一 `.bib`（或先导入 Zotero 再导出）；
3. 按 DOI 或「规范化标题 + 年份」**去重**（见 [multi-source-retrieval.md](references/multi-source-retrieval.md)）；
4. 再进入下方「检索 / 阅读与综述」等模式。

多个 `.bib` 文件合并且需命令行去重时，可使用 `scripts/dedupe_bibtex.py`。

---

## 一、检索模式

- **关键词扩展**：同义词、中英文对应、领域术语、组合查询。
- **检索方式**：语言能力检索 或 脚本（Zotero 本地 API）。脚本见本技能 `scripts/zotero_searcher.py`、`scripts/zotero_export_bibtex.py`；API 默认 `http://localhost:23119/api/`，鉴权可用环境变量 `ZOTERO_LOCAL_API_KEY`。
- **输出**：结构化检索结果（高/中/低相关）、扩展关键词列表。导出 BibTeX 时写入 `{{THESIS_DIR}}/references/zotero.bib`（默认即 `论文章节/references/zotero.bib`，按 citekey 去重）。

检索流程与关键词扩展、相关性排序等详见原 literature-search 设计；脚本用法见下方「脚本」节。

---

## 二、阅读与综述模式

- **阅读模式**：对单篇/多篇 PDF 提取元数据、主旨、方法、结论、与本文相关性、启发性信息；多篇时做横向比较与综合结论。输出结构参考 [references/output-template.md](references/output-template.md)。
- **改写模式**：综述草稿→规范学术综述，保留引用、补充文献、优化结构、输出 BibTeX。技术要点见 [references/rewriting-workflow.md](references/rewriting-workflow.md)。
- **端到端模式**：阅读结果→可插入论文的综述段落，标明可插入位置与 \cite{} 线索。

PDF 正文提取使用 `pdf` 技能。不编造 DOI/期刊/作者/结果；与当前论文相关性需显式判断。

---

## 三、插入引用模式

- **引用类型**：直接引用、间接引用、多项引用；带页码 \cite[p. 10]{key}、带章节 \cite[Chapter 3]{key}。
- **格式**：`\cite{key}`、`\cite{key1, key2}`；润色句首句尾使衔接自然，符合学术规范。
- **Zotero 自动补引**：用户提供 Zotero API 且要求「对段落加文献依据」时，用 scripts 检索→导出 BibTeX→在句末插入 \cite{} 并润色。

详见 [references/citation-formats.md](references/citation-formats.md)、[references/language-polishing.md](references/language-polishing.md)、[references/citation-examples.md](references/citation-examples.md)。

---

## 四、生成 BibTeX 模式

- **输入**：参考文献列表（中/英/混合）；若来自 PDF 阅读或用户提供全文/摘要，一并作为摘要来源。
- **简称规则**：英文 作者首字母+年份+中文关键词；中文 作者姓氏首字母+年份+中文简称。见 [references/abbreviation-rules.md](references/abbreviation-rules.md)、[references/bibtex-types.md](references/bibtex-types.md)。
- **输出**：完整 .bib 条目，含 note 字段（中文简称/英文原名）。**尽量附带摘要**：在生成每条 BibTeX 时，(1) 若有文献自带摘要或用户/阅读笔记提供的摘要，则在 `note` 中增加「摘要: …」；(2) **若无现成摘要但可读取原文**（如 PDF 正文、已提取文本），则从原文中总结 1～2 句话作为摘要写入 `note`；(3) 仅当既无摘要又无法读取原文时不写摘要，不编造内容。类型：article、inproceedings、phdthesis、book、techreport 等。

详见 [references/conversion-examples.md](references/conversion-examples.md)、[references/bibtex-types.md](references/bibtex-types.md) 中关于 note 与摘要的约定。

---

## 参考文档汇总

- [references/multi-source-retrieval.md](references/multi-source-retrieval.md)：多库导出、合并与去重
- [references/non-zotero-bibliography.md](references/non-zotero-bibliography.md)：EndNote/Mendeley/Word 等与 LaTeX 混用
- [references/output-template.md](references/output-template.md)：阅读模式输出模板
- [references/rewriting-workflow.md](references/rewriting-workflow.md)：综述改写流程与引用处理
- [references/citation-formats.md](references/citation-formats.md)：引用格式
- [references/language-polishing.md](references/language-polishing.md)：引用句润色
- [references/citation-examples.md](references/citation-examples.md)：插入示例
- [references/bibtex-types.md](references/bibtex-types.md)：BibTeX 类型
- [references/abbreviation-rules.md](references/abbreviation-rules.md)：简称规则
- [references/conversion-examples.md](references/conversion-examples.md)：Bib 转换示例

## 脚本

- `scripts/zotero_searcher.py`：Zotero 本地库检索（--query、--expand、--limit、--base-url、--api-key）。
- `scripts/zotero_export_bibtex.py`：按 item-key 导出 BibTeX 到指定 .bib（--bib-path、--item-key 可多次）。
- `scripts/dedupe_bibtex.py`：合并多个 `.bib` 并按 DOI / 标题+年份去重（无网络依赖，见脚本 `--help`）。
