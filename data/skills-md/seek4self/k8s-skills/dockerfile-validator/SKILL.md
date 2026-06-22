---
name: dockerfile-validator
description: 验证、检查、审计或扫描 Dockerfile，检查安全问题和最佳实践。
---

# Dockerfile 验证器

使用确定性阶段、清晰的严重程度报告和明确的回退方案验证 Dockerfile，以应对工具或网络访问受限的情况。

## 触发短语

当用户要求执行以下任务时使用此技能：
- "验证此 Dockerfile"
- "检查我的 Dockerfile"
- "安全扫描 Dockerfile"
- "优化 Docker 镜像大小/构建时间"
- "在合并前审查 Dockerfile"
- "查找 Dockerfile.prod/Dockerfile.dev 中的问题"

## 使用/不使用

将此技能用于：
- 语法和检查验证
- 安全和密钥检查
- 最佳实践和性能审查
- CI/CD 或生产前的 Dockerfile 加固

不要将此技能用于：
- 从头生成新的 Dockerfile（使用 `dockerfile-generator`）
- 运行容器、调试运行时行为或镜像仓库操作

## 此技能中的本地文件

- 验证器脚本：`scripts/dockerfile-validate.sh`
- 参考：
  - `references/security_checklist.md`
  - `references/optimization_guide.md`
  - `references/docker_best_practices.md`
- 示例 Dockerfile：`examples/*.Dockerfile`

## 确定性执行流程（必需）

按顺序运行这些步骤。除非有记录的回退分支适用，否则不要跳过步骤。

### 1. 预检和路径设置

假设仓库根目录为工作目录：

```bash
cd /path/to/repo
SKILL_DIR="devops-skills-plugin/skills/dockerfile-validator"
TARGET_DOCKERFILE="Dockerfile"   # 用户提供路径时替换
```

在运行工具之前验证输入：

```bash
test -f "$SKILL_DIR/scripts/dockerfile-validate.sh"
test -f "$TARGET_DOCKERFILE"
```

如果任一检查失败，停止并报告确切缺少的路径。

### 2. 显式读取目标 Dockerfile

使用显式文件读取命令（不是抽象的"读取工具"措辞）：

```bash
sed -n '1,220p' "$TARGET_DOCKERFILE"
```

对于长文件如果需要：

```bash
sed -n '220,440p' "$TARGET_DOCKERFILE"
```

### 3. 运行验证脚本

主要命令：

```bash
bash "$SKILL_DIR/scripts/dockerfile-validate.sh" "$TARGET_DOCKERFILE"
```

用于结构化报告的可选捕获运行：

```bash
bash "$SKILL_DIR/scripts/dockerfile-validate.sh" "$TARGET_DOCKERFILE" | tee /tmp/dockerfile-validator.out
```

### 4. 按严重程度分类发现（标准）

使用此标准严重程度模型：

- `严重`
  - 硬编码的密钥/凭证
  - 高风险上下文中的显式 root 运行时
  - 高影响安全策略失败
- `高`
  - Checkov 容器加固失败
  - 可能导致不安全/不可靠构建的 hadolint 错误
  - 缺少或不安全的运行时用户姿态（`USER`）
- `中`
  - `:latest` 镜像标签、缺少固定、缓存清理遗漏
  - 构建缓存低效和分层安装反模式
- `低`
  - 样式/信息指导和非阻塞优化建议

### 5. 无问题快速路径（必需）

如果验证没有可操作的发现：
- 返回简洁的通过摘要。
- **不要**打开参考文件。
- **不要**生成修复差异。

当以下所有条件都为真时使用快速路径：
- 脚本报告整体通过。
- 没有安全失败。
- 没有需要用户操作的错误/警告发现。

### 6. 参考加载规则（仅当发现存在时）

仅读取与实际问题匹配的参考。每个必需文件只读取一次。

问题到参考映射：

| 问题类别 | 触发示例 | 读取此文件 |
|---|---|---|
| 密钥、root 用户、暴露的敏感端口、加固缺口 | `CKV_DOCKER_*`、硬编码的 token/密码、root 运行时 | `references/security_checklist.md` |
| 镜像大小、层数、多阶段机会、缓存效率、`.dockerignore` 缺口 | 太多 `RUN`、带构建依赖的单阶段、缓存未命中 | `references/optimization_guide.md` |
| 标签固定、指令使用、COPY vs ADD、WORKDIR/CMD/ENTRYPOINT 约定 | `:latest`、未固定的包、指令级最佳实践 | `references/docker_best_practices.md` |

显式读取命令：

```bash
sed -n '1,220p' "$SKILL_DIR/references/security_checklist.md"
sed -n '1,220p' "$SKILL_DIR/references/optimization_guide.md"
sed -n '1,220p' "$SKILL_DIR/references/docker_best_practices.md"
```

用于目标提取：

```bash
rg -n "USER|secrets|EXPOSE|HEALTHCHECK" "$SKILL_DIR/references/security_checklist.md"
rg -n "multi-stage|cache|layer|dockerignore" "$SKILL_DIR/references/optimization_guide.md"
rg -n "FROM|COPY|ADD|WORKDIR|CMD|ENTRYPOINT|latest" "$SKILL_DIR/references/docker_best_practices.md"
```

### 7. 生成标准报告输出

对每个非快速路径运行使用此模板：

```markdown
## Dockerfile 验证报告
- 目标：<path>
- 命令：`bash <skill-script> <target>`
- 整体结果：PASS | FAIL | PARTIAL（回退）

### 严重
- <问题或 `无`>

### 高
- <问题或 `无`>

### 中
- <问题或 `无`>

### 低
- <问题或 `无`>

### 建议修复
- <每个可操作问题的具体代码级修复>

### 使用的参考
- <仅列出实际读取的文件>

### 使用的回退
- `无` 或确切的回退分支 + 原因
```

### 8. 提供修复应用

报告后：
- 询问是否应用修复。
- 如果用户批准，修补 Dockerfile 并重新运行验证。

## 回退行为（显式）

当主脚本无法完成时，使用确定性回退分支并报告它们。

### 回退 A：Python/工具安装约束

条件：
- 脚本以工具安装失败退出（例如 Python 缺失、包安装被阻止或受限环境）。

操作：
1. 报告主失败及其原因。
2. 运行手动最小检查：

```bash
# 基本语法信号（如果 Docker 可用）
DOCKERFILE_DIR="$(dirname "$TARGET_DOCKERFILE")"
docker build --no-cache -f "$TARGET_DOCKERFILE" "$DOCKERFILE_DIR"

# 高价值静态检查
grep -nEi "^[[:space:]]*FROM[[:space:]]+.*:latest" "$TARGET_DOCKERFILE" || true
grep -nEi "^[[:space:]]*(ENV|ARG)[[:space:]].*(password|secret|token|api[_-]?key)[[:space:]]*=" "$TARGET_DOCKERFILE" || true
grep -nEi "^[[:space:]]*USER[[:space:]]+(root|0(:0)?)$" "$TARGET_DOCKERFILE" || true
grep -nEi "^[[:space:]]*HEALTHCHECK[[:space:]]+" "$TARGET_DOCKERFILE" || true
```

3. 使用 `PARTIAL` 结果对输出进行分类并清晰标记跳过的检查。

### 回退 B：hadolint 不可用但 Docker 可用

使用 hadolint 容器镜像：

```bash
docker run --rm -i hadolint/hadolint < "$TARGET_DOCKERFILE"
```

### 回退 C：没有 Docker，没有 hadolint/checkov

仅运行手动基于正则表达式的检查（回退 A 步骤 2），清晰标记为 `PARTIAL`，并说明哪些扫描器被跳过。

## 快速命令集

### 验证一个 Dockerfile

```bash
cd /path/to/repo
bash devops-skills-plugin/skills/dockerfile-validator/scripts/dockerfile-validate.sh Dockerfile
```

### 验证替代文件

```bash
cd /path/to/repo
bash devops-skills-plugin/skills/dockerfile-validator/scripts/dockerfile-validate.sh Dockerfile.prod
```

### 验证技能示例

```bash
cd /path/to/repo/devops-skills-plugin/skills/dockerfile-validator
bash scripts/dockerfile-validate.sh examples/good-example.Dockerfile
bash scripts/dockerfile-validate.sh examples/security-issues.Dockerfile
```

### 运行回归检查（CI 入口点）

```bash
cd /path/to/repo
bash devops-skills-plugin/skills/dockerfile-validator/scripts/test_validate.sh
```

必须强制执行 ShellCheck 的 CI 环境的可选严格模式：

```bash
STRICT_SHELLCHECK=true bash devops-skills-plugin/skills/dockerfile-validator/scripts/test_validate.sh
```

## 渐进式披露规则

- 始终首先读取目标 Dockerfile。
- 除非发现需要，否则不要读取任何参考文件。
- 仅从问题到参考映射中读取匹配的参考文件。
- 除非出现新的问题类别，否则不要重新读取相同的参考。

## 完成标准

仅当满足以下所有条件时，才认为此技能执行完成：

- 触发匹配 Dockerfile 验证/检查/安全/优化请求。
- 目标 Dockerfile 路径已显式验证。
- 已执行验证命令（或显式回退）。
- 使用严重程度桶（`严重`、`高`、`中`、`低`）报告发现。
- 参考使用与问题类别匹配并已显式列出。
- 无问题快速路径跳过了不必要的参考读取。
- 如果应用了修复，已重新运行验证并报告最终状态。

## 资源

- 脚本：`scripts/dockerfile-validate.sh`
- CI/回归入口点：`scripts/test_validate.sh`
- 安全参考：`references/security_checklist.md`
- 优化参考：`references/optimization_guide.md`
- 最佳实践参考：`references/docker_best_practices.md`
- 示例：`examples/good-example.Dockerfile`、`examples/bad-example.Dockerfile`、`examples/security-issues.Dockerfile`、`examples/python-optimized.Dockerfile`、`examples/golang-distroless.Dockerfile`

## 源链接

- [Docker 构建最佳实践](https://docs.docker.com/build/building/best-practices/)
- [Dockerfile 参考](https://docs.docker.com/reference/dockerfile/)
- [Checkov Dockerfile 扫描](https://www.checkov.io/7.Scan%20Examples/Dockerfile.html)
- [hadolint](https://github.com/hadolint/hadolint)
