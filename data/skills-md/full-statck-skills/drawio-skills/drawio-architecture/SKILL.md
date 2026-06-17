---
name: drawio-architecture
description: Provides comprehensive guidance for draw.io architecture diagrams including diagram creation, shapes, templates, and collaboration. Use when the user asks about draw.io architecture, needs to create architecture diagrams, design system diagrams, or collaborate on diagrams.
license: Complete terms in LICENSE.txt
---

## When to use this skill

Use this skill whenever the user wants to:
- 用 Draw.io 画系统架构图、部署图、组件图
- 产出可导出的矢量/PNG 图用于文档或评审
- 协作编辑与版本管理（如 Confluence、Git 存 .drawio）

## How to use this skill

1. **工具**：Draw.io 桌面版或 diagrams.net；支持 .drawio XML、导出 PNG/SVG/PDF。
2. **内容**：从模板或形状库选（C4、UML、云组件）；用泳道/容器表达层次。
3. **协作**：存到 Confluence、Google Drive 或仓库；约定命名与图例。

## Best Practices

- 一图一主题；用标题与图例说明符号含义。
- 保持风格统一（颜色、字体、箭头）；复杂系统用多图分层。
- 导出时选合适分辨率；文档中引用时注明“架构图”与更新日期。

## Keywords

draw.io, architecture diagram, C4, deployment diagram, 架构图, 部署图, diagrams.net

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
