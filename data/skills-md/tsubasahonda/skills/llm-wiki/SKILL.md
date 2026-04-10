---
name: llm-wiki
description: 永続的な markdown wiki を LLM が保守する workflow。調査メモ、読書ノート、競合分析、project wiki、Obsidian 連携 wiki を育てるときに使う。既存 vault や既存ノートは read-only source として扱い、LLM の write 先は setup で確定した category-first な `wiki/` 配下に限定する。複数 project が同じ wiki を共有する場合は、カテゴリ分類と project affinity を分けて管理する。
---

# LLM Wiki

RAG のように毎回 raw source から答えを組み立てるのではなく、LLM が保守する wiki を知識の中間層として育てる。

## 基本原則

- raw source は読めても書き換えない
- 既存の vault / ノート群は source 扱いとし、LLM は更新しない
- write 先は setup で確定した `wiki/` 配下の category-first 構造だけに限定する
- source / concept / analysis は主題カテゴリへ保存する
- project ごとの強い導線は `wiki/projects/` で管理する
- `index.md` と `log.md` を必須で維持する
- query の有用な結果は chat で終わらせず wiki に昇格させる

## 開始ルール

- この skill は常に `setup` フェーズから開始する
- 初回 setup では、最初のアクションとしてユーザーに `storage_mode` を確認する
- 初回 setup で確認する質問は最低でも「repo-local で管理するか」「obsidian-vault を source of truth にするか」の 2 択を含める
- 初回 setup では、ユーザー回答または既存設定ファクトを得る前に setup コマンドを実行してはいけない
- `wiki/references/setup.md` が存在しない、または必須項目が未確定なら setup 未完了とみなす
- setup 未完了の状態では ingest / query / lint の運用フェーズへ進まない
- 既存 wiki がある場合も、最初に `wiki/references/setup.md` を読んで現在の決定事項を確認する
- `storage_mode` は setup の最初に確定する必須項目であり、未確定のまま `setup.sh` / `connect-obsidian.sh` / wiki 配下への write を行ってはいけない
- `setup.sh` が使えるからという理由だけで `repo-local` を選んではいけない
- `wiki/references/setup.md` がない初回セットアップでは、まず「repo-local か obsidian-vault か」をユーザーに確認して確定し、その後に初期化コマンドを選ぶ
- 既存の外部 wiki owner を repo やノートから確認できない場合は、`storage_mode` を推測で埋めずユーザーに確認して停止する

## 推奨構成

- `wiki/raw/`: immutable source of truth
- `wiki/index.md`: wiki 全体の入口
- `wiki/log.md`: append-only の操作ログ
- `wiki/overview.md`: 全体方針
- `wiki/projects/index.md`: project 一覧
- `wiki/projects/<project>.md`: project ごとの入口
- `wiki/references/`: 運用ルール、構造メモ、既存 vault の map
- `wiki/<category>/index.md`: カテゴリ入口
- `wiki/<category>/overview.md`: カテゴリ俯瞰
- `wiki/<category>/sources/`, `entities/`, `concepts/`, `analyses/`

詳しい構成は `references/structure.md` を読む。

## セットアップ

setup で最低限決めること:

- `storage_mode`: `repo-local` か `obsidian-vault`
- `wiki_root`: 実際の write target path
- `categories`: 初期カテゴリ一覧
- `read_only_sources`: 既存 vault / ノート / repo のどこを source 扱いにするか
- `projects`: project page を作る対象と命名規約
- `frontmatter`: `domain`, `projects`, `project_affinity` などの必須 metadata
- `assets`: 添付ファイルと画像の保存先

setup の流れ:

1. ユーザーに `storage_mode` を確認する
2. `storage_mode` に応じた owner path を確定する
3. `wiki_root` と `read_only_sources` を決める
4. `categories` と project 命名規約を決める
5. frontmatter / assets の運用を決める
6. `storage_mode` が `repo-local` なら `setup.sh`、`obsidian-vault` なら `connect-obsidian.sh` を実行する
7. 決定事項を `wiki/references/setup.md` に記録する

初回 setup の既定動作:

- 既定で `repo-local` を選ばない
- 既定で `obsidian-vault` を選ばない
- 既存の `wiki/references/setup.md` や明示的な運用ファクトがない限り、ユーザー確認なしで先へ進まない

`wiki/references/setup.md` が埋まるまでは、この skill を通常運用に入れてはいけない。

禁止事項:

- `storage_mode` 未確定のまま `bash .../setup.sh ./wiki ...` を実行しない
- 初回 setup で `repo-local` / `obsidian-vault` の確認を飛ばさない
- `wiki/references/setup.md` 不在時に `repo-local` を既定値として採用しない
- `setup.md` に `obsidian-vault` と書かれているのに repo 配下 `./wiki` へ書かない
- setup の選択根拠を残さず ingest を始めない

```bash
bash skills/llm-wiki/scripts/setup.sh [WIKI_DIR] [CATEGORIES_CSV]
# 例:
# bash skills/llm-wiki/scripts/setup.sh ./wiki engineering,llm,finance
```

repo 内で管理する場合はこのスクリプトを使う。`raw/`, `references/`, `projects/` と、カテゴリごとの雛形に加え、`references/setup.md` のテンプレートを作る。既存ファイルはスキップする。

このコマンドを使ってよいのは `storage_mode: repo-local` を明示確定した後だけ。

## Obsidian 連携

- setup で `storage_mode: obsidian-vault` を選んだ場合に使う
- source of truth は Obsidian vault 配下の shared `wiki/`
- project repo 側は source であり、wiki の owner ではない
- project ごとの導線は `wiki/projects/<project>.md` と frontmatter で管理する

```bash
bash skills/llm-wiki/scripts/connect-obsidian.sh init <VAULT_DIR> [WIKI_SUBDIR] [CATEGORIES_CSV]
```

Obsidian 連携の考え方は `references/obsidian.md` を読む。

このコマンドを使ってよいのは `storage_mode: obsidian-vault` を明示確定した後だけ。

## source の取り込み

- 通常の Web: WebFetch
- X: `scripts/fetch-x.sh`
- ローカル HTML: `scripts/extract-html.py`
- 画像保存: `scripts/download-images.py`

画像は URL 参照で放置せずローカル保存する。

## project affinity

カテゴリ共有では source が混在する。混在は許容するが、project 由来 source は project 内で優先的に辿れるようにする。

- 保存先カテゴリは常に主題で決める
- project 由来 source には frontmatter で `projects` を持たせる
- `wiki/projects/<project>.md` を作り、関連 source / concept / analysis / entity を横断リンクする
- project に強く紐づく query は、まず `wiki/projects/<project>.md` を読む
- 同じ source が複数 project に効く場合は `projects: [a, b]` とする

推奨 frontmatter:

```yaml
domain: engineering
projects:
  - example-project
source_type: clipping
project_affinity: primary
```

`project_affinity` は `primary` / `secondary` / `shared` を使う。

## ingest フロー

1. source を取得する
2. 画像があればローカル保存する
3. 適切なカテゴリを 1 つ決める
4. `wiki/<category>/sources/` に source summary を作る
5. 関連する entity / concept / overview を更新する
6. project 由来なら `projects` frontmatter を付け、`wiki/projects/<project>.md` を更新する
7. `wiki/<category>/index.md` と必要なら `wiki/index.md` / `wiki/projects/index.md` を更新する
8. `wiki/log.md` に追記する

複数 source を扱うときは、source 取得は並列でよいが wiki への書き込みは 1 source ずつ直列で行う。

## query フロー

1. `wiki/references/setup.md` を読み、write target と分類規約を確認する
2. project 文脈がある場合は `wiki/projects/<project>.md` を先に読む
3. `wiki/index.md` からカテゴリを特定する
4. `wiki/<category>/index.md` を読んで関連ページを絞る
5. 必要なページだけ読む
6. 回答が再利用価値を持つなら `wiki/<category>/analyses/` へ保存し、project 由来なら project page にも反映する

## lint 観点

- `wiki/references/setup.md` が存在し、運用実態と一致しているか
- orphan page がないか
- 重要概念に未作成ページがないか
- cross link が不足していないか
- 既存 vault を write 対象にしていないか
- project 由来 source が project page から辿れるか

元の発想は `references/origin.md` を参照する。
