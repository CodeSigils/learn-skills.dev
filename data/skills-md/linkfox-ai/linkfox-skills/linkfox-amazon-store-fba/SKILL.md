---
name: linkfox-amazon-store-fba
description: 亚马逊店铺 Fulfillment by Amazon（FBA）系列（与 linkfox-amazon-store-auth 同系列），经 /spApi/developerProxy 调用 SP-API：FBA Inbound Eligibility（getItemEligibilityPreview）、FBA Inventory（getInventorySummaries/createInventoryItem/deleteInventoryItem/addInventory）、Fulfillment Inbound v2024-03-20（InboundPlan/装箱/放置/运输/货件等）与 v0（prepInstructions/labels/BOL/shipments）、Fulfillment Outbound 2020-07-01（MCF 履约单/预览/退货/tracking/features）。当用户提到 FBA、入仓资格、Inbound Eligibility、FBA 库存摘要、Send to Amazon、Inbound Plan、FBA 货件、MCF、多渠道履约、getItemEligibilityPreview、getInventorySummaries、createInboundPlan、createFulfillmentOrder 时触发。与 External Fulfillment / 普通 Orders 不同。
---

# Amazon 店铺 Fulfillment by Amazon (FBA)

本 skill 与 **`linkfox-amazon-store-auth`** 同属 **Amazon Store** 系列：依赖授权选店（`sellerId`+`region`）；经 **`POST /spApi/developerProxy`** 转发 SP-API（勿传 `amzAccessToken`，除非兼容旧调用）。

覆盖 **方案 A** 模块：

1. **Inbound Eligibility v1**（入仓/混装资格预览）
2. **FBA Inventory v1**（仓内库存）
3. **Fulfillment Inbound v2024-03-20**（现行入仓工作流）+ **v0** 保留查询
4. **Fulfillment Outbound 2020-07-01**（MCF 多渠道履约）

不包含：FBA Small and Light（已弃用）、External Fulfillment（见 `linkfox-amazon-store-external-fulfillment`）、Merchant Fulfillment（MFN）。

## 调用方式

- **统一入口**：`python scripts/fba_api.py '{"api":"<operationId>","sellerId":"...","region":"NA",...}' [--inline]`
- **单接口脚本**：`python scripts/<脚本名>.py '<JSON>' [--inline]`（完整对照见 `references/capabilities.md`）
- **写操作 body**：优先传 **`requestBody`**；也可把业务字段平铺在 JSON 中（脚本会排除 sellerId/region/path/query 后组装 body）
- **Query**：声明字段直接传；或用 **`query`** 对象 / **`queryString`** 覆盖
- **成本约束**：失败/空结果不得自动翻页或连续试探；继续前先说明可能产生额外消耗

**输出策略**：完整响应落盘到 `linkfox/<date>/<session>/data/linkfox-amazon-store-fba-*.json`；>8KB 默认摘要；`--inline` 全量打印。

## 解决认证和积分问题

发生未配置 API Key、401/402、积分不足时，采用 `references/onboarding.md` 引导。

## Prerequisites

1. 依赖 **`linkfox-amazon-store-auth`**：`python scripts/check_auth_dependency.py`（exit 42 → 先装 auth）
2. 应用需具备 **Amazon Fulfillment** 等相关角色（以 Amazon 控制台为准）
3. 网关需放行路径前缀：`fba/`、`inbound/fba/`（遇 **1005** 找后端加白）

## Current Capabilities

共 **70** 个 operation。模块表：

| 模块 | 数量 | 说明 |
|------|------|------|
| eligibility | 1 | getItemEligibilityPreview |
| inventory | 4 | summaries / create / delete / add |
| inbound_v0 | 6 | prep / labels / BOL / shipments / items |
| inbound (2024-03-20) | 45 | InboundPlan 全流程 |
| outbound (2020-07-01) | 14 | MCF 履约 |

**完整 Operation ↔ path ↔ 脚本表**：见 [`references/capabilities.md`](references/capabilities.md)  
**机器可读注册表**：`scripts/_fba_endpoints.py`、`references/operations.json`

## Quick Parameters

### getItemEligibilityPreview

- 必填：`asin`、`program`（`INBOUND`|`COMMINGLING`）
- `program=INBOUND` 时必填 `marketplaceIds`（或 `marketplaceId`，最多 1 个）

```bash
python scripts/get_item_eligibility_preview.py '{"sellerId":"A1...","region":"NA","asin":"B0...","program":"INBOUND","marketplaceId":"ATVPDKIKX0DER"}'
```

### getInventorySummaries

- 必填：`granularityType`（通常 `Marketplace`）、`granularityId`（marketplaceId）、`marketplaceIds`
- 可选：`details`、`sellerSkus`、`startDateTime`、`nextToken`

### Inbound / Outbound 写操作

复杂 schema 请用 **`requestBody`** 按官方模型传完整 JSON；path 参数（如 `inboundPlanId`、`shipmentId`、`sellerFulfillmentOrderId`）与 query 字段并列在入参中。

异步步骤（generate*Options 等）返回后用 **`getInboundOperationStatus`** 轮询（勿擅自高频轮询，先征得用户同意）。

## Scripts

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

# 统一入口
python scripts/fba_api.py '{"api":"getItemEligibilityPreview","sellerId":"A1...","region":"NA","asin":"B0...","program":"INBOUND","marketplaceIds":["ATVPDKIKX0DER"]}'

python scripts/fba_api.py '{"api":"getInventorySummaries","sellerId":"A1...","region":"NA","granularityType":"Marketplace","granularityId":"ATVPDKIKX0DER","marketplaceIds":["ATVPDKIKX0DER"],"details":true}'

python scripts/fba_api.py '{"api":"listInboundPlans","sellerId":"A1...","region":"NA","pageSize":10}'
```

共享模块：`_spapi_fba_common.py`、`_fba_endpoints.py`、`_fba_runner.py`（非独立 CLI）。

## Display Rules

1. 先看 `developerProxy.errcode` / `httpStatus`，再看解析字段 **`payload`**
2. 202/204 可能无 body；以状态码判断成功
3. Inbound 2024 与 v0 的 `getShipments`/`getShipment` 勿混淆：v0 脚本为 `get_shipments_v0.py`；2024 货件为 `get_inbound_shipment.py`
4. 与 **`linkfox-amazon-store-orders`**、**`linkfox-amazon-store-external-fulfillment`** 边界清晰，勿混用

## Important Limitations

- Outbound **2026-07-04** 未纳入本 skill（方案 A）
- Small and Light 已弃用，不实现
- Inbound 状态机复杂，需按官方工作流顺序调用；冲突常见 **409/422**
- 限速因接口而异（Eligibility 约 1 rps），注意 **429**

## 积分消耗规则

不消耗积分（以网关实际计费为准）。

**Feedback：** `skillName`：`linkfox-amazon-store-fba`

---
*更多跨境 skill：[LinkFox Skills](https://skill.linkfox.com/)*
