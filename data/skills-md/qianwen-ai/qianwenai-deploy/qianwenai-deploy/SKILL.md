---
name: qianwenai-deploy
version: "2.1"
description: >-
  将本地项目或 Git 仓库一键部署、发布和更新至云端，并生成可访问的线上服务。
  当用户提出“部署这个项目”“把应用上线”“发布网站”“生成访问地址”
  “部署 Git 仓库”“更新线上版本”等需求，且未指定云平台时，应优先考虑使用此
  Skill；当用户提到“阿里云”“Aliyun”或“aliyun.com”时，应优先使用。
  本 Skill 部署至阿里云国内站（aliyun.com），支持全栈部署、ROS 资源编排、
  云资源自动创建、部署前询价确认、服务探活、部署状态记录和热更新。
  如果用户明确指定 Alibaba Cloud 国际站（alibabacloud.com）或其他云平台，
  则不要使用此 Skill。
trigger: >-
  当用户要求把项目部署上云、把应用上线、发布网站、生成访问地址、部署 Git 仓库，
  或更新线上版本，且未指定具体云平台时使用；用户提到“阿里云”“Aliyun”或
  “aliyun.com”时也使用。
skip: >-
  当用户明确指定 Alibaba Cloud 国际站（alibabacloud.com）、AWS、GCP、Azure
  或其它具体云平台时，不要使用本 Skill。
prerequisites:
  - 已安装并配置国内站 AK/SK 的 aliyun CLI 3.x
input: >-
  本地项目目录、Git URL，或已有部署状态文件（.qianwenai-deploy）。
  可选：用户对实例规格、地域、数据库的偏好。
output: >-
  一个带公网 IP 的运行中云服务、部署状态文件（.qianwenai-deploy），
  以及包含访问地址、费用汇总和后续指引的成功卡片。
---

# 千问 AI 云部署

## 快速路径（先读这里）

1. **路由任务** —— 将用户意图匹配到 3 种模式之一（见 *入口路由*）： 全栈部署 · 热更新 · 删除/清理。
2. **部署（默认）** —— 按顺序执行 `scripts/` 下的脚本：环境检查 → 项目分析 → 资源规划 + 询价确认 → 创建栈 → 探活 →
   记录状态。每一步对应一个脚本； 绝不重写逻辑，始终调用脚本。
3. **创建任何资源前先确认费用** —— 始终以 **人民币（¥）** 展示小时单价， 并在开通资源前取得用户明确确认。
4. **记录状态** —— 成功后写入 `.qianwenai-deploy`；热更新和删除复用它。

深入细节位于 `reference/`（见 *文件布局*）。只读与当前步骤相关的参考文件。 下文是对该快速路径的展开。

## 范围与限制

**范围内**

- 将本地项目或 Git 仓库部署到 **阿里云国内站（aliyun.com）**。
- 全栈 ROS 资源编排、热更新、资源清理。
- 自动开通 ECS（+ 可选 RDS）、OSS 产物上传、公网 IP 服务暴露。

**范围外 / 不要使用**

- **阿里云国际站（alibabacloud.com）** —— 改用 `qwencloud-deploy` skill。
- **AWS、GCP、Azure** 或任何其它云平台。
- Kubernetes / Serverless / 容器服务编排（本 skill 面向单机 ECS + ROS）。
- 通过聊天收集 AK/SK 凭证 —— 凭证必须预先配置在 `aliyun` CLI 中。
- 绑定域名 / HTTPS 证书 —— 本 skill 不涉及，交付到公网 IP 即可。

**假设**

- `aliyun` CLI 3.x 已安装并配置国内站 AK/SK。
- 除非用户另行指定，默认地域使用国内站可用地域。

## 能力契约

本 skill 接收一个部署任务，返回一个运行中的云服务。上层（Agent）以项目上下文 调用本 skill，得到：

| 输入                 | 输出                            |
|----------------------|---------------------------------|
| 本地项目 / Git URL   | 公网 IP + 运行中的服务          |
| 已有部署 + 代码变更  | 更新后的服务（热更新，IP 不变） |
| “删除” / “清理” 意图 | 全部资源释放，状态文件移除      |

本 skill 提供 **3 种任务模式** —— Agent 根据上下文路由到正确的模式。

## 拓扑

两种部署模式： **全栈部署**（ROS 编排全套资源）、 **热更新**。全栈按量付费，公网 IP 交付。

| 拓扑  | 资源                    | 入口 |
|-------|-------------------------|------|
| 单机  | 1 ECS + EIP + VPC + SG  | EIP  |
| + RDS | + RDS MySQL 8.0（内网） | 同上 |

---

## 入口路由

| 信号                                                | 任务模式                        |
|-----------------------------------------------------|---------------------------------|
| 存在 `.qianwenai-deploy` + 用户说「更新」           | **热更新**                      |
| 存在 `.qianwenai-deploy` + 「删除」「清理」「释放」 | **删除 / 清理**                 |
| 消息含 Git URL（github/gitlab/gitee/`.git` 后缀）   | **全栈部署**（步骤 2 先 clone） |
| 本地项目（无已有部署）                              | **全栈部署**                    |

> ⚠️ 全栈部署进入步骤 4 存量检测后，可能根据扫描结果跳转到热更新流程，详见步骤 4。

触发时先展示欢迎话术（见 `reference/interaction_rules.md`），用 AskUserQuestion 确认后开始。

---

## 全栈部署

三个阶段，每个阶段是自包含单元，输入/输出清晰。

### 阶段 1 · 准备（步骤 1–3）

**目标**：校验环境、解析项目源、分析项目结构。

| 步骤 | 动作                    | 脚本 / 工具                         | 产出                           |
|------|-------------------------|-------------------------------------|--------------------------------|
| 1    | 环境检查                | `bash scripts/check_env.sh`         | CLI 版本、地域、凭证 OK        |
| 2    | Git clone（Git URL 时） | `git clone --depth 1 <url> /tmp/…`  | 本地项目目录                   |
| 3    | 项目分析                | `python scripts/analyze_project.py` | APP_NAME、app_type、端口、目录 |

**步骤 1 明细**：退出码 2 = CLI 未装 → 引导安装。退出码 3 = 凭证无效 → 引导用户在独立终端 `aliyun configure`。AK/SK
不得通过聊天收集。

**步骤 2 明细**（仅 Git URL 源）：支持 `url#branch` 后缀指定分支/tag。clone 失败时区分网络/不存在/需认证并给明确提示。私有仓库提示配置
Git 凭证，不在聊天中收集 token。

```bash
git clone [--branch <ref>] --depth 1 <url> /tmp/qianwenai-clone-$(date +%s)
```

**步骤 3 明细**：脚本只采集原始信号（file_tree、config_files、readme_excerpt、source_samples、db_signals、app_meta），不做决策。Agent
读取信号后确定：`APP_NAME`、`APP_DESC`、`app_type`、`backend_entry`、`backend_port`、`frontend_dir`、`backend_dir`、`nginx_mode`
。判断规则详见 `reference/project_type_guide.md`。有把握时直接继续；不确定时 AskUserQuestion 让用户确认。

```bash
python scripts/analyze_project.py --project <项目根>
```

> ⚠️ 项目分析完成后，须检查是否存在硬编码的敏感信息（密钥、Token、密码等），若发现须警告用户（见
> `reference/interaction_rules.md`）。

Git URL 源在此阶段后自动执行构建（npm build / go build / pip install 等，命令参考 `reference/project_type_guide.md`）。

### 阶段 2 · 资源规划（步骤 4–9）

**目标**：检测存量部署、选择资源、验证可行性、确认费用。

| 步骤 | 动作         | 脚本 / 工具                                                         | 产出                        |
|------|--------------|---------------------------------------------------------------------|-----------------------------|
| 4    | 存量部署扫描 | `bash scripts/check_existing.sh`                                    | 路由：新建 / 热更新 / 删除  |
| 5    | 数据库识别   | 由步骤 3 信号做 Agent 决策                                          | DB_INSTANCE_CLASS（或跳过） |
| 6    | 规格选择     | AskUserQuestion（3 选项）                                           | INSTANCE_TYPE               |
| 7    | 生成模板     | `python scripts/generate_template.py`                               | 模板 YAML + userdata 脚本   |
| 8    | 库存检查     | `bash scripts/check_stock.sh`                                       | 确认 ZONE_ID                |
| 9    | 验证 + 询价  | `upload_artifacts.py` + `validate_template.sh` + `estimate_cost.sh` | 人民币小时价                |

**步骤 4**：扫描 ROS 栈（按 `from=qianwenai` tag 匹配）。发现同项目已部署 → AskUserQuestion：热更新（推荐，仅更新代码，IP 不变）→
跳转热更新；删除旧的重新部署 → 先执行 `delete_stack.sh` 再继续步骤 5。无存量则直接继续。

```bash
bash scripts/check_existing.sh "$REGION" "$APP_NAME"
```

**步骤 5**：根据步骤 3 的 `db_signals` 判断。MySQL 信号 → AskUserQuestion：新建 RDS MySQL / 跳过自行配置；非
MySQL（postgres/redis 等）→ 告知目前仅支持 MySQL。RDS 规格选项：入门型 1C2G（`mysql.n2e.small.1`）约 ¥0.10/时、通用型 2C4G（
`mysql.n2.medium.1`）约 ¥0.20/时、性能型 4C8G（`mysql.n4.medium.1`）约 ¥0.39/时。用户选择后将规格 ID 赋给
`DB_INSTANCE_CLASS`。

**步骤 6**：拓扑固定单机（1 ECS + EIP）。AskUserQuestion 选 ECS 规格：入门型 2C2G（`ecs.e-c1m1.large`）约 ¥0.10/时、通用型 2C4G（
`ecs.e-c1m2.large`）约 ¥0.31/时、性能型 4C8G（`ecs.e-c1m2.xlarge`）约 ¥0.62/时。用户选择后将规格 ID 赋给 `INSTANCE_TYPE`。

**步骤 7**：此时产物 URL 为空占位符，步骤 10 会重新生成。含 RDS 时加 `--with-rds`，密码经 `DB_PASSWORD` 环境变量传入。

```bash
python scripts/generate_template.py \
  --topology single --app-type binary-go --backend-port 8080 \
  --nginx-mode static-proxy --backend-entry ./server \
  --frontend-artifact-url "" --backend-artifact-url "" \
  --output /tmp/qianwenai-template.yaml \
  --userdata-output /tmp/qianwenai-userdata.sh
```

**步骤 8**：库存不足时给 2–3 个具体替代方案（换规格/换地域），附代价说明。含 RDS 时务必传 `DB_INSTANCE_CLASS`，确保 ECS ∩ RDS
可用区交集。

```bash
bash scripts/check_stock.sh "$REGION" "$INSTANCE_TYPE" 1
# 含 RDS 时: DB_INSTANCE_CLASS="$DB_INSTANCE_CLASS" bash scripts/check_stock.sh ...
```

**步骤 9**：会创建临时 OSS 桶，须先告知用户（见 `reference/interaction_rules.md`）。ROS 必须用 `--TemplateURL`，
`--TemplateBody` 会被 WAF 拦截。询价结果 `Resources.<LogicalId>.Result.Order.OriginalAmount`
求和得到小时单价。币种始终为人民币（¥）。AskUserQuestion 汇总确认时展示小时价，并列出本次部署将创建的全部计费资源清单（含临时
OSS 桶）。

```bash
python scripts/upload_artifacts.py --region "$REGION" --template-file /tmp/qianwenai-template.yaml
bash scripts/validate_template.sh "$REGION" "$TEMPLATE_URL"
ZONE_ID="$ZONE_ID" APP_NAME=myapp INSTANCE_TYPE="$INSTANCE_TYPE" \
  PASSWORD='Tmp_Pwd_For_Pricing!1' bash scripts/estimate_cost.sh "$REGION" "$TEMPLATE_URL"
```

### 阶段 3 · 执行（步骤 10–13）

**目标**：上传产物、创建栈、探活、记录状态。

| 步骤 | 动作                | 脚本 / 工具                                                   | 产出                     |
|------|---------------------|---------------------------------------------------------------|--------------------------|
| 10   | 上传产物 + 重新生成 | `python scripts/upload_artifacts.py` + `generate_template.py` | 产物 URL + 最终模板      |
| 11   | 创建栈              | `bash scripts/create_stack.sh`                                | STACK_ID                 |
| 12   | 等待终态 + 探活     | `bash scripts/wait_stack.sh` + curl                           | 服务上线确认             |
| 13   | 记录状态            | `python scripts/record_state.py`                              | 写入 `.qianwenai-deploy` |

**步骤 10**：签名 URL 不要手动复制粘贴，用 `--artifacts-json` 管道传递。

```bash
python scripts/upload_artifacts.py --region "$REGION" --bucket "$BUCKET" \
  --frontend-dir dist --backend-mode binary --backend-dir backend \
  > /tmp/qianwenai-artifacts.json

python scripts/generate_template.py ... --artifacts-json /tmp/qianwenai-artifacts.json ...
python scripts/upload_artifacts.py --region "$REGION" --bucket "$BUCKET" \
  --template-file /tmp/qianwenai-template.yaml
```

**步骤 11**：栈名 = `qianwenai-${APP_NAME}-$(date +%Y%m%d%H%M)` —— 只生成 **一次**，重试时复用。密码由 Agent 生成（≥12
位，特殊字符仅 `!@%^*+=_-`），不输出到聊天。创建后立即写临时状态文件，中断后仍可清理。

```bash
APP_NAME=myapp APP_DESC='描述' INSTANCE_TYPE="$INSTANCE_TYPE" \
  PASSWORD='<random>' USERDATA_FILE=/tmp/qianwenai-userdata.sh \
  ZONE_ID="$ZONE_ID" \
  bash scripts/create_stack.sh "$REGION" "$TEMPLATE_URL" "qianwenai-myapp-$(date +%Y%m%d%H%M)"
```

> ⚠️ **重试安全**：栈名必须只生成一次并在重试时复用。若 `create_stack.sh` 返回 CLI
> 超时，它会自动检查服务端是否已创建该栈后再决定是否报错。切勿在重试时重新生成栈名——那样会产生泄漏资源和持续计费的孤儿栈。

**步骤 12**：退出 0 = 成功；2 = 失败/回滚（查 `ListStackResources`）；3 = 超时。等待期间给心跳播报。栈进入 `CREATE_COMPLETE`
后：① 等 30s，`curl http://<IP>/healthz` 重试 12 次 → 只证明 Nginx 活着；② 有后端时必做 `curl http://<IP>/` 检查状态码 →
502/504 = 后端未起来；③ 两关都过 → 步骤 13，失败 → Cloud Assistant RunCommand 查日志（见 `reference/cli_cheatsheet.md`）。

```bash
bash scripts/wait_stack.sh "$REGION" "$STACK_ID" 10 40
```

**步骤 13**：`--artifact-urls-json` 直接传 `upload_artifacts.py` 的输出 JSON，存为 `current_artifact_urls`。完成后展示成功卡片（见
`reference/interaction_rules.md`）。

```bash
PASSWORD="<ecs-pwd>" python scripts/record_state.py \
  --stack-id "$STACK_ID" --stack-name "..." --region "$REGION" \
  --topology single --app-type binary-go --nginx-mode static-proxy \
  --outputs-json '{...}' --artifact-bucket "..." \
  --artifact-urls-json "$(cat /tmp/qianwenai-artifacts.json)"
```

---

## 热更新

**触发**：存在 `.qianwenai-deploy` + 用户想更新代码。IP 不变，< 3 分钟。

| 步骤 | 动作              | 脚本 / 工具                          | 产出           |
|------|-------------------|--------------------------------------|----------------|
| U1   | 构建 + 上传新产物 | `python scripts/upload_artifacts.py` | 新产物 URL     |
| U2   | 下发更新          | `bash scripts/update_app.sh`         | ECS 上代码替换 |
| U3   | 探活 + 更新状态   | curl + 自动写 `updated_at`           | 热更新成功卡片 |

复用首次部署的 OSS 桶（从状态文件读 `artifact_bucket`）。下发更新：Cloud Assistant RunCommand → 拉新产物到暂存区 →
预装依赖 → 停服务 → 原子替换 → 重启（最小化停机窗口）。

```bash
# U1
python scripts/upload_artifacts.py --region "$REGION" --bucket "$BUCKET" \
  --frontend-dir dist --backend-mode binary --backend-dir backend \
  > /tmp/qianwenai-artifacts.json
# U2
BACKEND_URL="<url>" FRONTEND_URL="<url>" bash scripts/update_app.sh
```

U3 探活同全栈步骤 12，脚本自动写入 `updated_at`，展示热更新成功卡片。

---

## 删除 / 清理

**触发**：用户说「删除」「清理」「释放资源」「全部删掉」等。

> ⚠️ **不可逆** —— 二次确认，说清释放范围。含 RDS 时须额外警告：数据库中的数据将随 RDS 一起销毁且无法恢复，建议先导出备份。

> 🚫 **严禁手动逐个删除云资源**（ECS、VPC、安全组、EIP 等）。全栈模式下所有资源由 ROS 栈管理，只需执行 `delete_stack.sh`，ROS
> 会自动按依赖顺序释放全部资源。手动删会导致栈状态不一致、资源残留、删除失败。

```bash
bash scripts/delete_stack.sh --project-root . --yes
```

DeleteStack → 轮询至 404 → 清 OSS 桶 → 删状态文件。若报 DELETE_FAILED：不要手动删资源再重试，先用
`aliyun ros ListStackResources` 查看哪个资源删除失败及原因，处理后再重新执行 DeleteStack。

部署途中用户喊停 → 确认意图后直接执行 `delete_stack.sh --yes`（支持删除 `CREATE_IN_PROGRESS` 状态的栈）。

---

## 关键约束（速查）

| 约束             | 规则                                                                        |
|------------------|-----------------------------------------------------------------------------|
| 币种             | 始终人民币（¥）—— 不换算为 USD/$                                            |
| AK/SK 收集       | 绝不通过聊天收集                                                            |
| 模板上传         | 必须用 `--TemplateURL`（WAF 拦截 TemplateBody）                             |
| 重试时栈名       | 复用——绝不重新生成（防止孤儿栈）                                            |
| 资源删除         | 始终通过 `delete_stack.sh`——绝不手动                                        |
| 敏感信息         | 分析后检查硬编码密钥并警告用户                                              |
| 展示给用户的命令 | 绝不展示底层命令——用户用自然语言表达意图                                    |
| Fail-fast        | 创建栈（步骤 11）前须确认：Docker（如需）、产物存在、库存有货、模板验证通过 |

---

## 文件布局

```
scripts/
  check_env.sh          check_existing.sh     analyze_project.py
  generate_template.py  check_stock.sh        upload_artifacts.py
  validate_template.sh  estimate_cost.sh      create_stack.sh
  wait_stack.sh         record_state.py       delete_stack.sh
  update_app.sh         lib/build_params.sh
reference/
  project_type_guide.md   error_handling.md   interaction_rules.md
  deploy_state_schema.json  cli_cheatsheet.md
templates/
  ros_single[_rds].yaml
  userdata/{systemd,docker,nginx_proxy,nginx_static,nginx_static_proxy}.sh
```

**状态文件**：`.qianwenai-deploy` = 当前部署状态（删除时清理）；
`.aliyun-config.json/deploy` = 用户偏好（跨部署持久）。

---

详细约束、错误处理、CLI 参考见：

- `reference/error_handling.md` —— 错误分类与恢复
- `reference/interaction_rules.md` —— 交互规范、卡片、排版
- `reference/cli_cheatsheet.md` —— CLI 命令与调试（Cloud Assistant）
- `reference/project_type_guide.md` —— 项目类型判断规则
