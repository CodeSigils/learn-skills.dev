---
name: interaction-design
description: 用于输出交互设计方案。当用户提出“设计交互、设计流程、怎么操作、优化流程、改体验、交互方案、画原型”等需求时使用。通过需求解析、目标对齐、背景采集、路径分析、方案对比、细节设计和 HTML 原型验证，产出结构化交互方案与可点击原型。
---

# Interaction Design

用于把一个模糊的产品想法、功能需求或体验问题，转化为可讨论、可验证、可落地的交互方案。

核心原则：

> 交互设计不是“页面怎么摆”，而是帮助用户以尽可能低的成本完成任务，同时让业务目标、系统反馈和异常兜底都成立。

## 适用场景

当用户提出以下需求时使用：

- 设计某个功能的操作流程
- 优化已有产品体验
- 梳理用户完成任务的关键路径
- 对比多个交互方案
- 输出交互说明、流程说明或产品原型
- 将文字方案转成可点击 HTML 原型

## 工作流程

### 1. 需求快速解析

先用 1-3 句话确认当前需求：

- 这是什么功能？
- 用户要完成的核心任务是什么？
- 什么结果代表“体验成功”？

如果需求过于模糊，先给出合理理解，并标注假设，不要直接进入细节设计。

### 2. 目标对齐

交互方案必须先对齐目标，再设计路径。

优先从用户提供的产品背景、需求文档、数据、业务描述或上下文中提取目标。如果信息不足，主动询问：

- 这个功能最想提升什么指标？
- 当前更关注拉新、激活、转化、留存、效率、满意度，还是风险控制？
- 有没有现有数据或参考基准？
- 这次设计最不能牺牲的体验或业务约束是什么？

常见目标示例：

| 业务/产品目标 | 可转化的交互目标 |
| --- | --- |
| 提升转化率 | 减少决策摩擦、突出价值、强化行动引导 |
| 提升留存 | 建立进度感、降低再次进入成本、提供持续反馈 |
| 提升效率 | 缩短路径、减少重复输入、支持批量操作 |
| 降低错误率 | 预防误操作、增强校验、提供撤销与恢复 |
| 提升信任感 | 解释规则、展示依据、明确状态与结果 |
| 提升内容消费 | 优化浏览节奏、强化筛选、降低理解成本 |

输出目标摘要：

```markdown
目标摘要：
- 当前重点：[如：提升新用户完成首单的转化率]
- 核心指标：[如：首单转化率、下单耗时、支付失败率]
- 关键约束：[如：不能增加注册前置步骤]
- 交互目标：[如：减少决策摩擦、强化价值感、提供错误兜底]
```

### 3. 背景信息采集

至少确认 3 类信息：

- 使用频次：高频 / 中频 / 低频
- 使用场景：移动中、办公室、碎片时间、多人协作、强任务场景等
- 用户类型：新手、熟悉用户、专家用户、管理员、运营人员等

根据需求补充追问：

- 复杂流程：有没有参考产品或现有流程？
- 多角色协作：谁发起，谁审核，谁执行，谁接收结果？
- 决策类功能：用户做判断时依赖什么信息？
- 高风险操作：最坏情况是什么，是否需要确认、撤销或审批？
- 数据密集场景：用户最常比较、筛选、定位什么？

### 4. 交互目标定位

把目标翻译成 2-3 个交互关键词，例如：

- 最短路径
- 价值可视化
- 减少决策摩擦
- 强反馈
- 防误触
- 可撤销
- 状态透明
- 渐进披露
- 新手友好
- 专家提效

不要贪多。交互目标越多，方案越容易发散。

### 5. 关键路径分析

必须覆盖 3 条路径：

**Happy Path：一切顺利时**

- 用户做什么？
- 系统给什么反馈？
- 用户如何知道自己成功了？

**Sad Path：出错或失败时**

- 哪些地方可能失败？
- 系统如何解释原因？
- 用户下一步还能做什么？

**Edge Case：边界情况**

- 空状态
- 网络异常
- 权限不足
- 数据过多或过少
- 重复提交
- 中途退出
- 多端状态不一致
- 不可逆或高风险操作

### 6. 方案对比

当存在多个方案时，用矩阵比较，不只凭喜好判断。

推荐维度：

| 维度 | 方案 A | 方案 B | 方案 C |
| --- | --- | --- | --- |
| 用户操作步数 |  |  |  |
| 理解成本 |  |  |  |
| 业务目标对齐度 |  |  |  |
| 异常处理完整度 |  |  |  |
| 开发成本 |  |  |  |
| 可扩展性 |  |  |  |
| 风险 |  |  |  |

最后明确推荐方案，并说明为什么。

### 7. 交互细节输出

对推荐方案补齐细节：

- 入口：用户从哪里进入，什么条件下看到
- 主路径：每一步的操作、页面状态和系统反馈
- 反馈：点击、加载、成功、失败、空状态、禁用态
- 容错：撤销、二次确认、自动保存、草稿、恢复
- 文案：按钮、提示、错误说明、成功反馈
- 权限：谁能看，谁能操作，谁不能操作
- 数据：需要展示哪些字段，哪些信息延后展示
- 埋点：关键转化、退出、失败、重复操作等指标

## HTML 原型

当用户需要“可点击体验”或方案较复杂时，输出单文件 HTML 原型。

原则：

- 单文件：一个 `.html` 文件，内联 CSS 和 JS
- 可交互：按钮、弹窗、Tab、状态切换、表单反馈可操作
- 移动优先：优先适配 375px 视口，桌面端自适应
- 示例数据：使用虚构数据，并标注“示例数据”
- 无外部依赖：不依赖远程 CSS、JS 或图片
- 可验证：Happy Path、Sad Path、Edge Case 都有可视化呈现

原型常见视图：

- 入口页
- 列表页
- 详情页
- 表单页
- 确认弹窗
- 成功反馈
- 错误反馈
- 空状态
- 权限不足状态

HTML 结构建议：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>功能名称 - 交互原型</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #f5f6f8;
      color: #1f2937;
    }
    .prototype-shell {
      width: min(100%, 420px);
      min-height: 100vh;
      margin: 0 auto;
      background: #ffffff;
    }
    .page { display: none; padding: 16px; }
    .page.active { display: block; }
    .button {
      border: 0;
      border-radius: 8px;
      padding: 12px 16px;
      background: #2563eb;
      color: #ffffff;
      font-weight: 600;
      cursor: pointer;
    }
    .button.secondary {
      background: #e5e7eb;
      color: #111827;
    }
    .card {
      border: 1px solid #e5e7eb;
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 12px;
      background: #ffffff;
    }
    .modal-mask {
      position: fixed;
      inset: 0;
      display: none;
      align-items: center;
      justify-content: center;
      background: rgba(0, 0, 0, 0.42);
      padding: 20px;
    }
    .modal {
      width: min(100%, 360px);
      border-radius: 12px;
      background: #ffffff;
      padding: 20px;
    }
  </style>
</head>
<body>
  <main class="prototype-shell">
    <section class="page active" id="page-entry">
      <p>示例数据</p>
      <button class="button" onclick="showPage('detail')">开始操作</button>
    </section>

    <section class="page" id="page-detail">
      <div class="card">这里展示核心信息</div>
      <button class="button" onclick="openModal()">提交</button>
      <button class="button secondary" onclick="showPage('entry')">返回</button>
    </section>
  </main>

  <div class="modal-mask" id="confirm-modal">
    <div class="modal">
      <h2>确认提交？</h2>
      <p>提交后系统会立即处理。</p>
      <button class="button" onclick="showSuccess()">确认</button>
      <button class="button secondary" onclick="closeModal()">取消</button>
    </div>
  </div>

  <script>
    function showPage(id) {
      document.querySelectorAll(".page").forEach(page => page.classList.remove("active"));
      document.getElementById("page-" + id).classList.add("active");
    }

    function openModal() {
      document.getElementById("confirm-modal").style.display = "flex";
    }

    function closeModal() {
      document.getElementById("confirm-modal").style.display = "none";
    }

    function showSuccess() {
      closeModal();
      alert("操作成功");
    }
  </script>
</body>
</html>
```

原型检查清单：

- 主流程可以完整点击走通
- 关键按钮有即时反馈
- 加载、成功、失败、空状态至少覆盖必要场景
- 弹窗可打开和关闭
- 表单有校验或错误提示
- 移动端 375px 视口不横向溢出
- 示例数据已明确标注

## 标准输出模板

```markdown
收到，下面是交互方案：

## 需求理解

[用一句话说明这是一个什么功能，用户要完成什么任务。]

## 目标对齐

- 当前目标：[产品/业务/体验目标]
- 核心指标：[转化率、完成率、耗时、错误率、留存等]
- 关键约束：[时间、技术、合规、角色、场景等]
- 交互目标：[2-3 个关键词]

## 背景确认

- 使用频次：[高/中/低]
- 使用场景：[具体场景]
- 用户类型：[新手/熟悉用户/专家用户/多角色]

## 关键路径

### Happy Path

1. 用户 [操作] -> 系统 [反馈]
2. 用户 [操作] -> 系统 [反馈]
3. 用户完成任务，并看到 [成功状态]

### Sad Path

- 如果 [错误/失败]，系统 [解释原因]，用户可以 [下一步操作]

### Edge Case

- 如果 [边界情况]，系统 [处理方式]

## 方案对比

| 维度 | 方案 A | 方案 B |
| --- | --- | --- |
| 操作步数 |  |  |
| 理解成本 |  |  |
| 目标对齐 |  |  |
| 异常处理 |  |  |
| 开发成本 |  |  |

推荐：[方案 X]

理由：[简洁说明推荐原因]

## 推荐方案细节

- 入口：[从哪里进入]
- 主流程：[核心步骤]
- 反馈机制：[点击/加载/成功/失败]
- 容错设计：[撤销/确认/自动保存/恢复]
- 关键文案：[按钮、提示、错误信息]
- 数据埋点：[需要观察的关键行为]

## 原型

- 文件：[如已生成，填写 HTML 文件名或路径]
- 包含视图：[入口页/详情页/弹窗/成功态/失败态等]
- 验证结果：[主流程是否走通，异常状态是否覆盖]
```

## 常见模式

表单提交：

填写 -> 实时校验 -> 提交 -> 加载 -> 成功反馈 / 错误修正 -> 跳转或留在当前页

列表操作：

筛选 -> 选择对象 -> 操作 -> 二次确认 -> 状态更新 -> 支持撤销或查看结果

复杂流程：

步骤拆分 -> 进度提示 -> 自动保存 -> 中途退出恢复 -> 完成确认 -> 异常兜底

决策辅助：

信息分层 -> 关键指标突出 -> 推荐理由解释 -> 风险提示 -> 用户确认

高风险操作：

权限判断 -> 影响说明 -> 二次确认 -> 执行反馈 -> 操作记录 -> 可恢复方案

## 交互设计 8 条检查原则

1. 目标先行：先确认产品目标和用户任务，再设计界面。
2. 主路径最短：高频关键任务尽量减少步骤。
3. 状态透明：用户随时知道当前在哪、发生了什么、下一步做什么。
4. 反馈及时：点击、提交、加载、成功、失败都要有反馈。
5. 错误友好：说明原因，提供解决办法，不只告诉用户“失败”。
6. 容错充分：支持撤销、草稿、恢复、二次确认或防重复提交。
7. 信息分层：先给决策必需信息，再提供详情。
8. 新手可懂，熟手高效：低频功能要清晰，高频功能要快捷。

## 输出要求

最终方案应尽量做到：

- 目标明确
- 路径完整
- 方案可比较
- 异常有兜底
- 细节可执行
- 原型可点击
- 结论可复盘
