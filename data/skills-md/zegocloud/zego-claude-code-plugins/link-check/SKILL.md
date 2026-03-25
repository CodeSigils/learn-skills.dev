---
name: link-check
description: 检查文档中的各类链接有效性，包括：相对链接（./path/to/file.mdx）文件存在性检查、站内链接（/some/slug）通过 config_helper.py 解析验证、中英文链接混用检查（中文文档不应出现 zegocloud.com 域名，英文文档不应出现 doc-zh.zego.im 域名）。当审核文档、检查文档质量或验证链接时使用此技能。
---

# 链接检查

## 检查流程

### 1. 确定文档语言

根据文档路径判断：
- 路径包含 `/zh/` 或 `/cn/` → 中文文档
- 路径包含 `/en/` → 英文文档
- 路径无语言标识 → 默认为中文文档（与 config_helper.py 行为一致）

### 2. 提取所有链接

从文档内容中提取所有链接：

- MD 格式链接：[文本](链接地址)
- HTML a 标签链接：<a href="链接地址">文本</a>
- 组件链接：比如：<Card title="文本" href="链接地址">文本</Card>。还有类似的 <Button> 等组件。
- 纯文本链接：http://xxx 或 https://xxx
- MDX 导入语句：import xxx from 'path' 或 import xxx from "path" 或 import { xxx } from 'path'

重点检查以下类型：

| 链接类型 | 格式示例 |
|---------|---------|
| 相对链接 | `./path/to/file.mdx`、`../path/to/file.mdx` |
| 站内链接 | `/product/feature/slug` |
| 外部链接 | `https://zegocloud.com/...`、`https://doc-zh.zego.im/...` |

### 3. 执行检查

执行检查，针对错误链接查找可能正确的链接。

#### 3.1 相对链接检查

解析相对路径，检查目标文件是否存在：
1. 基于文档所在目录解析完整路径
2. 检查文件是否存在（支持 .md 和 .mdx 扩展名）
3. 对于 `../` 路径，确保正确解析出文档根目录

如何查找可能正确的链接：
相对路径只在同一个实例下内使用，所以可以按以下步骤查找：
1. 向上遍历目录，直到找到 sidrbars.json 文件所在目录则为实例目录
2. 在实例目录下查找目标文件
3. 如果找到目标文件，则返回目标文件路径，否则返回空

#### 3.2 站内链接检查

使用 config_helper.py 解析链接：
```bash
python3 .docuo/scripts/config_helper.py --resolve-url /some/slug
```
验证返回的文件路径是否存在对应的 .mdx 文件。返回路径为空表示链接无效。

如何查找可能正确的链接：
站内链接可能是本实例也可能是其他产品其他实例的链接，所以需要按以下步骤查找：
1. 使用 `python3 .docuo/scripts/config_helper.py /some/slug --info` 命令获取slug所属实例信息。
2. 如果找不到实例信息，则说明这个链接问题比较大，直接返回空。
2. 将原始 slug 减去 routeBasePath 后得到的就是文档 id
3. 在 instanceinfo.path 目录下查找目标文档（文档id是：文件名转换为小写，空格转换为横杠(-)，然后删除.mdx后缀）
4. 如果找到目标文档，则调用 `python3 .docuo/scripts/config_helper.py <目标文档路径> --url` 获取目标文档的 URL并返回，否则返回空

#### 3.3 中英文链接混用检查

| 文档语言 | 禁止出现的域名 |
|---------|---------------|
| 中文 | `https://zegocloud.com` |
| 英文 | `https://xxx.zego.im` |

例外：带文件后缀的可下载资源文件（如 `.zip`、`.pdf`）不受此限制。

#### 3.4 锚点检查
1. 如果是 slug 链接，先用 `python3 .docuo/scripts/config_helper.py --resolve-url /some/slug` 获取对应的mdx文件路径
2. 如果是相对链接，则先转为相对于workspace根目录的相对路径
3. 使用 `python3 .claude/plugins/write-zego-docs/skills/link-check/scripts/anchor_helper.py check <文件路径> <锚点名>` 检查锚点是否有效

如何查找可能正确的锚点：
1. 先调用 `python3 .claude/plugins/write-zego-docs/skills/link-check/scripts/anchor_helper.py headings <文件路径>` 获取所有标题
2. 从所有标题中选出与锚点名含义最接近的标题，如果所有 heading 都与锚点名含义不接近，直接返回空。
3. 如果找到了与锚点名含义最接近的标题，则先把锚点名改为符合规则的小写英文加连接符的形式
4. 使用 `python3 .claude/plugins/write-zego-docs/skills/link-check/scripts/anchor_helper.py generate <相对workspace的文件路径> <标题> <锚点名>` 在目标文件中生成锚点，并返回生成的锚点名

## 输出格式

检查完成后，按以下格式输出结果：

```markdown
## 链接检查结果

### ✅ 链接检查通过
共检查 N 个链接，全部有效。

### ❌ 无效链接
|无效链接|可能正确的链接|
|---------|---------------|
| ./path/to/wrong_file.mdx | ./path/to/correct_file.mdx |
| /some/wrong_slug | /some/correct_slug |
| #some-wrong-anchor | #some-correct-anchor |

### ⚠️ 中英文混用问题
1. [链接文本](链接地址) - 中文文档包含英文站链接
```

> **注意**：当所有链接都有效时，使用"✅ 链接检查通过"汇总形式，无需逐条列出有效链接。
