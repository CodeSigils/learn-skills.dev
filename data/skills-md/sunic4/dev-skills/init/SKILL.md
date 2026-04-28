---
name: "init"
description: "项目初始化与骨架生成。当在新项目中首次使用 dev-skills 工作流时调用，或需要重置/修复 wiki/ 目录结构时调用。一键生成 wiki/ 完整目录树和 AGENTS.md。"
---

# Init - 项目初始化

## 职责
生成项目所需的完整 wiki/ 骨架目录 + AGENTS.md

## 触发条件
- 新项目首次使用 dev-skills 工作流
- wiki/ 目录缺失或损坏需要重建
- 需要补充缺失的子目录

## 执行步骤

### Step 1: 创建 wiki/ 骨架

在项目根目录下创建以下目录结构（已存在则跳过）：

```
wiki/
├── tools/                    # 工具脚本 (由 init 从模板复制)
│   ├── validate-yaml.mjs     # YAML schema 校验器
│   ├── review-generate.mjs   # review 报告生成器
│   └── read-yaml.mjs         # 选择性 YAML 读取器（上下文控制）
├── raw/
│   ├── user-inputs/          # 用户原始输入存档
│   ├── research/             # 网络调研资料
│   └── references/           # 外部参考资料
├── requirements/             # 需求文档 (slug 命名)
├── architecture/
│   ├── overview.md           # 系统总览 (首次 arch 时创建)
│   ├── decisions/            # ADR 技术决策
│   └── modules/              # 模块设计文档
├── roadmaps/                 # 大需求拆解规划 (一个 roadmap 一个目录)
├── features/                 # 特性开发记录 (一个 feature 一个目录)
├── issues/                   # 问题修复记录
└── knowledge/
    ├── raw/                 # 原始写入区 (各技能写到这里，不可被其他技能检索)
    ├── patterns/            # 正式发布区 (经过 kb 整理后可读)
    ├── lessons/
    ├── decisions/
    ├── references/
    └── _archive/            # 归档 (过时但保留)
```

### Step 2: 复制工具脚本

将脚本模板从技能定义目录复制到 `wiki/tools/`（已存在则跳过）：

```
源模板位置 (只读参考):  .trae/skills/init/references/tools/
目标运行位置 (可执行):   wiki/tools/
```

**复制清单**:

| 脚本 | 用途 |
|------|------|
| `yaml-utils.mjs` | 共享 YAML 工具库（解析/序列化/值转换），其他脚本的依赖 |
| `validate-yaml.mjs` | 校验所有 YAML 文件是否符合 schema（impl-checklist/items/review-report/kb-status/project-status） |
| `review-generate.mjs` | 读取 impl-checklist.yaml 生成 review-report.yaml 模板 |
| `read-yaml.mjs` | **选择性读取** YAML 字段，控制 agent 上下文（支持 query/summary/flat） |

**使用方式**:
```bash
# 在项目根目录下运行
node wiki/tools/validate-yaml.mjs wiki/features/xxx/impl-checklist.yaml --schema impl_checklist
node wiki/tools/review-generate.mjs --feature xxx
node wiki/tools/read-yaml.mjs wiki/features/xxx/impl-checklist.yaml --query "meta.status,files[*].path"
node wiki/tools/read-yaml.mjs wiki/features/xxx/impl-checklist.yaml --summary
```

### Step 3: 生成 .gitignore

在**项目根目录**创建/更新 `.gitignore`（已存在则追加缺失规则，不覆盖已有内容）：

```gitignore
# === dev-skills 工作流 ===
wiki/raw/
wiki/knowledge/_archive/

# === 常规忽略 ===
node_modules/
dist/
build/
*.log
.DS_Store
Thumbs.db

# === IDE ===
.vscode/
.idea/
*.swp
*.swo
```

> ⚠️ 如果项目已有 `.gitignore`，只追加 `dev-skills 工作流` 段落中的条目。

### Step 4: 检测语言与框架

**目的**: 确定项目的技术栈，为后续生成 CodeStyle 和 AGENTS.md 选择合适的模板。

#### 4.1 自动检测

扫描项目文件，检测编程语言和框架：

| 检测项 | 检测方法 |
|--------|---------|
| 编程语言 | 检查文件扩展名分布 (`.ts`, `.py`, `.rs`, `.go`, `.java` 等) |
| 包管理器 | 检查锁文件 (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `poetry.lock`, `Cargo.lock` 等) |
| 框架 | 检查依赖配置 (`package.json` dependencies, `pyproject.toml`, `Cargo.toml` 等) |
| 构建工具 | 检查配置文件 (`vite.config.*`, `webpack.config.*`, `tsconfig.json` 等) |
| 测试框架 | 检查测试依赖和配置 |
| 代码质量工具 | 检查 ESLint/Prettier/Black/Ruff/Clippy 等配置 |

**检测优先级**:
1. 现有代码库 → 统计文件扩展名分布
2. 配置文件 → 读取依赖声明
3. 锁文件 → 确认实际安装的依赖

#### 4.2 模板选择

根据检测结果，从 `references/templates/` 选择合适的模板：

```
references/templates/
├── languages/           # 编程语言模板
│   ├── typescript/
│   │   ├── codestyle.md
│   │   └── agents-sections.md
│   ├── python/
│   ├── rust/
│   └── ...
└── frameworks/          # 框架模板 (会与语言模板合并)
    ├── react/
    ├── vue/
    ├── nextjs/
    ├── fastapi/
    └── ...
```

**选择逻辑**:
1. 先选择语言模板
2. 再选择框架模板（如有）
3. 合并两者内容，框架模板覆盖语言模板的特定部分

#### 4.3 不确定时的处理

当无法自动确定技术栈时，使用 AskUserQuestion 工具询问用户：

```markdown
问题: 请选择项目的主要编程语言
选项:
- TypeScript (推荐)
- Python
- Rust
- Go
- Java
- 其他
```

#### 4.4 记录检测结果

将检测结果写入 `wiki/raw/project-tech-stack.yaml`:

```yaml
detected_at: "2024-01-15T10:30:00Z"
language: typescript
framework: react
package_manager: pnpm
build_tool: vite
test_framework: vitest
lint_tool: eslint
format_tool: prettier
confidence: high  # high/medium/low
source: auto_detected  # auto_detected / user_specified
```

### Step 5: 生成 CodeStyle 规范

在**项目根目录**创建 `codestyle.md`（或更新 AGENTS.md 中的「关键约定」章节）：

**生成策略**:

1. **有现有代码**: 
   - 加载 Step 4 选中的模板作为基础
   - 扫描代码库自动推断风格特征
   - 合并模板规范与推断结果
   - 生成规范文档供 agent 遵循

2. **无现有代码（全新项目）**: 
   - 直接使用 Step 4 选中的模板
   - 保留 `{待确认}` 占位符
   - 首次 feat 时由 agent 根据实际编码填充

3. **已存在 codestyle.md**: 
   - 不覆盖
   - 仅标注 `{待确认}` 条目供审查

**模板合并逻辑**:

```
基础模板 (languages/typescript/codestyle.md)
    +
框架模板 (frameworks/react/codestyle.md)  [可选]
    +
代码库推断结果  [有代码时]
    =
最终 codestyle.md
```

**输出格式**:

```markdown
# CodeStyle - {项目名} 代码风格规范

## 模板来源
- 语言模板: {language}/codestyle.md
- 框架模板: {framework}/codestyle.md (如有)
- 推断来源: 代码库扫描 / 用户指定

## 命名约定
{从模板加载，结合代码库实际情况调整}

## 目录结构约定
{从代码库推断或使用模板默认值}

## 代码格式化
{自动检测: prettier/eslint/biome 等，配置文件位置}

## 语言/框架特定规范
{从模板加载的特定规范}

## 禁止事项
{从模板加载 + 从代码库反模式推断}
```

### Step 6: 生成 AGENTS.md

在**项目根目录**（不是 wiki/ 下）创建 `AGENTS.md`:

**生成策略**:

1. 加载 Step 4 选中的语言/框架模板中的 `agents-sections.md`
2. 合并模板内容与项目实际信息
3. 生成完整的 AGENTS.md

**模板合并逻辑**:

```
基础模板 (languages/typescript/agents-sections.md)
    +
框架模板 (frameworks/react/agents-sections.md)  [可选]
    +
项目实际信息 (package.json, README 等)
    =
最终 AGENTS.md
```

**输出格式**:

```markdown
# {项目名} - AI 编程助手指引

## 项目概述
{自动检测: package.json name / README 第一行 / git remote}

## 技术栈
{从 Step 4 检测结果填充}

## 关键约定
{从模板加载 + 代码库推断}
> 详细规范见 [codestyle.md](./codestyle.md)

## 常用命令
{从模板加载 + package.json scripts}

## 工作流入口
使用 `/dev` 开始工作流，它会根据你的意图路由到正确的技能。

可用技能:
- **init** — 项目初始化，生成骨架
- **req** — 需求收集与分析
- **arch** — 架构设计与技术决策
- **roadmap** — 大需求拆解与规划
- **feat** — 特性设计、实现与验收
- **issue** — 问题诊断与修复
- **review** ★ — 五轴代码审查（正确性/安全/性能/可维护性/测试）
- **security** ★ — 三层边界安全检查
- **ship** ★ — 发布部署（git规范/CI-CD门禁/灰度发布/回滚）
- **kb** — 知识沉淀与复用

工具脚本位于 `wiki/tools/`，在项目根目录下运行。

★ = 质量保障环节

## 文档索引
(首次使用各技能后自动填充)

### 需求
(无)

### 架构
(无)

### 路线图
(无)

### 进行中的特性
(无)

### 已解决的问题
(无)

### 知识库
(无)

---

最后更新: {当前时间}
模板来源: {language}/{framework} | 由 init 技能生成
```

**AGENTS.md 维护规则**:
- 各技能输出新文档后，自动更新对应分类下的索引链接
- 不在此文件中写详细内容，只做索引
- 人和 AI 都可以读

**AGENTS.md 索引校验规则**:

各技能在更新 AGENTS.md 索引后，必须执行以下校验：

| 校验项 | 方法 | 不通过时的处理 |
|--------|------|--------------|
| 链接目标存在 | `existsSync(链接路径)` | 删除无效链接或补充缺失文档 |
| 索引覆盖完整 | Grep `wiki/` 下所有文档的 frontmatter，对比 AGENTS.md 索引 | 补充缺失的索引条目 |
| 无重复条目 | 检查同一文档在 AGENTS.md 中只出现一次 | 合并或去重 |
| 分类正确 | 文档 type 与 AGENTS.md 分类一致 | 修正分类 |

**校验时机**:
- 每次 ship 完成后（发布前最后一次确认）
- 用户显式要求"检查索引"时
- init 重新运行时（全量校验）

### Step 7: 验证

确认以下条件全部满足：
- [ ] `wiki/` 及其所有子目录已创建
- [ ] `wiki/tools/` 下有 `validate-yaml.mjs`、`review-generate.mjs` 和 `read-yaml.mjs`
- [ ] 项目根目录有 `.gitignore`（包含 dev-skills 工作流忽略规则）
- [ ] 项目根目录有 `codestyle.md`（或 AGENTS.md 中已引用）
- [ ] 项目根目录有 `AGENTS.md`（关键约定章节引用 codestyle.md）
- [ ] 运行 `ls wiki/` 能看到完整目录树

## 与其他技能的关系

| 场景 | 动作 |
|------|------|
| init 完成 | → 用户可开始用 `/dev` 进入正常工作流 |
| 缺失目录 | → 重新运行 init 补充 |

## 注意事项

- **不覆盖已有文件**: 如果 wiki/ 下已有文档，只补缺目录和文件
- **不删除任何内容**: 只创建，不清理
- **AGENTS.md 只生成一次**: 后续由各技能增量更新索引部分
- **.gitignore 增量追加**: 已存在时只追加 `dev-skills 工作流` 段落条目，不修改其他规则
- **codestyle.md 智能生成**: 有代码库时自动推断风格；全新项目生成模板；已存在时不覆盖
