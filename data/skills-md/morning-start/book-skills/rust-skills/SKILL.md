---
name: rust-skills
description: Rust 程序设计语言完整技能集，采用元认知框架，涵盖基础语法、所有权系统、泛型 Trait、并发异步、Cargo 包管理等，支持 Layer 1/2/3 三层认知模型
version: 2.0.0
---

# Rust Skills 技能集

## 概述

Rust Skills 是 AI 驱动的 Rust 开发助手，采用**元认知框架**提供领域正确的架构解决方案。不是简单给出表面答案，而是通过认知层级追溯问题根源。

## 元认知框架

三层认知模型帮助 AI 提供更深入的 Rust 问题解答：

- **Layer 3: 领域约束 (WHY)** - 为什么这样设计？领域规则决定设计选择
- **Layer 2: 设计选择 (WHAT)** - 什么设计模式适合？架构决策
- **Layer 1: 语言机制 (HOW)** - 如何用 Rust 实现？语法特性

详细说明见 [references/meta-cognition.md](references/meta-cognition.md)

## 技能架构

```
rust-skills (母技能 v2.0.0)
├── references/                 # 框架文档
│   ├── meta-cognition.md       # 元认知框架
│   ├── architecture.md         # 技能架构
│   └── commands.md            # 命令系统
├── Layer 1: 语言机制          # m01-m07
├── Layer 2: 设计选择          # m09-m15
├── Layer 3: 领域扩展          # domain-*
└── 基础技能                   # rust-*, 13个子技能
```

## 技能地图

### Layer 1: 语言机制 (m01-m07)

| 技能 | 核心问题 | 触发条件 |
|------|---------|---------|
| rust-ownership-skill | 谁应该拥有这个数据? | E0382, move, borrow |
| rust-resource-management-skill | 什么所有权模式适合? | Box, Rc, Arc, RefCell |
| rust-mutability-skill | 为什么数据需要变化? | mut, Cell, E0596 |
| rust-zero-cost-skill | 编译时还是运行时多态? | generic, trait, E0277 |
| rust-type-driven-skill | 如何用类型防止无效状态? | newtype, PhantomData |
| rust-error-handling-skill | 预期失败还是 bug? | Result, panic, ? |
| rust-concurrency-skill | CPU 密集还是 I/O 密集? | async, Send, Sync |

### Layer 2: 设计选择 (m09-m15)

| 技能 | 核心问题 | 触发条件 |
|------|---------|---------|
| rust-domain-design-skill | 这个概念扮演什么角色? | DDD, entity |
| rust-performance-skill | 瓶颈在哪里? | benchmark, profiling |
| rust-ecosystem-skill | 哪个 crate 适合? | crate selection |
| rust-lifecycle-skill | 何时创建、使用、清理? | RAII, Drop |
| rust-domain-error-skill | 谁来处理错误? | retry, circuit breaker |
| rust-mental-model-skill | 如何正确理解这个? | learning Rust |
| rust-anti-pattern-skill | 这个模式有问题吗? | code smell |

### Layer 3: 领域扩展 (domain-*)

| 技能 | 领域 | 核心约束 |
|------|------|---------|
| rust-fintech-skill | 金融科技 | 审计、精度、一致性 |
| rust-ml-skill | 机器学习 | 内存效率、GPU 加速 |
| rust-cloud-native-skill | 云原生 | 12-Factor、可观测性 |
| rust-iot-skill | 物联网 | 离线优先、功耗、安全 |
| rust-web-skill | Web 服务 | 无状态、低延迟 |
| rust-embedded-skill | 嵌入式 | no_std、无堆分配 |

### 基础技能

| 技能 | 描述 | Layer |
|------|------|-------|
| rust-core-skill | 变量、数据类型、函数、控制流 | 入门 |
| rust-ownership-skill | 所有权、借用、生命周期 | Layer 1 |
| rust-struct-enum-skill | 结构体、枚举、模式匹配 | 入门 |
| rust-generics-skill | 泛型、Trait、trait object | Layer 1 |
| rust-error-handling-skill | Result、Option、错误传播 | Layer 1 |
| rust-collections-skill | Vec、String、HashMap | 进阶 |
| rust-iterators-skill | 迭代器、闭包、函数式 | 进阶 |
| rust-smart-pointers-skill | Box、Rc、Arc、RefCell | Layer 1 |
| rust-concurrency-skill | 线程、消息传递、共享状态 | Layer 1 |
| rust-async-skill | async/await、Tokio、Future | 进阶 |
| rust-cargo-skill | 包管理、依赖、工作区 | 工程 |
| rust-testing-doc-skill | 单元测试、集成测试、文档 | 工程 |
| rust-cli-project-skill | CLI 开发、参数解析 | 工程 |

## 学习路径

### 入门路径（1-2 周）

1. rust-core-skill - 基础语法
2. rust-ownership-skill - 所有权系统
3. rust-struct-enum-skill - 数据组织

### 进阶路径（2-4 周）

4. rust-generics-skill - 泛型抽象
5. rust-error-handling-skill - 错误处理
6. rust-collections-skill - 集合类型
7. rust-iterators-skill - 函数式编程

### Layer 1 路径

8. rust-mutability-skill - 可变性设计
9. rust-zero-cost-skill - 零成本抽象
10. rust-type-driven-skill - 类型驱动设计
11. rust-resource-management-skill - 资源管理模式

### Layer 2 路径

12. rust-domain-design-skill - 领域设计
13. rust-performance-skill - 性能优化
14. rust-ecosystem-skill - 生态选择
15. rust-lifecycle-skill - 生命周期管理

### 领域路径

16. rust-fintech-skill / rust-ml-skill / rust-web-skill 等

## 命令系统

| 命令 | 描述 |
|------|------|
| /rust-features [version] | 获取 Rust 版本特性 |
| /crate-info \<crate> | 获取 crate 信息 |
| /docs \<crate> [item] | 获取 API 文档 |

## 官方资源

- [The Rust Programming Language](https://doc.rust-lang.org/book/)
- [The Rust Standard Library](https://doc.rust-lang.org/std/index.html)
- [Cargo Book](https://doc.rust-lang.org/cargo/index.html)
- [rustdoc Book](https://doc.rust-lang.org/rustdoc/index.html)

## 版本历史

- 2.0.0 - 添加元认知框架、Layer 1/2/3 分层、Domain Extensions
- 1.0.0 - 初始版本，包含 13 个基础子技能
