---
name: elk
description: 快速检索和查看 ELK 日志数据，基于 Elasticsearch 数据流。
---

# /elk — ELK 日志检索

索引由项目根目录 `.elkrc.json` 中的 `index` 字段决定。默认 `*s35*`。默认时间范围 **15 分钟**，`-t N` 覆盖（分钟）。

---

## 〇、首次配置：`/elk setup`

安装 skill 后首次使用前，运行 `/elk setup`：

1. 询问用户以下配置项：

  - **ES Hosts**：例 `https://es.example.com:9200`
  - **ES Username**：例 `elastic`
  - **ES Password**
  - **索引模式**：默认 `*s35*`，可自定义如 `*myapp*`

2. 检查当前项目根目录是否存在 `.venv`，如不存在则创建并安装 MCP server：

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install elasticsearch-mcp-server
```

3. 生成或合并项目根目录 `.mcp.json`：

  - 如果 `.mcp.json` 已存在，读取并合并 `elasticsearch-mcp-server` 配置（不覆盖其他已有 MCP server）
  - 如果不存在，创建新的 `.mcp.json`

  配置内容：

```json
{
  "mcpServers": {
    "elasticsearch-mcp-server": {
      "command": ".venv\\Scripts\\elasticsearch-mcp-server.exe",
      "env": {
        "ELASTICSEARCH_HOSTS": "<用户输入的 ES Hosts>",
        "ELASTICSEARCH_USERNAME": "<用户输入的 ES Username>",
        "ELASTICSEARCH_PASSWORD": "<用户输入的 ES Password>"
      }
    }
  }
}
```

4. 生成项目根目录 `.elkrc.json`：

```json
{
  "index": "<用户输入的索引模式>"
}
```

5. 完成，告知用户重启 Claude Code 使 MCP 配置生效。

---

## 一、操作模式：`/elk use <操作>`

有 `use` 关键字时直接调用对应的 ES MCP 工具，不回显，不额外处理：

- `/elk use list_indices` → `mcp__elasticsearch-mcp-server__list_indices`
- `/elk use cluster` → `mcp__elasticsearch-mcp-server__get_cluster_health`
- `/elk use datas` → `mcp__elasticsearch-mcp-server__get_data_stream`，参数 `name: "<索引模式>"`
- `/elk use datas <pattern>` → `mcp__elasticsearch-mcp-server__get_data_stream`，参数 `name: "<pattern>"`
- `/elk use index <name>` → `mcp__elasticsearch-mcp-server__get_index`，参数 `index: "<name>"`
- `/elk use alias` → `mcp__elasticsearch-mcp-server__get_alias`，参数 `index: "<索引模式>"`
- `/elk use alias <pattern>` → `mcp__elasticsearch-mcp-server__get_alias`，参数 `index: "<pattern>"`

---

## 二、快捷查询：`/elk <内容> [-t 分钟]`

没有 `use` 就是快捷查询，分两种情况：

### 1. `id:"xxx"` → `get_document`

字段名是 `id` 且值被引号包裹：

```
/elk id:"G1jhH54BsXvF6ebjJy8x"
```

→ 回显并调用：
```
get_document:
  index: "<索引模式>"
  id: "G1jhH54BsXvF6ebjJy8x"
```

`id` 查询不加时间范围。

### 2. 其他 → `search_documents`

全部走 `search_documents`，index 从 `.elkrc.json` 读取（默认 `*s35*`），size 默认 10。

**解析步骤：**

**a) 提取查询内容和时间参数**

去掉开头 `/elk ` 和末尾 ` -t N`。`-t N` 存在则时间范围 = `now-Nm`，否则 = `now-15m`。

**b) 解析查询类型**

| 输入形式 | 方法 | 示例 |
|---|---|---|
| 纯文本（无冒号） | `match` 查 `message` | `我是傻子` |
| `字段:"值"`（引号包裹） | `term` 精确 | `hostName:"d01"` |
| `字段:值`（无引号，无 `*`） | `match` 模糊 | `hostName:123` |
| `字段:*值*`（含 `*`） | `wildcard` | `path:*/api/*` |

**c) 字段名映射**
- `message` → 保持 `message`
- `traceid`、`traceId` 或 `trace_id` → `labels.xh_trace_id`
- 其他字段 → 自动加 `labels.` 前缀

**d) 组装 body**

```json
{
  "query": {
    "bool": {
      "must": [ <步骤b的查询> ],
      "filter": [
        {"range": {"@timestamp": {"gte": "now-<N>m", "lte": "now"}}}
      ]
    }
  },
  "size": 10
}
```

**e) 回显 + 调用**

先纯文本输出完整请求块，然后立即调用 `mcp__elasticsearch-mcp-server__search_documents`：

```
> search_documents:
>   index: "<索引模式>"
>   body: {"query":{"bool":{"must":[...],"filter":[...]}},"size":10}
```

**f) 整理输出**

用表格展示 `@timestamp`、`message`、关键 labels 字段，不要直接甩原始 JSON。

---

## 三、示例速查

| 输入 | 实际查询 | 说明 |
|---|---|---|
| `/elk 我是傻子` | `match: message` | 纯文本查 message |
| `/elk traceid:"xxx"` | `term: labels.xh_trace_id` | traceid 精确 |
| `/elk hostName:"d01"` | `term: labels.hostName` | 字段精确 |
| `/elk hostName:d01` | `match: labels.hostName` | 字段模糊 |
| `/elk path:*/api/*` | `wildcard: labels.path` | 通配符 |
| `/elk id:"xxx"` | `get_document` | 按 ID 取 |
| `/elk error -t 60` | 时间范围 60 分钟 | 自定义时间 |
