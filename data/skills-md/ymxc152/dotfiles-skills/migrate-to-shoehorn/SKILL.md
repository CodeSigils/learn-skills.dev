---
name: migrate-to-shoehorn
description: 将测试文件从 `as` 类型断言迁移到 @total-typescript/shoehorn。当用户提到 shoehorn、想替换测试中的 `as`，或需要部分测试数据时使用。
---

# Migrate to Shoehorn（迁移到 Shoehorn）

## Why shoehorn?（为什么用 shoehorn？）

`shoehorn` 让你在测试中传递部分数据，同时保持 TypeScript 满意。它用类型安全的替代方案替换 `as` 断言。

**仅限测试代码。** 永远不要在生产代码中使用 shoehorn。

测试中 `as` 的问题：

- 训练有素不去使用它
- 必须手动指定目标类型
- 对于故意错误的数据需要双重 `as`（`as unknown as Type`）

## Install（安装）

```bash
npm i @total-typescript/shoehorn
```

## Migration patterns（迁移模式）

### 大对象中只有少数需要的属性

Before：

```ts
type Request = {
  body: { id: string };
  headers: Record<string, string>;
  cookies: Record<string, string>;
  // ...20 more properties
};

it("gets user by id", () => {
  // Only care about body.id but must fake entire Request
  getUser({
    body: { id: "123" },
    headers: {},
    cookies: {},
    // ...fake all 20 properties
  });
});
```

After：

```ts
import { fromPartial } from "@total-typescript/shoehorn";

it("gets user by id", () => {
  getUser(
    fromPartial({
      body: { id: "123" },
    }),
  );
});
```

### `as Type` → `fromPartial()`

Before：

```ts
getUser({ body: { id: "123" } } as Request);
```

After：

```ts
import { fromPartial } from "@total-typescript/shoehorn";

getUser(fromPartial({ body: { id: "123" } }));
```

### `as unknown as Type` → `fromAny()`

Before：

```ts
getUser({ body: { id: 123 } } as unknown as Request); // wrong type on purpose
```

After：

```ts
import { fromAny } from "@total-typescript/shoehorn";

getUser(fromAny({ body: { id: 123 } }));
```

## When to use each（何时使用哪个）

| Function        | Use case（使用场景）                               |
| --------------- | -------------------------------------------------- |
| `fromPartial()` | 传递仍然类型检查通过的部分数据                     |
| `fromAny()`     | 传递故意错误的数据（保留自动补全）                 |
| `fromExact()`   | 强制完整对象（稍后与 fromPartial 交换）            |

## Workflow（工作流）

1. **Gather requirements（收集需求）** — 询问用户：
   - 哪些测试文件的 `as` 断言造成了问题？
   - 它们是否处理只有部分属性重要的大对象？
   - 他们是否需要为错误测试传递故意错误的数据？

2. **Install and migrate（安装并迁移）**：
   - [ ] 安装：`npm i @total-typescript/shoehorn`
   - [ ] 查找带 `as` 断言的测试文件：`grep -r " as [A-Z]" --include="*.test.ts" --include="*.spec.ts"`
   - [ ] 将 `as Type` 替换为 `fromPartial()`
   - [ ] 将 `as unknown as Type` 替换为 `fromAny()`
   - [ ] 添加来自 `@total-typescript/shoehorn` 的 imports
   - [ ] 运行类型检查验证
