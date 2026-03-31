---
name: cangjie
description: 面向仓颉 / Cangjie 编程语言的代码生成、工程设计、问题修复与大型仓库分析技能。只要用户提到“仓颉 / Cangjie / .cj / cjpm / cjc / cjfmt / cjdb / LSP”，或要生成/修复仓颉函数、类型、模块、workspace、多模块包设计、并发、网络、宏、FFI 示例，或分析真实仓颉仓库的模块层次、`package.package-configuration`、`workspace`、组织名与版本差异，就应主动使用本技能。即使用户没有明确说“用 skill”，只要任务核心是编写、修正或分析仓颉代码与工程结构，也应使用本技能。
compatibility: 优先读取当前工作区 `references/dev-guide`、`references/tools` 与 `release-notes`；若缺失，再回退到本技能 bundled 的 `references/dev-guide` 与 `references/tools`。
---

# Cangjie Skill

这个技能的目标不是把回答写成仓颉语法百科，而是帮助模型用尽量少的 token，稳定地产出更接近官方文档约束的仓颉代码、工程结构和分析结论。

默认优化目标：

1. 先给正确结构，再给深入解释。
2. 先走最短文档路径，再决定是否继续下钻。
3. 优先减少臆造 API、错误包结构和无效长篇输出。
4. 遇到大型工程时，先做结构化盘点，再做设计建议。

## 何时使用

当用户出现以下任一意图时，优先使用本技能：

- 生成仓颉函数、类型、模块、类、接口、泛型、模式匹配、异常处理代码
- 把其他语言、伪代码或设计思路改写成仓颉
- 生成 `cjpm` 项目、workspace、多模块目录结构和 `cjpm.toml`
- 修复仓颉编译错误、入口函数错误、包声明错误、依赖配置错误
- 设计仓颉包边界、模块分层、本地 `path` 依赖、组织名命名方案
- 分析真实仓颉仓库的 `src/` 层次、`package.package-configuration`、`workspace`、`output-type`
- 回答 `cjpm`、`cjfmt`、`cjdb`、LSP、交叉编译、中心仓依赖等工具链问题
- 涉及 `stdx`、宏、FFI、并发、网络、多平台等专题

## 知识源优先级

按下面顺序取知识，不要跳级：

1. 工作区原始文档
   - `references/dev-guide/source_zh_cn/`
   - `references/tools/source_zh_cn/`
   - `release-notes/`
2. 工作区英文原文
   - `references/dev-guide/source_en/`
   - `references/tools/source_en/`
3. 本技能的索引与摘要
   - `references/pattern-index.md`
   - `references/syntax-essentials.md`
   - `references/path-index.md`
   - `references/doc-map.md`
   - `references/codegen-guidelines.md`
   - `references/version-notes.md`
   - `references/online-fallback.md`
4. bundled 原文
   - `references/dev-guide/`
   - `references/tools/`
5. 官方在线文档与中心仓
   - `https://cangjie-lang.cn/docs`
   - `https://docs.cangjie-lang.cn/`
   - `https://pkg.cangjie-lang.cn/index`
6. 模型记忆

原则：

- 常见任务先读 pattern，不要一上来扫描整份文档。
- 中文够用时不要切英文；只有细节缺失或术语不稳时才回退英文。
- `release-notes` 只在版本差异、中心仓、组织名、Common/Specific、交叉编译、工具行为变化等问题上再读。
- 本地 `references/` 足够时，不要立刻联网。
- 只有本地资料未命中、信息明显缺失、或用户明确要求查库时，才回退到官方在线文档和中心仓。
- 联网时优先只查官方域名，不要把第三方博客当主依据。

## 依赖工具

| 工具 | 用途 | 必需 |
|------|------|------|
| `WebSearch` | 搜索官方文档页与中心仓条目 | 是 |
| `WebFetch` | 获取命中页面的深度内容 | 是 |
| `Bash` | 本地 `rg` 搜索、脚本执行与必要的辅助抓取 | 是 |

## 任务分流

先把请求归到最接近的一类，再读取最少的文档。

### 1. 语法示例 / 小函数 / 小算法

适用：

- 单个函数
- 单文件语法示例
- `struct` / `enum` / `class` / `match` / 泛型骨架

默认读取：

1. `references/syntax-essentials.md`
2. 必要时再读 1 个相关原文文件

默认交付：

- 单个 `.cj` 文件
- `cjc` 编译命令

### 2. 单模块 `cjpm` 项目

适用：

- 命令行参数
- 最小项目骨架
- 多文件但仍是单模块

默认读取：

1. `references/patterns/cjpm-project-minimal.md`
2. 必要时再读
   - `references/dev-guide/source_zh_cn/package/entry.md`
   - `references/tools/source_zh_cn/cmd-tools/cjpm_manual.md`

默认交付：

1. 目录结构
2. `cjpm.toml`
3. `src/main.cj`
4. 其他关键源码
5. `cjpm build` / `cjpm run`

### 3. workspace / 包设计 / 多模块工程

适用：

- `app` 依赖 `core`
- 本地 `path` 依赖
- 工作空间根配置
- 组织名设计

默认读取：

1. `references/patterns/package-workspace-design.md`
2. 必要时再读
   - `references/tools/source_zh_cn/cmd-tools/cjpm_manual.md`
   - `references/dev-guide/source_zh_cn/package/`

默认交付：

1. workspace 目录结构
2. 根 `cjpm.toml`
3. 子模块 `cjpm.toml`
4. 关键包声明和导入示例
5. 包职责说明

### 4. 编译错误 / 结构错误 / 配置错误修复

适用：

- `main(): String`
- `package` / `import` 错误
- `cjpm.toml` 字段冲突
- `path/git/version` 配置错误

默认读取：

1. 用户给出的代码或配置
2. 若属于依赖来源、组织名、workspace 约束，先读 `references/patterns/version-config-fix.md`
3. 再读 1 个相关工具或包文档
4. 如果明显涉及版本变化，再读 `references/version-notes.md`

默认交付：

1. 先指出最可能的结构性错误
2. 再给修正后的代码或配置
3. 最后给验证命令

### 5. 并发 / 网络 / 宏 / FFI / 多平台

适用：

- `spawn`
- `stdx.net.http`
- `macro package`
- `foreign func`
- 交叉编译 / Android / iOS

默认读取：

1. 对应 pattern
2. 必要时再读 1 到 2 个原文文件
3. 若涉及工具参数或版本行为，再读工具文档或 release notes

默认交付：

- 最小可运行示例优先
- 明确写出依赖前提、编译顺序和风险点

### 6. 大型真实仓库分析

适用：

- 用户给出真实仓库路径
- 需要分析分层、模块职责、依赖方向
- 需要新增一个模块或包

默认读取顺序：

1. 根 `cjpm.toml`
2. `src/` 一级和二级目录树
3. 只打开少量代表性文件：
   - 顶层 `pkg.cj`
   - 入口 `main.cj`
   - 用户点名的文件
4. 若需要再看 1 到 3 个具体源码文件

工具选择：

- 目录树与精确文件优先用 `Glob` / `Read` / `Grep` 风格工具
- 只有这些工具不够时才退回 shell
- 不要为了简单的目录枚举先用 `Bash ls/find`

默认交付：

1. 工程概览
2. 模块分层
3. 依赖方向
4. 库模块 / 动态模块 / 可执行模块区分
5. 新模块建议
6. 配置片段和源码骨架

如果用户明确要求“直接基于这个真实仓库生成一个新模块/新文件”，先读：

1. `references/patterns/existing-large-repo-module-codegen.md`
2. 根 `cjpm.toml`
3. 目标层目录树
4. 1 到 3 个相邻现有模块文件

工具选择：

- 先用结构化文件读取工具获取目录树和邻近文件
- 避免为了简单目录查看调用 shell

然后只输出：

1. 放置位置
2. `cjpm.toml` 配置片段
3. 3 到 6 个关键新文件
4. 接入点说明

不要：

- 一上来读大量 `.cj` 文件
- 还没确认真实结构就发明层次
- 先写一大段新代码，再补当前仓库分析

### 7. 工具链 / 版本差异

适用：

- `cjpm` 字段解释
- `cjfmt` / `cjdb` / LSP
- `version` / 中心仓 / 组织名
- Common/Specific
- `TrustALL`

默认读取：

1. 相关工具手册的最小片段
2. `references/version-notes.md`

默认交付：

- 先说现在的约束
- 再说版本差异
- 最后给修正配置或命令

### 8. 在线文档回退 / 中心仓搜索

适用：

- 本地 `references/` 未命中
- 本地资料缺少某个 API、工具参数或新版本细节
- 需要搜索中心仓里是否已有相关仓颉库

默认读取：

1. 先看 `references/online-fallback.md`
2. 优先使用工具：
   - `WebSearch`
   - `WebFetch`
   - 必要时 `Bash`
3. 再查官方在线文档：
   - `cangjie-lang.cn/docs`
   - `docs.cangjie-lang.cn`
4. 若是库/依赖问题，再查：
   - `pkg.cangjie-lang.cn/index`

默认交付：

- 先说明“本地资料未命中，改查官方在线资料”
- 再给官方文档或中心仓命中线索
- 最后给保守建议，不把在线搜索结果包装成绝对确定的 API 承诺

## Token 预算

除非用户明确要求深度分析，否则遵守下面的读文档预算：

- 小语法题：最多 1 个 pattern 或 1 个语法速记文件，必要时再加 1 个原文文件
- 单模块项目：最多 1 个 pattern + 1 个包/工具文件
- workspace 设计：最多 1 个 pattern + 1 个 `cjpm_manual` 片段 + 1 个包文档
- 配置修复 / 版本差异：最多 1 个 pattern + 1 个工具文档片段 + 1 个 release note
- 高级专题：最多 1 个 pattern + 1 到 2 个原文文件
- 大型仓库分析：根 `cjpm.toml` + `src` 目录树 + 最多 6 个代表性文件
- 大仓内直接模块生成：1 个 codegen pattern + 根配置 + 目标层目录树 + 最多 3 个相邻模块文件
- 版本差异：最多 1 个 release note + 1 个工具文档片段
- 在线回退：最多 3 个官方页面 + 最多 5 个中心仓线索

停手规则：

- 已经拿到合法骨架、关键限制和关键命令后，立即回答
- 不要为了“更稳”而顺手全局搜索整个 `references/`
- 不要在大仓分析里遍历所有 `.cj` 文件
- 不要在配置修复题里顺手展开成长篇教程
- 不要在本地资料已经足够时顺手去全网搜索
- 不要把同一个约束重复解释两次

## 输出目标

默认输出应满足：

1. 先给代码或结构，再给说明。
2. 说明只保留关键约束和假设。
3. 代码中的解释性注释默认使用中文。
4. 不要求落盘时，默认直接在回答中内联关键文件内容。
5. 用户要求项目、多文件或 workspace 时，必须给关键文件的完整内容，而不是只给摘要。

项目型回答优先使用这个顺序：

1. 目录结构
2. `cjpm.toml`
3. `src/main.cj`
4. 其他关键源码
5. 构建 / 运行 / 调试命令
6. 2 到 6 行关键说明

大型仓库分析优先使用这个顺序：

1. 工程概览
2. 模块分层
3. 依赖方向
4. 库 / 动态 / 可执行模块区分
5. 新模块建议
6. 配置片段

## 高优先级约束

### 入口与包结构

- 程序入口必须是顶层 `main`
- `main` 参数只用无参或 `Array<String>`
- `main` 返回类型只用 `Unit` 或整数类型
- `cjpm` 项目里源码默认放 `src/`
- 项目示例默认显式写 `package`
- workspace 根 `cjpm.toml` 里不要同时出现 `[package]` 和 `[workspace]`

### 包设计与多模块

- 入口 `main` 只放在可执行模块
- 可复用逻辑放到独立模块
- `public` 只暴露跨模块必需的声明
- 本地多模块关系优先用 `path` 依赖表达
- 若配置了 `organization`，包声明和导入要使用 `org::pkg` 形式
- workspace 成员即使同在一个根目录下，只要模块源码互相 `import`，也要显式声明 `[dependencies]`，除非你明确把公共依赖配在根 workspace

### 工具链与版本

- 若出现 `only one of 'git' or 'path' or 'version' fields can exist`，优先想到中心仓 `version` 字段与本地/远程依赖互斥
- 若用户问组织名、Common/Specific、中心仓或交叉编译，主动查看 `references/version-notes.md`
- 若用户没有给具体版本，默认按当前工作区文档主线回答，并标注“该点可能受版本影响”
- 区分 `cjpm.toml` 的 `output-type` 与 `cjc --output-type`
- 在 `cjpm.toml` 里优先使用 `static / dynamic / executable`
- 不要把 `cjc` 命令行里的 `staticlib / dylib` 直接搬进 `cjpm.toml`

### `stdx`

- `stdx.net.*`、`stdx.log.*` 等能力不要当作基础 SDK 必定内置
- 要提醒用户先下载对应软件包，并在 `cjpm.toml` 中配置依赖

### 宏

- 宏定义和宏调用不要放在同一包
- 宏定义使用 `public`
- 先编译宏包，再通过 `--import-path` 编译调用方
- 最小宏示例优先给分包结构，不要一开始展开成复杂工程

### FFI

- `foreign` 只声明，不实现
- 外部调用放在 `unsafe` 块中
- 不使用命名参数和默认值
- 对类型映射没把握时，不要臆造复杂签名

## 自检清单

回答前快速自检：

1. 我是否选对了单文件 / `cjpm` / workspace / 大仓分析形态？
2. 我是否只读了最少、最相关的文档？
3. 我是否明确说明了 `stdx`、宏、FFI、版本差异等前提？
4. 我是否给了关键文件完整内容和验证命令？
5. 我是否把不确定的 API 标成“需按本地 SDK 核对”？
6. 如果是大仓分析，我是否先基于真实目录和根配置总结，再给新增模块建议？

## 参考资料

- `references/pattern-index.md`
- `references/syntax-essentials.md`
- `references/path-index.md`
- `references/doc-map.md`
- `references/codegen-guidelines.md`
- `references/version-notes.md`
- `references/online-fallback.md`
- `references/patterns/`

只有任务确实涉及该主题时才继续往下读，避免把仓颉 skill 变成高 token 的“大而全提示词”。
