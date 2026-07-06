---
name: design-pipeline
description: 美工全流程 - 从参考店铺到成品设计，自动分析风格并生成同风格电商素材（主图、海报、Banner）。激活条件：(1) 用户需要分析店铺/竞品视觉风格
  (2) 用户需要生成电商产品主图 (3) 用户需要制作活动Banner/海报 (4) 用户需要批量生成同风格产品图 (5) 用户需要从参考URL提取设计语言并复用。关键词：美工、设计、主图、海报、Banner、批量生成、风格分析、店铺拆解、电商素材、详情页、小红书、产品图、视觉风格
metadata:
  openclaw:
    emoji: 🖼️
    userInvocable: true
    version: 1.0.0
---

# 美工全流程 (Design Pipeline)

从参考店铺到成品设计的自动化电商美工工作流。串联浏览器截图、风格分析、AI 生图三大环节，一条龙输出同风格电商素材。

## 核心能力链

```
参考URL/图片 → 浏览器截图 → 风格拆解分析 → 设计简报生成 → nano-banana2 AI生图 → 成品素材
     ↑              ↑              ↑                ↑                ↑              ↑
  用户输入     OpenClaw浏览器   store-teardown   本技能核心     Gemini图像生成   输出交付
```

## 依赖工具

| 工具 | 用途 | 调用方式 |
|------|------|----------|
| OpenClaw 浏览器 | 截取参考页面 | `take_screenshot` MCP 工具 |
| store-teardown | 店铺视觉拆解分析 | `{baseDir}/../store-teardown/scripts/` |
| nano-banana2 | Gemini AI 图像生成 | 见下方命令格式 |
| ecommerce-designer | 模版渲染（可选） | `{baseDir}/../ecommerce-designer/scripts/` |

### nano-banana2 命令格式

```bash
cd {baseDir}/../nano-banana2/scripts && .venv/bin/python nano_banana2.py \
  --mode image \
  --prompt "提示词" \
  --aspect-ratio "1:1" \
  --output "/tmp/design-pipeline/"
```

### 画幅比例速查

| 素材类型 | 比例 | 适用场景 |
|----------|------|----------|
| 主图 | 1:1 | 淘宝/天猫/京东/拼多多产品主图 |
| 详情页 | 3:4 或 2:3 | 商品详情长图分段 |
| Banner (宽幅) | 21:9 | 店铺首页通栏 Banner |
| Banner (标准) | 16:9 | 活动专区 Banner |
| 小红书封面 | 3:4 | 小红书笔记封面图 |
| 抖音封面 | 9:16 | 抖音/快手竖版封面 |
| 公众号封面 | 16:9 | 微信公众号文章头图 |

---

## 工作模式

本技能支持 4 种工作模式，根据用户输入自动判断或由用户指定。

### 模式 1: 参考生成 (Reference-based Generation)

从店铺/产品 URL 截图 → 风格拆解 → 设计简报 → AI 生成同风格素材。
触发词: "参考这个店铺生成"、"照着这个风格做"、"分析这个链接的设计"

> 详见 [references/mode-reference-gen.md](references/mode-reference-gen.md)

### 模式 2: 产品主图 (Product Main Image)

根据产品描述生成 4 种变体主图 (白底/场景/氛围/特写)。
触发词: "做主图"、"生成产品图"、"产品主图"

> 详见 [references/mode-product-main.md](references/mode-product-main.md)

### 模式 3: 店铺 Banner

根据活动信息生成多尺寸 Banner，支持自动匹配活动风格预设。
触发词: "做Banner"、"做海报"、"做活动图"、"促销Banner"

> 详见 [references/mode-banner.md](references/mode-banner.md)

### 模式 4: 批量生成 (Batch Generation)

锁定风格锚点后，为多个产品顺序生成视觉一致的系列主图。
触发词: "批量生成"、"一组产品图"、"全店主图"、"系列产品图"

> 详见 [references/mode-batch.md](references/mode-batch.md)

---

## 提示词工程

提示词构造遵循统一结构，附带风格/背景/光线关键词速查表。

> 详见 [references/prompt-guide.md](references/prompt-guide.md)

---

## 交互规范

### 接收需求时

1. 识别工作模式 (参考生成 / 产品主图 / Banner / 批量生成)
2. 确认必填参数是否齐全
3. 缺少信息时主动追问，追问简洁直接

### 追问模板

```
收到! 需要确认几个信息:
1. [缺少的信息A]?
2. [缺少的信息B]?
3. 风格偏好: [给出2-3个选项]?
```

### 执行过程中

- 每完成一个关键步骤，简要汇报进度
- 风格分析完成后，先展示设计简报让用户确认再生图
- 生图完成后展示结果并询问是否需要调整

### 交付时

汇报: 文件位置、尺寸、风格关键词、生成素材清单。提供调整选项 (换风格/调配色/重新生成/出其他尺寸)。

所有产出统一存放在 `/tmp/design-pipeline/` 下，按模式分子目录 (reference/, output/, product-main/, banner/, batch/)。

## 注意事项

1. **风格一致性**: 批量生成时始终使用同一份 style_anchor，不要中途修改
2. **提示词语言**: nano-banana2 提示词统一使用英文，效果最佳
3. **比例匹配**: 严格按照目标平台要求选择 aspect-ratio，不要混用
4. **迭代优先**: 先生成少量样本确认方向，再批量铺开
5. **文字叠加**: AI 生图不擅长生成精确文字，Banner/海报的文案部分建议后期叠加
6. **版权意识**: 不要在提示词中引用具体品牌名/IP名称，用风格描述替代
