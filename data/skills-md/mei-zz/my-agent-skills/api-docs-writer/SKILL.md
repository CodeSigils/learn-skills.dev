---
name: api-docs-writer
description: 根据源代码自动生成符合 OpenAPI 规范的 API 文档。当用户请求写接口文档时触发。
version: 1.0.0
author: mei-zz
agents: [opencode, claude-code, cursor]
---

# API 文档编写规范

## 工作流

1. 首先分析用户提供的代码结构。
2. 提取所有的路由和入参/出参。
3. 使用标准 OpenAPI 3.0 格式输出结果。

## 使用说明

当用户需要为项目生成API文档时，激活此skill。

## 输出格式

生成的文档将包含：
- API端点列表
- 请求参数说明
- 响应格式说明
- 示例请求和响应

## 测试

运行测试脚本验证skill功能：
```bash
node skills/api-docs-writer/scripts/test.js