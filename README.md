# K8sプラットフォームドキュメントサイト

このリポジトリは、Kubernetesプラットフォーム向けドキュメントサイトの具体サンプルです。

`docs/` 配下のMarkdownを正本とし、Blumeで人間向けサイト、`llms.txt`、MCP endpointを生成します。サーバコンテナは1つだけです。BlumeのNode serverがサイトと `/mcp` を同時に配信します。

## 目的

- 人間が読みやすいプラットフォームドキュメントサイトを作る。
- AIエージェントがMCP経由で同じドキュメントを検索・取得できるようにする。
- 依存ライブラリのインストール、ビルド、検証をコンテナ内に閉じる。
- Markdownの構造とfrontmatterを直すだけで、検索とAI向けindexが更新される状態にする。

## ローカルでの使い方

ホストにNode.js packageを入れないでください。DockerまたはPodman経由でビルドして実行します。

```bash
make image
make run
```

Podmanを使う場合:

```bash
make CONTAINER=podman image
make CONTAINER=podman run
```

起動後に確認するURL:

- `http://localhost:4321/`
- `http://localhost:4321/mcp`
- `http://localhost:4321/.well-known/mcp.json`
- `http://localhost:4321/llms.txt`

## 検証

Blumeのstrict buildを実行します。

```bash
make validate
```

MCPの日本語検索を検証します。

```bash
make test-mcp-search
```

Podmanを使う場合:

```bash
make CONTAINER=podman validate
make CONTAINER=podman test-mcp-search
```

`test-mcp-search` はコンテナbuild内でBlume serverを起動し、`/mcp` の `search_docs` toolに日本語queryを投げます。次のような検索語で期待するページが返ることを確認します。

| query | 期待するroute |
| --- | --- |
| `本番` | `/environments/production` |
| `デプロイ` | `/procedures/deploy-application` |
| `命名` | `/constraints/naming-conventions` |
| `ロールバック` | `/procedures/rollback` |

## AI/MCP設計

MCPはBlume内蔵MCP serverを使います。日本語検索を有効にするため、`blume.config.ts` では `i18n.defaultLocale: "ja"` を設定しています。

使う入口:

| endpoint | 用途 |
| --- | --- |
| `/mcp` | AIエージェント向けMCP endpoint |
| `/.well-known/mcp.json` | MCP endpoint discovery |
| `/llms.txt` | AI向け軽量index |

サーバは1コンテナです。Nginxコンテナ、Python MCP sidecar、別検索サーバは使いません。

## 執筆フロー

1. `docs/` 配下のMarkdownを編集する。
2. 必須frontmatterを更新する。
3. チェックリスト項目は、正本となる制約ページまたは手順ページへリンクする。
4. `make validate` でBlume strict buildを実行する。
5. `make test-mcp-search` でMCP日本語検索を確認する。
6. イメージをビルドして、サイトを再生成する。

## ドキュメント運用ルール

執筆ルールと運用ルールは [ドキュメント運用ルール](docs/operations/document-operations.md) を参照してください。

現在の自動検証はBlume strict buildとMCP検索smoke testです。frontmatter policyやlink policyをさらに厳密化する場合は、Blumeのcontent処理またはBlume向けvalidatorとして追加します。

## 主要ドキュメント

- [要件とアーキテクチャ](docs/design/requirements-and-architecture.md)
- [AIエージェント向けアクセス設計](docs/design/ai-agent-access-plan.md)
- [ドキュメント運用ルール](docs/operations/document-operations.md)
- [ページテンプレート](docs/authoring/page-template.md)
