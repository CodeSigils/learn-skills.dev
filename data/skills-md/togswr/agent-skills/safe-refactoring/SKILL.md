---
name: safe-refactoring
description: |
  コードスメルの検出、安全なリファクタリング手順の設計、レガシーコード改善を行う。
  リファクタリング計画の作成、テストなしコードの段階的改善、Tidy First?による日常的な整頓、
  大規模リファクタリング戦略の選定が必要な場合に使用する。
---

# Safe Refactoring

権威ある書籍に基づいた安全なリファクタリングの原則と手法。状況に応じた判断フローで適切なアプローチを選択する。

## 基本原則 (MUST)

### 1. リファクタリングの定義

> "Refactoring is a disciplined technique for restructuring an existing body of code, altering its internal structure without changing its external behavior."
> — Martin Fowler

- 外部から見た振る舞いを変えずに、内部構造を改善する
- パフォーマンス最適化ではない（構造の改善が目的）
- 機能追加ではない（振る舞いは変わらない）

### 2. 2つの帽子 (Two Hats)

**リファクタリングと機能追加を同時に行わない。**

| 帽子 | 目的 | テスト |
|-----|------|-------|
| リファクタリング | 構造改善 | 既存テストが通り続ける |
| 機能追加 | 振る舞い変更 | 新しいテストを追加 |

頻繁に帽子を切り替えるが、**同時には被らない**。

### 3. 小さなステップの原則

- 各ステップでコンパイル・テストが通る状態を維持
- 1つのリファクタリングを完了してから次へ
- 問題があればすぐに元に戻せる粒度で進める

### 4. テストファーストの原則

- リファクタリング前にテストが存在することを確認
- テストがなければ、まず特性テストを追加（→ `templates/characterization-test.md`）
- テストを安全網として活用

### 5. コミット戦略

- リファクタリングごとに小さなコミット
- 機能追加とリファクタリングは別コミット
- メッセージで「refactor:」などのプレフィックスを使用

## 状況判断フロー

リファクタリング作業を始める前に、以下のフローで適切なアプローチを選択する。

```
テストがあるか？
├─ Yes → 変更規模は？
│        ├─ 小さい整頓（数分〜1時間）→ 「Tidy First? アプローチ」へ
│        ├─ 中規模の改善（数日）      → 「通常リファクタリング」へ
│        └─ 大規模な移行（数週間〜）  → 「大規模リファクタリング戦略」へ
└─ No → 「レガシーコード対応」へ（まずテストを配置する）
```

### コードスメルを起点にする場合

コードスメル（問題の兆候）が見つかったら `references/code-smells.md` で該当するスメルを特定し、推奨される対策リファクタリングを `references/refactoring-catalog.md` で確認する。

## 通常リファクタリング

テストが存在する状態で行う標準的なリファクタリング。タイミングに応じて4種類に分かれる。

- **Preparatory**（準備的）: 機能追加を容易にするために、先に構造を整える
- **Comprehension**（理解促進）: コードを理解する過程で、その理解をコードに固定化する
- **Litter-Pickup**（ゴミ拾い）: 小さな改善を見つけたら、すぐに直す（Boy Scout Rule）
- **Rule of Three**: 同じことを3回繰り返したら、共通化を検討する

具体的なリファクタリング手法は `references/refactoring-catalog.md` を参照。

## Tidy First? アプローチ (Kent Beck)

小さな整頓（Tidying）をいつ行うかの判断フレームワーク。

| 選択 | 判断基準 |
|------|---------|
| **First** | 整頓で直後の変更が著しく容易になる場合 |
| **After** | 変更後に構造改善の機会が見える場合 |
| **Later** | 今は価値がないが将来的に有益な場合 |
| **Never** | コストが利益を上回る場合 |

> "Structure changes are reversible. Behavior changes are not." — Kent Beck

- 構造変更（リファクタリング）は可逆的 → 軽い精査で十分
- 振る舞い変更は不可逆的 → 慎重な検討が必要
- **同一のPR/コミットに混在させない**

15のTidyingsの詳細と経済的判断基準は `references/tidy-first.md` を参照。

## レガシーコード対応

> "Legacy code is simply code without tests." — Michael Feathers

テストのないコードを変更する手順（Legacy Code Change Algorithm）:

1. **Identify change points** - 変更が必要な箇所を特定
2. **Find test points** - テストを追加できる箇所を探す
3. **Break dependencies** - Seamsを使って依存関係を断ち切る
4. **Write tests** - 特性テストを追加
5. **Make changes and refactor** - 変更とリファクタリング

### 安全な拡張パターン

レガシーコードを直接変更せず、安全に拡張する手法:

| パターン | 用途 |
|---------|------|
| Sprout Method | 新機能を新メソッドとして追加 |
| Sprout Class | 新機能を新クラスとして追加 |
| Wrap Method | 既存メソッドをラップして前後に処理追加 |
| Wrap Class | Decoratorパターンで拡張 |

依存関係解消テクニック、Seamsの詳細は `references/legacy-techniques.md` を参照。
特性テスト作成の手順は `templates/characterization-test.md` を参照。

## 大規模リファクタリング戦略

| パターン | 用途 | 時間目安 |
|---------|------|---------|
| Boy Scout Rule | 小さなコード改善 | 数分 |
| Branch by Abstraction | モジュール/ライブラリの置き換え | 数日〜数週間 |
| Parallel Change | API変更（後方互換性必要） | 数週間 |
| Strangler Fig | レガシーシステム全体の置き換え | 数ヶ月 |

各パターンの詳細と適用手順は `references/large-scale-refactoring.md` を参照。

## アンチパターン (MUST NOT)

- **Big Bang Refactoring**: 大規模な書き直しを一度に行わない。段階的な改善、Strangler Fig Patternで代替する
- **機能追加との混在**: 同一コミットでリファクタリングと機能追加を混ぜない。レビューと問題切り分けが困難になる
- **テストなしでの大規模変更**: まずテストを追加してから変更する。テスト追加が困難なら依存関係を断ち切る
- **過度な抽象化 (Speculative Generality)**: 将来の要件を予測した過剰な設計を避ける。具体的なニーズが3回出てから抽象化する

## テンプレート

- [リファクタリング計画](templates/refactoring-plan.md) - 中〜大規模リファクタリングの計画立案用
- [特性テスト作成ガイド](templates/characterization-test.md) - レガシーコードの現在の振る舞いを記録するテスト作成用

## 参照資料

- [コードスメルカタログ](references/code-smells.md) - Fowler 24のコードスメルと対策
- [Clean Codeヒューリスティクス](references/clean-code-heuristics.md) - Clean Code 63のスメルとFowler対応
- [リファクタリングカタログ](references/refactoring-catalog.md) - 主要リファクタリング手法一覧
- [レガシーコード対応テクニック](references/legacy-techniques.md) - 依存関係解消、Seams、特性テスト
- [Tidy First? アプローチ](references/tidy-first.md) - 15のTidyingsと経済的判断基準
- [大規模リファクタリング戦略](references/large-scale-refactoring.md) - Strangler Fig, Branch by Abstraction等
