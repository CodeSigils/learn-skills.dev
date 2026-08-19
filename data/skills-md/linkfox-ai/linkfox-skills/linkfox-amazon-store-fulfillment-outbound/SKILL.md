---
name: linkfox-amazon-store-fulfillment-outbound
description: 亚马逊 Multi-Channel Fulfillment（MCF）出仓履约 Skill，经 LinkFox /spApi/developerProxy 调用 Fulfillment Outbound API v2026-07-04，并提供该文档角色列表关联的 Invoices v2026-06-25 getInvoiceHeaders；支持配送报价与预览、创建/查询/列出/更新/取消履约订单、动态沙箱订单/包裹状态更新及发票头分页查询。用户提到 Fulfillment Outbound、MCF、多渠道配送、getOffers、getOrderPreview、createOrder、getInvoiceHeaders、Amazon 库存配送到站外客户、订单包裹与跟踪、签收证明或投递照片、receivedBy、locker/drop-off location、商品序列号/unitIdentifiers、v2026-07-04 时触发。与 External Fulfillment、普通 Orders API 和旧版 v2020-07-01 不同。
---

# Amazon 店铺 Fulfillment Outbound

Use this Skill for Amazon Multi-Channel Fulfillment workflows on Fulfillment Outbound `v2026-07-04`. It exposes all nine operations in Amazon's current Outbound model plus the overview page's associated `getInvoiceHeaders` operation from Invoices `v2026-06-25`, while keeping the existing production `linkfox-amazon-store-fba` and `linkfox-amazon-store-external-fulfillment` implementations untouched.

## Prerequisites

1. Require **`linkfox-amazon-store-auth`**. Run `python scripts/check_auth_dependency.py`; exit code `42` means the dependency must be installed or loaded first.
2. Select one authorized store and obtain its `sellerId` and `region`. Accept only `NA`, `EU`, or `FE`.
3. Never accept or forward `amzAccessToken`, `accessToken`, or `refreshToken`; the server resolves authorization from `sellerId + region`.
4. Read [references/api.md](references/api.md) for operation contracts and [references/workflows.md](references/workflows.md) before a create, update, or cancel action.
5. After explicit user confirmation, pass boolean `confirmWrite: true` to `createOrder`, `updateOrder`, `cancelOrder`, `updateOrderStatus`, or `updatePackage`; the wrappers reject writes without it.
6. When Amazon assigned a multi-tenant service identifier, pass it only as top-level `fulfillmentServiceId` (1–40 characters). The proxy maps it to `x-amzn-fulfillment-service-id`; never put the raw header name in query or body.

## 调用方式

- **API 端点**：`POST /spApi/developerProxy`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/<operation_script>.py '<JSON 参数>' [--inline] [--no-cache]`
- **调用约束**：本工具沿用 Amazon Store Skill 的统一免费配置；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换参数、翻页或连续试探；需要继续调用时先征得用户同意。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-store-fulfillment-outbound-<timestamp>.json`（`<session>` 取自 `SESSION_ID`；禁止写入 `/tmp`，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数、最大列表字段长度及前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）
- 加 `--no-cache` 强制本次读/预览操作访问网关；只在用户要求刷新或已确认外部状态变化时使用

**读数据建议**：先看摘要；需要具体字段时用 `jq` 或 `ConvertFrom-Json` 从保存文件按需抽取。

## Operation Guide

| Stage | Operation | Script | Availability |
|---|---|---|---|
| Quote | `getOffers` | `get_offers.py` | Production |
| Preview | `getOrderPreview` | `get_order_preview.py` | Production |
| Create | `createOrder` | `create_order.py` | Production |
| Read | `getOrder` | `get_order.py` | Production |
| List | `listOrders` | `list_orders.py` | Production |
| Release hold / update | `updateOrder` | `update_order.py` | Production |
| Cancel | `cancelOrder` | `cancel_order.py` | Production |
| Simulate order status | `updateOrderStatus` | `update_order_status.py` | Amazon dynamic sandbox only |
| Simulate package status | `updatePackage` | `update_package.py` | Amazon dynamic sandbox only |
| List invoice headers | `getInvoiceHeaders` | `get_invoice_headers.py` | Production, Invoices v2026-06-25 |

## Workflow Rules

1. Use `getOffers` for multi-SKU delivery options and expiration times; use `getOrderPreview` for planned shipments, fees, constraints, and fulfillability.
2. Show the chosen store, destination, line items, service tier, fees, hold/ship action, and `orderId` before `createOrder`.
3. Treat `orderId` and every `lineItemId` as seller-controlled idempotency identifiers. Never invent a replacement ID after an uncertain timeout.
4. A `createOrder` response can be HTTP 200 or 202. On 202, use the returned/requested `orderId` with `getOrder`; do not automatically poll.
5. Use `updateOrder` only to update the supported fulfillment configuration, currently the HOLD/SHIP action. Confirm before releasing a held order.
6. Confirm before `cancelOrder`. Amazon only stops fulfillment where cancellation is still possible; do not present 202 as completed cancellation.
7. Add `shipments: "INCLUDE"` to `getOrder` or `listOrders` when package and tracking details are needed.
8. Never automatically replay POST/PUT after 429, 500, 503, or a timeout. Recover with `getOrder` where possible.
9. Use `getInvoiceHeaders` only for header-level invoice discovery. Require `marketplaceId`; provide both issue-date bounds or neither, keep the range within 90 days, and page with `nextToken` only after user approval.

## Important Limitations

- `updateOrderStatus` and `updatePackage` are marked `x-amzn-api-sandbox-only: true` by Amazon. Consistent with the existing FBA skill, their wrappers use the same `/spApi/developerProxy` request shape as every other operation and do not accept or send a separate `sandbox` control field. Use them only with sandbox test data; availability depends on the unified gateway/upstream route.
- The optional `x-amzn-fulfillment-service-id` multi-tenant header is exposed only through the typed top-level `fulfillmentServiceId` parameter. Raw header names, nested aliases, blank values, values over 40 characters, and newline characters are rejected before calling the gateway.
- Amazon's Outbound overview role list mentions `getInvoiceHeaders`, but its Reference path is `/finances/invoices/2026-06-25/invoices`. This Skill exposes it as an explicitly labeled related Invoices operation; it is not counted among the nine Outbound OpenAPI operations and does not accept `fulfillmentServiceId`.
- Legacy v2020-07-01 returns, features, and package-tracking operations remain in the production FBA Skill and are not copied into this current-version Skill. Read [references/migration.md](references/migration.md) when migrating.

## Display Rules

- Present Amazon data and identifiers without exposing internal tool names or access tokens.
- Separate operation success from business completion: show gateway `errcode`, Amazon `httpStatus`, order `status`, constraints, and next action.
- For offers and previews, show expiration, service tier, delivery interval, currency, price, and item constraints together.
- For orders, show `orderId`, status, line items, shipments, packages, tracking, proof of delivery, drop-off/locker details, unit identifiers, and pagination token only when present.

## User Expression

**Ask**: “Check MCF delivery options for these Amazon SKUs to this postal code.”

**Do**: use `getOffers`; do not create an order.

**Ask**: “Preview and then create this MCF order.”

**Do**: run `getOrderPreview`, present constraints and fees, obtain confirmation, then run `createOrder` once.

**Ask**: “Track my MCF order.”

**Do**: run `getOrder` with `shipments: "INCLUDE"`; do not call the legacy tracking operation.

## Feedback

Report issues with `skillName: linkfox-amazon-store-fulfillment-outbound`, operation, masked IDs, resolved path, gateway status, and Amazon response summary. Never include credentials.

## 积分消耗规则

不消耗积分（以网关实际计费为准）。

---
*更多跨境 Skill：[LinkFox Skills](https://skill.linkfox.com/)*
