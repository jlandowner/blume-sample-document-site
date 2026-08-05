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

### MCPクライアント設定

BlumeのMCP endpointはStreamable HTTPで公開されます。ローカル起動時に手動で接続する場合は、次のURLを登録します。

```text
http://localhost:4321/mcp
```

Blume公式の接続例は、HTTP transportを指定して `/mcp` を登録する形式です。このリポジトリをローカル起動した場合は次のようになります。

```bash
claude mcp add --transport http k8s-platform-docs http://localhost:4321/mcp
```

MCP clientがwell-known discoveryに対応している場合は、公開サイトのroot URLを登録します。discovery documentは次のURLで確認できます。

```text
https://docs.example.internal/.well-known/mcp.json
```

ローカルでも `http://localhost:4321/.well-known/mcp.json` は取得できます。ただし、このファイル内のendpoint URLは `blume.config.ts` の `deployment.site` から生成されるため、デフォルトでは `https://docs.example.internal/mcp` を指します。ローカル検証では discovery ではなく、`http://localhost:4321/mcp` を直接登録してください。

MCP clientが手動設定を要求する場合は、client固有の設定ファイルにStreamable HTTP transportとして `/mcp` を登録します。設定キー名はclientごとに異なるため、次の形を目安にしてください。

```json
{
  "mcpServers": {
    "k8s-platform-docs": {
      "transport": "streamable-http",
      "url": "http://localhost:4321/mcp"
    }
  }
}
```

接続確認は `search_docs` toolで行います。

```bash
curl -s http://localhost:4321/mcp \
  -H 'accept: application/json, text/event-stream' \
  -H 'content-type: application/json' \
  --data '{"id":1,"jsonrpc":"2.0","method":"tools/call","params":{"name":"search_docs","arguments":{"query":"デプロイ","limit":5}}}'
```

代表的なtool:

| tool | 用途 |
| --- | --- |
| `search_docs` | queryから関連ページ候補を検索する |
| `get_page` | routeを指定してMarkdown本文を取得する |
| `list_pages` | ページ一覧を取得する |
| `get_navigation` | navigation treeを取得する |

参照:

- [Blume公式サイト](https://useblume.dev/) は、MCP serverが `search_docs`、`get_page`、`list_pages`、`get_navigation` の4つのread-only toolsを公開し、`claude mcp add --transport http ... /mcp` で接続する例を示しています。
- [MCP Streamable HTTP transport仕様](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports) は、MCP endpointがHTTP POSTを受け、`Accept: application/json, text/event-stream` を使うことを定義しています。
- Blumeが生成するserver cardは `/.well-known/mcp/server-card.json` で確認できます。

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
