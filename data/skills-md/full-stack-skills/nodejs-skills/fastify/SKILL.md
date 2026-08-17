---
name: fastify
description: Provides comprehensive guidance for Fastify framework including routing, plugins, schemas, hooks, and performance optimization. Use when the user asks about Fastify, needs to create high-performance Node.js applications, implement Fastify plugins, or optimize API performance.
license: Complete terms in LICENSE.txt
---

## When to use this skill

Use this skill whenever the user wants to:
- 用 Fastify 编写高性能 Node.js HTTP 服务、 schema 校验与插件
- 配置路由、序列化、日志与 TypeScript

## How to use this skill

1. **核心**：fastify()、get/post、request/reply；schema 与 serialization；插件与装饰器。
2. **进阶**：@fastify/cors、formbody、static；类型与 async/await。
3. **参考**：https://fastify.dev/docs/latest/

## Best Practices

- schema 定义请求响应；插件封装与顺序。
- 生产用日志与错误处理；性能与安全头。

## Keywords

fastify, Node.js, 高性能, schema

## 能力边界

### ✅ 适用场景
- 当你需要使用此技能对应的技术栈时
- 当项目需要遵循最佳实践时
- 当需要快速上手或深入理解核心概念时

### ⚠️ 需要注意
- 复杂业务逻辑需要结合具体场景调整
- 性能优化需要根据实际数据量评估

### ❌ 不适用场景
- 不相关的技术栈或框架
- 需要完全自定义的特殊场景

## 常见陷阱 (Gotchas)

1. **版本兼容性**：注意框架版本与依赖库的兼容性，不同版本 API 可能有差异
2. **配置文件格式**：配置文件格式错误是最常见的问题，建议使用编辑器的语法检查
3. **环境变量**：确保所有必要的环境变量已正确设置，敏感信息不要硬编码
4. **依赖冲突**：多版本共存时注意依赖冲突，使用 lock 文件锁定版本
5. **性能陷阱**：大数据量场景下注意性能优化，避免 N+1 查询等常见问题

## 使用流程

### Step 1: 环境准备
确保开发环境已安装必要的依赖和工具。

### Step 2: 配置初始化
根据项目需求进行基础配置。

### Step 3: 核心功能使用
按照示例代码实现核心功能。

### Step 4: 测试验证
运行测试确保功能正常。

### Step 5: 部署上线
完成开发后进行部署和监控。
