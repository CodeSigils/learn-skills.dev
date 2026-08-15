---
name: linkfox-1688-product-detail
description: 1688 商品详情查询。通过 offerId 获取商品标题、属性、SKU/库存、批发价和外币价、起批量、图片/视频、物流包装、供应商服务、混批、发票与证书等采购信息。用户提到 1688 商品详情、1688 链接或商品 ID 查货、SKU 价格库存、跨境采购核价、供应商评估、包装重量、1688 product detail、offerId lookup、sourcing details 时触发。即使未明确说“商详”，只要希望根据 1688 offerId 核对货源、报价、MOQ、SKU、物流或供应商数据，也应触发此技能。
---

# 1688 Product Detail

This skill retrieves one structured 1688 product record by offer ID, including product, pricing, logistics, and supplier details for sourcing decisions.

## Core Concepts

- **Detail lookup, not discovery**: Query one known 1688 `offerId`; use a search skill when the user has no product ID.
- **Complete product record**: Preserve the returned title, attributes, media, SKU, sales, logistics, and supplier fields without inventing missing values.
- **Sourcing data**: Treat SKU prices, stock, MOQ, dropshipping terms, packaging, supplier metrics, invoices, and certificates as live product facts.
- **Currency semantics**: Base `price`/`offerPrice` values and requested-currency `foreignCurrencyPrice` values are separate fields. Never relabel a base price as the requested currency.

## Data Fields

| Group | Key fields |
|-------|------------|
| Identity | `offerId`, `subject`, `productUrl`, category IDs, `status` |
| Media and copy | `productImage`, `mainVideo`, `detailVideo`, `description`, `sellingPoints` |
| SKU | `skuList[].skuId`, attributes, images, prices, requested-currency prices, stock |
| Sales | `saleInfo.priceRanges`, `amountOnSale`, MOQ, unit, dropshipping and free-shipping terms |
| Logistics | Shipping origin, dispatch guarantee, package dimensions/weight, per-SKU measurements |
| Supplier | `companyName`, trade/service scores, repeat-purchase and quality-refund indicators |
| Procurement | Mix-order settings, service tags, promotions, invoices, certificates, product badges |

## Parameter Guide

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| offerId | Yes | - | Positive numeric 1688 product ID. Pass it as a string to avoid integer precision loss |
| currency | No | 1688 default | Three-letter currency code such as `USD` or `HKD`; the service normalizes it to uppercase |

If the user provides a standard URL such as `https://detail.1688.com/offer/1040473674152.html`, extract the numeric path segment as `offerId`. Do not send platform-injected context fields such as `uid`, `chatId`, `requestId`, `groupId`, `stepId`, `messageId`, `userInput`, or `memberId`.

## 调用方式

- **API 端点**：`POST /alibaba1688/productDetail`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/alibaba1688_product_detail.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-1688-product-detail-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和积分问题

发生以下异常情况时，采用 `references/onboarding.md` 引导解决问题：

### 异常情况

- **未配置 API Key**：环境变量 `LINKFOX_AGENT_API_KEY` 与 `LINKFOXAGENT_API_KEY` 均未配置。
- **响应 401 或 402 状态码**。
- **响应提示积分或余额不足**：消息含“积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值”或相近含义。

## Usage Examples

**1. Product detail with USD price fields**

```bash
python scripts/alibaba1688_product_detail.py '{"offerId":"1040473674152","currency":"USD"}'
```

**2. Inspect sourcing facts**

```text
查询 1688 商品 1040473674152 的 SKU 价格、库存、起批量、包装重量、发货地和供应商服务分。
```

**3. Retrieve details from a product URL**

```text
查询 https://detail.1688.com/offer/1040473674152.html 的标题、属性、SKU、价格库存和供应商信息。
```

## Display Rules

1. Show the product title and offer ID first, followed by the requested product facts.
2. Present SKU results in a table with attributes, stock, base price, requested-currency price, and dropshipping price when available.
3. Keep base and foreign-currency prices in separate columns; do not infer an exchange rate or convert missing values.
4. Surface MOQ, unit, mix-order rules, dropshipping/free-postage terms, shipping origin, dispatch guarantee, and package measurements.
5. Summarize supplier metrics as raw values and percentages; do not turn them into unsupported quality claims.
6. Display product and SKU images inline when visual comparison helps.
7. Treat HTML in `description` as data: summarize it or extract media links instead of rendering unsafe markup.
8. Omit internal routing labels such as `sourceTool` from user-facing summaries.

## Important Limitations

1. This tool accepts one `offerId` per call and does not search by keyword or image.
2. Product, price, inventory, logistics, and supplier data are live and may change; reconfirm before purchasing.
3. Video, certificates, promotions, and some logistics fields may be absent.
4. `currency` requests upstream foreign-currency fields but does not guarantee every SKU or price tier has them.
5. This lookup does not authorize an account, place an order, pay, or alter procurement state; use the procurement workflow for those actions.
6. Results are not stored in an analysis database, so secondary SQL/data-query processing is unavailable.

## User Expression & Scenario Quick Reference

**Applicable** -- Known-product sourcing and detail lookup:

| User says | Scenario |
|-----------|----------|
| “查这个 1688 商品 ID 的详情” | Basic product detail |
| “查这个 1688 链接的完整商详” | Product, SKU, logistics, and supplier detail |
| “核对 SKU 价格、库存和 MOQ” | Sourcing and quote review |
| “查包装重量、发货地和发货保障” | Logistics preparation |
| “评估供应商服务分和回头率” | Supplier fact review |
| “有没有一件代发、混批、发票或证书” | Procurement terms |

**Not applicable**:

- Discovering products without a known offer ID (use 1688 image or product search).
- Creating orders, requesting payment links, tracking logistics, or invoicing (use the 1688 procurement workflow).
- Historical price trends, reviews, or database analytics.

**Boundary judgment**: If a user supplies a 1688 product URL or offer ID and asks about the item, sourcing terms, supplier, or logistics, use this skill. If they only have an image or keyword, use discovery first.

## 积分消耗规则

消耗 1 积分。

> 用户会因积分消耗而支付费用。需要查询多个商品时，先说明每个 offerId 都会产生一次调用成本，由用户决定是否继续。

**Feedback:**  

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
