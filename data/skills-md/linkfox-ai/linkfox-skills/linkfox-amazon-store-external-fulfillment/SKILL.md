---
name: linkfox-amazon-store-external-fulfillment
description: 亚马逊店铺 External Fulfillment（与 linkfox-amazon-store-auth / orders / listings 同系列），经 /spApi/developerProxy 调用 SP-API External Fulfillment v2024-09-11：Inventory 的 batchInventory（按 location 查/写库存）；Shipping 的 getShipments、getShipment、processShipment、createPackages、updatePackage、updatePackageStatus、retrieveShippingOptions、generateInvoice、retrieveInvoice、generateShipLabels；Returns 的 listReturns、getReturn。覆盖 Seller Flex / Easy Ship / Self Ship / MFN Self Delivery 等。当用户提到 External Fulfillment、SmartConnect、Seller Flex、FBA Onsite、Easy Ship、Self Ship、batchInventory、location 库存、履约单 shipment、面单、发票、EF 退货、externalFulfillment 时触发。与普通 Orders/Feeds 库存不同，本技能专指 External Fulfillment API。
---

# Amazon 店铺 External Fulfillment

本 skill 与 **`linkfox-amazon-store-auth`** 等同属 **Amazon Store** 系列：依赖 **`linkfox-amazon-store-auth`** 选店（`sellerId`+`region`）；直接 **`POST /spApi/developerProxy`** 传入 `sellerId`+`region`，由服务端解析 token（勿传 `amzAccessToken`，除非兼容旧调用）。转发上游 **`GET` / `POST` / `PUT` / `PATCH`**。

适用渠道：Seller Flex / FBA Onsite、Multi Seller Flex、Easy Ship、Self Ship、MFN Self Delivery、Amazon Pharmacy 等（以商家 allowlist 与角色为准）。

## 调用方式

- **API 端点**：`POST /spApi/developerProxy`（完整参数/响应见 `references/api.md`）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；失败/空结果不得自动翻页或连续试探；需要继续时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-store-external-fulfillment-<timestamp>.json`
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要
- 加 `--inline` 强制全量打印（同样落盘）

**读数据建议**：先看摘要；需要具体字段时用 `jq` / `ConvertFrom-Json` 从落盘文件抽取。

## 解决认证和积分问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

## 官方参考索引

| 模块 | 能力 | 文档 |
|------|------|------|
| Inventory | batchInventory | [batchInventory](https://developer-docs.amazon.com/sp-api/reference/batchinventory) |
| Shipping | getShipments | [getShipments](https://developer-docs.amazon.com/sp-api/reference/getshipments-1) |
| Shipping | getShipment | [getShipment](https://developer-docs.amazon.com/sp-api/reference/getshipment-1) |
| Shipping | processShipment | [processShipment](https://developer-docs.amazon.com/sp-api/reference/processshipment) |
| Shipping | createPackages | [createPackages](https://developer-docs.amazon.com/sp-api/reference/createpackages) |
| Shipping | updatePackage | [updatePackage](https://developer-docs.amazon.com/sp-api/reference/updatepackage) |
| Shipping | updatePackageStatus | [updatePackageStatus](https://developer-docs.amazon.com/sp-api/reference/updatepackagestatus) |
| Shipping | retrieveShippingOptions | [retrieveShippingOptions](https://developer-docs.amazon.com/sp-api/reference/retrieveshippingoptions) |
| Shipping | generateInvoice | [generateInvoice](https://developer-docs.amazon.com/sp-api/reference/generateinvoice) |
| Shipping | retrieveInvoice | [retrieveInvoice](https://developer-docs.amazon.com/sp-api/reference/retrieveinvoice) |
| Shipping | generateShipLabels | [generateShipLabels](https://developer-docs.amazon.com/sp-api/reference/generateshiplabels) |
| Returns | listReturns | [listReturns](https://developer-docs.amazon.com/sp-api/reference/listreturns) |
| Returns | getReturn | [getReturn](https://developer-docs.amazon.com/sp-api/reference/getreturn) |

---

## Prerequisites（必须先读）

本 skill **依赖** **`linkfox-amazon-store-auth`**。

1. 运行 `python scripts/check_auth_dependency.py`；若 exit code **42** 且 stderr 含 `DEPENDENCY_MISSING:`，请先安装 **`linkfox-amazon-store-auth`**。
2. **不要**在本 skill 内绕过依赖实现授权或令牌逻辑。
3. 商家需 **External Fulfillment allowlist**，应用需 **Direct-to-Consumer Shipping (Restricted)** 角色。

---

## Current Capabilities（脚本一览）

| 能力 | developerProxy `path`（要点） | 脚本 |
|------|------------------------------|------|
| batchInventory | `externalFulfillment/inventory/2024-09-11/inventories`，POST | `post_batch_inventory.py` |
| getShipments | `externalFulfillment/2024-09-11/shipments` + Query | `get_shipments.py` |
| getShipment | `.../shipments/{shipmentId}` | `get_shipment.py` |
| processShipment | `.../shipments/{shipmentId}?operation=`，POST | `process_shipment.py` |
| createPackages | `.../shipments/{shipmentId}/packages`，POST | `create_packages.py` |
| updatePackage | `.../shipments/{shipmentId}/packages/{packageId}`，PUT | `update_package.py` |
| updatePackageStatus | 同上 path，PATCH | `update_package_status.py` |
| retrieveShippingOptions | `.../shipments/{shipmentId}/shippingOptions` + packageId | `retrieve_shipping_options.py` |
| generateInvoice | `.../shipments/{shipmentId}/invoice`，POST | `generate_invoice.py` |
| retrieveInvoice | 同上 path，GET | `retrieve_invoice.py` |
| generateShipLabels | `.../shipments/{shipmentId}/shipLabels?operation=`，PUT | `generate_ship_labels.py` |
| listReturns | `externalFulfillment/2024-09-11/returns` + Query | `list_returns.py` |
| getReturn | `.../returns/{returnId}` | `get_return.py` |

共享逻辑见 **`scripts/_spapi_ef_common.py`**（仅供同目录脚本 import）。

---

## Quick Parameters（摘要）

- **batchInventory**：`requests` 1～10 条。简化项：`action`=`fetch`|`update`、`locationId`、`skuId`；update 必填 `quantity`。MFN 单仓常用 `locationId=DEFAULT`；Seller Flex 用 4 位仓码。高级：`useAmazonRequestShape:true` 直传官方 `requests`。
- **getShipments**：必填 `status`（如 `ACCEPTED`/`CREATED`）；可选 `locationId`、`marketplaceId`、`channelName`、`lastUpdatedAfter/Before`、`maxResults`、`paginationToken`。
- **processShipment**：`operation`=`CONFIRM`|`REJECT`；REJECT 时可传 `referenceId`/`lineItems` 或 `requestBody`。
- **createPackages / updatePackage**：包裹尺寸重量与 `packageLineItems` 按官方 schema 放在 `packages` 或 `requestBody`。
- **updatePackageStatus**：主要用于 Self Delivery；传 `status`/`subStatus`/`reason`。
- **generateShipLabels**：`operation`=`GENERATE`|`REGENERATE`；可选 `shippingOptionId`、`packageIds`。
- **listReturns**：可选 `status`（新退货常用 `CREATED`）、`returnLocationId`、时间窗、`nextToken`。

典型履约流程：`getShipments` → `processShipment(CONFIRM)` → `createPackages` → `retrieveShippingOptions` → `generateInvoice` → `generateShipLabels` →（Self Delivery）`updatePackageStatus`。

---

## Scripts

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/post_batch_inventory.py '{"sellerId":"A1...","region":"NA","requests":[{"action":"fetch","locationId":"DEFAULT","skuId":"SKU-1","marketplaceAttributes":{"marketplaceId":"ATVPDKIKX0DER","channelName":"MFN"}}]}'

python scripts/get_shipments.py '{"sellerId":"A1...","region":"NA","status":"ACCEPTED","locationId":"ABCD"}'

python scripts/process_shipment.py '{"sellerId":"A1...","region":"NA","shipmentId":"...","operation":"CONFIRM"}'
```

---

## Display Rules

1. 先看网关 **`developerProxy.errcode` / `httpStatus`**，再解析脚本附加字段（如 **`batchInventory`**、**`shipments`**、**`invoice`**）。
2. **batchInventory** 成功时常为 **207** Multi-Status；逐条看 `responses[].status`。
3. 多数写操作成功可能为 **204**（无 body）；stdout 会标 `success: true`。
4. 发票/面单文档多为 Base64 或预签名 URL，勿把整段大 base64 反复贴进上下文。
5. **路径白名单**：若返回 **1005**，需后端放行 **`externalFulfillment/`** 前缀。

---

## Important Limitations

- 权限：**Direct-to-Consumer Shipping (Restricted)**；商家需 allowlist。
- **写库存为绝对值发布**，非增量；只同步有变化的 SKU；SKU 特殊字符需 URL 编码（脚本已处理简化入参）。
- 与 **`linkfox-amazon-store-orders`**（普通 Orders）、**`linkfox-amazon-store-feeds`**（Feed 改库存）、**`linkfox-amazon-store-report`**（库存报告）边界不同，勿混用。
- Seller Flex 上 `retrieveShippingOptions` 常返回空；Easy Ship 全球多数站点可能不支持 `generateInvoice`（印度除外）。
- 返回结构以 Amazon schema 为准；详见 **`references/api.md`**。

## 积分消耗规则

不消耗积分（以网关实际计费为准；若网关计费则按积分规则处理）。

**Feedback：** 见 `references/api.md`，`skillName`：`linkfox-amazon-store-external-fulfillment`。

---
*更多跨境 skill：[LinkFox Skills](https://skill.linkfox.com/)*
