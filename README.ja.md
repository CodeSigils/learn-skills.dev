<div align="center">

<h1><a href="https://www.learn-skills.dev">learn-skills.dev</a></h1>

<p>厳選された高品質な AI エージェント向けスキル。検索・インストール・コピー・共有ができます。<br>
Claude Code、Cursor、OpenClaw、その他の AI コーディングツールと連携します。</p>

<p><strong>Web アプリ:</strong> <a href="https://www.learn-skills.dev">https://www.learn-skills.dev</a> — AI エージェントスキルの検索・インストール・コピー・共有。</p>

<p>
<a href="./README.md">English</a> | <a href="./README.zh.md">简体中文</a> | <a href="./README.tw.md">繁體中文</a> |
日本語 |
<a href="./README.ko.md">한국어</a> |
<a href="./README.fr.md">Français</a> |
<a href="./README.de.md">Deutsch</a> |
<a href="./README.es.md">Español</a> |
<a href="./README.it.md">Italiano</a> |
<a href="./README.ru.md">Русский</a> |
<a href="./README.ar.md">العربية</a>
</p>

</div>

## データソース

### 現在のプロバイダー

- **[skills.sh](https://skills.sh)** — コミュニティがキュレーションしたスキルランキング
  - All Time (`/`) — 累計インストール数ランキング
  - Trending (`/trending`) — 直近の伸びランキング
  - Hot (`/hot`) — 日次インストール数ランキング

### 予定しているプロバイダー

- **GitHub Trending** — GitHub 上の人気スキルリポジトリ
- **Awesome Lists** — AI エージェントスキル向けの awesome-* リスト

### 手動スキル

どのプロバイダーにも載っていないスキルは、`data/manual_skills.json` から手動で追加できます。

```json
{
  "skills": [
    {
      "source": "owner/repo",
      "skillId": "skill-name",
      "name": "Skill Display Name",
      "installs": 1
    }
  ]
}
```

手動スキルは次のようになります。

- GitHub から `SKILL.md` を取得（標準的なスキルフォルダ検出）
- `skills_index.json` に `providerId: "manual"` で含まれる
- クローラーで**上書きされない**（実行をまたいで保持）
- **重複排除**: 後から skills.sh が同じスキルを追跡した場合は skills.sh のデータを使用

注意: `installs` は少なくとも 1（最小値）にしてください。

## 出力ファイル

クローラーは `data/` ディレクトリにファイルを生成します。

### `data/skills.json`

3 つのランキングを含む完全なスキルデータ。

```json
{
  "updatedAt": "2024-01-27T00:00:00.000Z",
  "allTime": [...],
  "trending": [...],
  "hot": [...]
}
```

### `data/skills_index.json`

*すべて*のスキル向けのサイト用インデックス（`data/skills.json` から構築）。

- `data/skills-md/` にキャッシュされた `SKILL.md` がある場合、`description` は `description_en.txt` への**パス**
- サイトが全文 Markdown を取得・表示できるよう `skillMdPath` を含む
- `id`（`<source>/<skillId>`）で**重複排除**。上流に重複がある場合は `installsAllTime` が最大のエントリを残す

### `data/feed.json`

簡易フィード形式（各ランキング上位 50 件）。

対応する GitHub の `SKILL.md`（`data/skills-md/` にキャッシュ）を取得して各項目に `description` を付与しようとします。

```json
{
  "title": "Skills Feed",
  "description": "Aggregated AI agent skills from multiple sources",
  "link": "https://github.com/user/skills_feed",
  "updatedAt": "2024-01-27T00:00:00.000Z",
  "topAllTime": [...],
  "topTrending": [...],
  "topHot": [...]
}
```

### `data/skills-md/`

GitHub から取得してキャッシュした `SKILL.md`。よくあるパス例:

- `skills/<skillId>/SKILL.md`（最も多い）
- `.claude/skills/<skillId>/SKILL.md`
- `.cursor/skills/<skillId>/SKILL.md`
- `.codex/skills/<skillId>/SKILL.md`
- `plugins/<plugin-name>/skills/<skillId>/SKILL.md`（プラグイン型リポジトリで多い、例: Expo）

`SKILL.md` がある場合、クローラーは次も生成します。

- `description_en.txt`（利用可能なら SKILL.md の frontmatter の `description` から抽出）

既定では、日次ジョブを速く保つため、トップリストに載るスキルの `SKILL.md` のみ取得します。

`data/skills.json` の*すべて*のスキルを同期するには:

```bash
SYNC_ALL_SKILL_MDS=1 bun run crawl
```

### `data/feed.xml`

RSS 2.0（XML）。RSS リーダー／購読用。

- 現在のクロール結果と直前の `data/feed.json` から生成
- スパムを避けるため、意味のある変更（新規エントリ／順位の大きな変動）のみ公開

## 使い方

### ローカル開発

```bash
# 依存関係のインストール
bun install

# クローラーの実行
bun run crawl
```

ヒント: GitHub 上の `SKILL.md` をより広く取得したい場合（`plugins/*/skills/...` などプラグイン形式のパスを含む）、  
GitHub API のレート制限を避けるために `GITHUB_TOKEN` を設定してください。

```bash
export GITHUB_TOKEN=ghp_xxx
bun run crawl
```

### GitHub Actions

GitHub にプッシュすると、クローラーは次のように動きます。

1. 毎日 UTC 0:00 に自動実行
2. 手動トリガー可能（Actions タブの「Run workflow」）
3. `main` ブランチへのプッシュ時に自動実行

## サイトでの利用

GitHub の Raw URL から直接データを取得できます。

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/skills.json
```

または jsDelivr CDN（多くの場合高速）:

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/skills.json
```

### RSS 購読（推奨）

RSS フィードを購読:

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/feed.xml
```

jsDelivr 経由:

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/feed.xml
```

### コード例

```typescript
// Next.js の例
const SKILLS_DATA_URL = 'https://cdn.jsdelivr.net/gh/your-username/skills-crawler@main/data/skills.json';

export async function getSkillsData() {
  const res = await fetch(SKILLS_DATA_URL, {
    next: { revalidate: 3600 } // 1 時間ごとに再検証
  });
  return res.json();
}
```

## 注意

- データは毎日更新されます
- 各プロバイダーの利用規約を遵守してください
- 個人の学習・研究目的のみ

## 推奨ツール

learn-skills のアウトプット（メモ、要約、データなど）を AI プレゼンツールと組み合わせると、共有しやすいスライドにすばやくできます。

**ワークフローを強化**  
learn-skills の結果をプロ品質のスライドに？PopAi でワンクリック AI プレゼン生成を試してください：  
[https://www.popai.pro](https://www.popai.pro)

## コントリビューション

新しいスキルソースを追加したいですか？PR 歓迎です。既存のプロバイダー実装を参照してください。
