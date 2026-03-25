---
name: dispatch
description: ユーザーがタスク一覧に対して実装を求めてきた際に参照するスキル。複数のイシューを同時に取り組むためのワークフロー。
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent, Skill
---

# Dispatch

GitHub Issues と PR を triage → tasks → reviews の流れで処理する。
サブコマンドを指定すると該当フェーズだけ実行し、省略すると全フェーズを順に実行する。

## dispatch triage

まだトリアージラベルがついていない Issue 一覧を確認し、以下のいずれかに振り分けてラベルを付与する:

- **needs-refinement** — 要件が曖昧でユーザーの判断待ちの分岐がある
- **needs-investigation** — 方針を決めるために調査が必要
- **needs-alignment** — エージェントが自律的に判断できない意思決定事項がある（利用は最小限にすること）
- **ready-to-implement** — 何を作る・変更するかが一意に解釈でき、完了条件が明確

## dispatch tasks

以下の両方を並列で行う:

### needs-investigation ラベルの Issue

- `needs-investigation`ラベルの Issue を抜き出す
- Agent ツールで並列に調査を開始する
- 調査内容を Issue にコメントとして残す
- 調査が完了したら`needs-investigation`ラベルを剥がし、トリアージを再実行して適切なラベル（ready-to-implement etc.）を付与する

### needs-alignment ラベルの Issue

- `needs-alignment`ラベルの Issue を抜き出す
- Issue コメントまたは本文に、ユーザーに決めてほしい事項を**明確な選択肢**として提示する
- ユーザーからのフィードバック・意思決定を受けたら、以下のいずれかに遷移する:
  - 方針が確定 → `needs-alignment`ラベルを剥がし、トリアージを再実行して適切なラベルを付与する
  - さらなるリファインが必要 → `needs-refinement`ラベルに変更する
  - 追加調査が必要 → `needs-investigation`ラベルに変更する

### ready-to-implement ラベルの Issue

- `ready-to-implement`ラベルの Issue を抜き出す
- Agent ツール + `isolation: "worktree"` で並列に実装を開始する
- 各 Agent には以下を指示:
  - 対象 Issue の番号・内容・完了条件
  - 実装後に commit & push し、`Closes #<number>` を含む PR を作成すること

## dispatch reviews

2段階で処理する:

### 1. レビュー

- open な PR 一覧を確認する
- Agent ツールと `/review` skill を使って並列にレビューを開始する
  - 注意: skill 名は `review` であり、`review-pr` など類似名と間違えないこと
- レビュー内容を PR コメントとして反映したら完了

### 2. レビュー指摘の修正

- 上記レビューがすべて完了したら、修正が必要な PR について Agent ツール + `isolation: "worktree"` で並列に修正を行う
