---
name: better-auth-integration
description: 在 TanStack Start + Drizzle ORM + PostgreSQL 项目中集成 Better Auth 认证，支持邮箱登录与 GitHub/Google OAuth
---

# Better Auth Integration Skill

## 何时激活

- 用户要在 TanStack Start 项目接入认证
- 用户要复刻 better-auth 登录注册与 OAuth 流程
- 用户要把现有认证迁移到 better-auth
- 用户反馈登录、注册、OAuth 出现 4xx/5xx 或回调异常

## 执行协议

按固定顺序执行并维护 todo 状态：

- Phase 1 探索：先确认项目结构与现状，禁止跳过
- Phase 2 安装：补齐依赖与环境变量
- Phase 3 Schema：校正数据库表结构与字段类型
- Phase 4 实现：落地 5 个核心文件
- Phase 5 验证：启动与接口联调验证

## Phase 1 探索

目标：防止覆盖已有实现，先摸清目标项目

- 检查清单见 [phase-1-exploration-checklist.md](references/phase-1-exploration-checklist.md)
- 输出要求：
  - 框架、ORM、数据库驱动版本结论
  - schema 文件组织方式结论
  - 环境变量读取方式结论
  - 是否已有 better-auth 相关文件结论

## Phase 2 安装

目标：安装认证所需依赖并补齐 env

- 安装命令见 [phase-2-install-commands.sh](references/phase-2-install-commands.sh)
- 环境变量模板见 [.env.example](references/env/.env.example)
- 输出要求：
  - 依赖安装完成
  - BETTER_AUTH_SECRET 与 VITE_APP_URL 已配置

## Phase 3 Schema

目标：确保 better-auth 托管表与业务外键兼容

关键约束：所有 better-auth 托管表的 id 及关联 user_id 必须使用 text，不可使用 uuid

- 单文件 schema 示例见 [schema-single-file.ts](references/schema/schema-single-file.ts)
- 按表拆分 schema 示例见 [users_table.ts](references/schema/split/users_table.ts)
- schema 聚合导出见 [index.ts](references/schema/split/index.ts)
- 业务表外键类型要求见 [business-fk-rules.md](references/schema/business-fk-rules.md)

如果项目已有 uuid 历史数据：

- 迁移 SQL 见 [uuid-to-text.sql](references/migrations/uuid-to-text.sql)

## Phase 4 实现

目标：完成服务端、路由、客户端、env、hook 五类核心文件

- 服务端实例示例见 [auth.ts](references/core-files/auth.ts)
- 服务端导出见 [better-auth-index.ts](references/core-files/better-auth-index.ts)
- API 路由示例见 [route-api-auth-dollar.ts](references/core-files/route-api-auth-dollar.ts)
- 客户端 SDK 示例见 [auth-client.ts](references/core-files/auth-client.ts)
- 客户端导出见 [auth-client-index.ts](references/core-files/auth-client-index.ts)
- 服务端 env schema 示例见 [envSchema.ts](references/core-files/envSchema.ts)
- useAuth hook 示例见 [useAuth.ts](references/core-files/useAuth.ts)

实现约束：

- API 路由必须使用静态 import，禁止动态 import
- auth 适配器 schema 字段名必须与实际表定义一致
- trustedOrigins 在开发环境需覆盖 localhost 多端口

## Phase 5 验证

目标：验证认证链路可用并可定位问题

- 验证步骤见 [phase-5-verification.md](references/phase-5-verification.md)
- 一键验证脚本见 [phase-5-verify-auth.sh](references/phase-5-verify-auth.sh)

## 常见问题与定位

- 踩坑速查见 [pitfalls.md](references/troubleshooting/pitfalls.md)
- 架构流转说明见 [flow.md](references/architecture/flow.md)

## 参考实现映射

- 参考路径索引见 [reference-paths.md](references/reference-paths.md)

## 交付标准

- 主 SKILL 文档只保留协议、流程、约束与链接入口
- 所有代码、命令、SQL、env 内容均放到 references 独立文件
- 新增内容保持职责单一，避免重复与跨文件混杂
