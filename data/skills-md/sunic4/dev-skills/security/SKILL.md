---
name: "security"
description: "安全加固与漏洞预防。OWASP Top 10 防范、认证授权模式、密钥管理、依赖审计。作为嵌入式检查点在 feat-impl/review/ship 中触发，也可独立调用。"
---

# Security - 安全加固

## 职责
**安全不是可选的质量属性 — 它是每个代码变更的内建检查点。**

## 触发方式

### 方式 A: 嵌入式触发（主要）— 在其他流程中自动执行

| 触发时机 | 来源技能 | 强制等级 | 说明 |
|---------|---------|---------|------|
| feat-impl 写完敏感代码后 | feat | **必须** | 涉及 auth/input/crypto/API 时 |
| review Axis 2 安全审查 | review | **必须** | 每个 review 都执行 |
| ship 发布前最终检查 | ship | **必须** | 发布门禁之一 |
| arch 设计涉及安全架构 | arch | **应做** | auth/权限/加密相关设计 |

### 方式 B: 显式调用
- 用户要求"安全检查"/"security audit"/"漏洞扫描"
- 接入新依赖或第三方服务前
- 处理用户数据的功能开发前

## 三层边界系统

```
┌─────────────────────────────────────────┐
│         Layer 3: Infrastructure          │
│   依赖审计 / 密钥管理 / 网络安全 / 日志   │
├─────────────────────────────────────────┤
│         Layer 2: Application             │
│   认证授权 / 会话管理 / 加密存储 / CORS  │
├─────────────────────────────────────────┤
│         Layer 1: Input/Output            │
│   输入验证 / 输出编码 / XSS / 注入防护   │
└─────────────────────────────────────────┘
```

**从 Layer 1 到 Layer 3 逐层检查，外层不通则内层不必查。**

## 检查清单（按场景）

### 场景 A: 用户输入处理（Layer 1）

| # | 检查项 | 通过标准 | 常见漏洞 |
|---|--------|---------|---------|
| A1 | 输入长度限制 | 有 max length 校验 | Buffer overflow / DoS |
| A2 | 输入类型校验 | 类型不匹配时 reject 或 coerce | Type confusion |
| A3 | 特殊字符转义 | HTML/SQL/命令注入字符已转义 | XSS / SQLi / RCE |
| A4 | 白名单优先 | 允许的值列表优于黑名单过滤 | Bypass via encoding |
| A5 | 文件上传限制 | 类型+大小+内容三重校验 | Malicious upload |

### 场景 B: 认证与授权（Layer 2）

| # | 检查项 | 通过标准 | 常见漏洞 |
|---|--------|---------|---------|
| B1 | 密码存储 | bcrypt/scrypt/argon2，**绝不明文** | Credential theft |
| B2 | Token 安全 | JWT 有过期时间 + 签名验证 | Token forgery |
| B3 | 会话管理 | 登出后 session 失效，idle timeout | Session hijacking |
| B4 | 权限检查 | 每个端点都验证权限，不只靠前端 | IDOR / privilege escalation |
| B5 | Rate limiting | 认证端点 + 敏感操作有频率限制 | Brute force |
| B6 | OAuth/第三方 | state 参数验证 + CSRF protection | OAuth hijacking |

### 场景 C: 数据处理（Layer 2）

| # | 检查项 | 通过标准 | 常见漏洞 |
|---|--------|---------|---------|
| C1 | 敏感数据日志 | 无密码/token/PII 出现在日志中 | Info leakage |
| C2 | 数据加密传输 | 全站 HTTPS，无 mixed content | MitM |
| C3 | 数据加密存储 | PII 至少 AES-256 at rest | Data breach |
| C4 | 错误信息 | 不泄露内部堆栈/路径/DB 结构给用户 | Info leakage |
| C5 | SQL 查询 | 参数化查询，**绝无字符串拼接** | SQL injection |

### 场景 D: 前端安全（Layer 1）

| # | 检查项 | 通过标准 | 常见漏洞 |
|---|--------|---------|---------|
| D1 | CSP 策略 | 有 Content-Security-Policy 头 | XSS mitigation |
| D2 | DOM 操作 | innerHTML 使用 sanitized 输入 | DOM-based XSS |
| D3 | 跳转链接 | 用户可控 URL 做 allowlist 校验 | Open redirect |
| D4 | 本地存储 | token 不存 localStorage（用 httpOnly cookie） | Token theft |
| D5 | 依赖完整性 | script tag 有 integrity 属性 | Supply chain attack |

### 场景 E: 基础设施与依赖（Layer 3）

| # | 检查项 | 通过标准 | 常见漏洞 |
|---|--------|---------|---------|
| E1 | 依赖版本锁定 | package.json + lockfile 一致 | Dependency confusion |
| E2 | 已知漏洞扫描 | npm audit / Snyk 无 high/critical | Known CVE |
| E3 | 密钥管理 | 无硬编码密钥；使用环境变量或密钥服务 | Secret leakage |
| E4 | CORS 配置 | 不允许 wildcard origin | Cross-origin attack |
| E5 | 环境隔离 | dev/staging/prod 配置分离 | Accidental prod access |

## 评分与输出

每次安全检查输出：

```yaml
# security-check.yaml (附加到目标文档目录)
meta:
  target: "{feature_id or file_path}"
  checked_at: "YYYY-MM-DDTHH:MM"
  checker: "security-agent"

layers_checked:
  - layer_1_input: { passed: true, findings: [] }
  - layer_2_application: { passed: true, findings: [] }
  - layer_3_infrastructure: { passed: false, findings: [...] }

verdict: pass | pass_with_warnings | fail | waived
critical_findings: []
waiver_reason: null
```

**输出位置规则**:

| 触发场景 | 输出路径 | 说明 |
|---------|---------|------|
| feat-impl 嵌入式触发 | `wiki/features/{slug}/security-check.yaml` | 附加到当前 feature 目录 |
| review Axis 2 嵌入式触发 | 合并到 `review-report.yaml` 的 axes.security 章节 | 不生成独立文件 |
| ship Step 2 门禁 | `wiki/features/{slug}/security-check-final.yaml` | 发布前最终检查，与 impl 检查分开 |
| 独立调用(有明确目标) | `wiki/features/{slug}/security-check.yaml` 或 `wiki/issues/{slug}/security-check.yaml` | 根据目标类型决定 |
| 独立调用(无明确目标) | `wiki/security-audit-{YYYYMMDD}.yaml` | 项目根 wiki/ 下 |

**命名规则**: 文件名始终为 `security-check.yaml`（或 `security-check-final.yaml` 用于发布门禁），放在目标文档的同级目录下。

**verdict 判定**:
- **pass**: 全部通过 → 继续
- **pass_with_warnings**: 有 fyi/optional 级别 → 记录，继续
- **fail**: 有 must 级别 → **阻止合并/发布**
- **waived**: 有 must 但有充分理由豁免 → 记录 waiver 原因 + 过期时间

## OWASP Top 10 映射

| OWASP 2021 | 对应检查项 | Layer |
|------------|-----------|-------|
| A01 Broken Access Control | B4 权限检查 | L2 |
| A02 Cryptographic Failures | B1 密码/C2 加密/C3 Token | L2 |
| A03 Injection | A3 转义/C5 SQL参数化 | L1 |
| A04 Insecure Design | 架构阶段安全 review | L2 |
| A05 Security Misconfiguration | E4 CORS/E5 环境隔离 | L3 |
| A06 Vulnerable Components | E1 依赖锁/E2 漏洞扫描 | L3 |
| A07 Auth Failures | B1-B6 全部 | L2 |
| A08 Software/Data Integrity | D5 依赖完整性 | L1 |
| A09 Logging/Monitoring Failures | C1 敏感日志 | L2 |
| A10 SSRF | A5 文件上传/D3 跳转 | L1 |

## Anti-Rationalization

| "借口" | 反驳 |
|--------|------|
| "这是内部系统，不需要安全检查" | 内部系统往往是攻击者的第一跳板 |
| "后面再加安全" | 安全无法事后补丁，必须在设计时就内建 |
| "框架已经处理了" | 框架提供工具，但不会自动正确使用 |
| "性能优先，安全其次" | 一个漏洞可以让所有性能优化归零 |
| "这个功能太小不值得" | 最小的功能也可能成为攻击面 |

## Red Flags

- ⚠️ 代码中有 `eval()` / `innerHTML` / `dangerouslySetInnerHTML` → 必须替换或 sanitize
- ⚠️ 正则表达式含用户输入且未锚定 → ReDoS 风险
- ⚠️ `console.log(data)` 其中 data 来自用户 → 信息泄漏
- ⚠️ 硬编码密码/API key/secret → 必须移除
- ⚠️ 关闭了 ESLint/TypeScript 的安全相关 rule → 必须重新开启
