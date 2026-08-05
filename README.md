# K8sプラットフォームドキュメントサイト

このリポジトリは、Kubernetesプラットフォーム向けドキュメントサイトの具体サンプルです。

`docs/` 配下のMarkdownを正本とします。デフォルトのビルドはMkDocsサイトを生成し、Nginxで配信します。Blume.dev版は、人間向けサイトとBlume内蔵MCP serverを同じNode serverで配信するターゲットとして試作実装しています。

## 目的

- 人間が読みやすいプラットフォームドキュメントサイトを作る。
- 依存ライブラリのインストールとビルドをコンテナ内に閉じる。
- Blume内蔵MCP serverからも検索しやすいように、Markdown構造とfrontmatterを整理しておく。

## ローカルでの使い方

ホストにMkDocsやPythonパッケージを入れないでください。Docker経由でビルドして実行します。

### MkDocs版

通常はこちらを使います。`docker/Dockerfile` でMkDocsサイトをビルドし、Nginxで `8080` に配信します。

```bash
make image
make run
```

ドキュメント検証だけを実行する場合:

```bash
make validate
```

Podmanを使う場合:

```bash
make CONTAINER=podman image
make CONTAINER=podman run
make CONTAINER=podman validate
```

起動後に確認するURL:

- `http://localhost:8080/`

### Blume.dev版

Blume.dev版を確認する場合だけ、明示的に `blume-*` ターゲットを使います。`docker/Dockerfile.blume` でBlumeのNode serverをビルドし、サイトとMCP endpointを `4321` に配信します。

```bash
make blume-image
make blume-run
```

Podmanを使う場合:

```bash
make CONTAINER=podman blume-image
make CONTAINER=podman blume-run
make CONTAINER=podman blume-validate
```

起動後に確認するURL:

- `http://localhost:4321/`
- `http://localhost:4321/mcp`

### AI/MCP試作

MCPはBlume.dev版の内蔵MCP serverを使います。日本語検索を有効にするため、`blume.config.ts` では `i18n.defaultLocale: "ja"` を設定しています。

現時点のターゲットの使い分け:

| target | 内容 |
| --- | --- |
| `make image` / `make run` | MkDocs版 |
| `make blume-image` / `make blume-run` | Blume.dev版とBlume内蔵MCP server |

## 執筆フロー

1. `docs/` 配下のMarkdownを編集する。
2. 必須frontmatterを更新する。
3. チェックリスト項目は、正本となる制約ページまたは手順ページへリンクする。
4. `make validate` でドキュメント運用ルールを検証する。
5. イメージをビルドして、サイトを再生成する。

## ドキュメント検証

validatorの仕様は [validate_docs.py](tools/document-validator/validate_docs.py) に直接実装しています。

検出できるもの:

- 必須frontmatterの不足
- `id`、`type`、`owner`、`status`、`review_cycle` の不正値
- `id` とMarkdown pathの不一致
- `canonical_url` とMarkdown pathの不一致
- `id` または `canonical_url` の重複
- `last_reviewed` の形式不正、未来日、review期限切れ
- pageが `mkdocs.yml` の `nav` に含まれていない状態
- H1がない、H1が複数ある、H1とfrontmatter `title` が一致しない状態
- checklist pageの各行が正本ドキュメントへlinkしていない状態
- 存在しないMarkdown link
- deprecated pageに `replaced_by` がない状態

AI/RAG向けartifact生成とMCP serverは試作実装です。MCPはBlume内蔵MCP serverへ寄せています。設計方針は [AIエージェント向けアクセス設計](docs/design/ai-agent-access-plan.md) を参照してください。

## 主要ドキュメント

- [要件とアーキテクチャ](docs/design/requirements-and-architecture.md)
- [ドキュメント運用ルール](docs/operations/document-operations.md)
- [ページテンプレート](docs/authoring/page-template.md)
