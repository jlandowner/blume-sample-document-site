# K8sプラットフォームドキュメントサイト

このリポジトリは、Kubernetesプラットフォーム向けドキュメントサイトの具体サンプルです。

`docs/` 配下のMarkdownを正本とします。コンテナビルドの中でMkDocsサイトをビルドし、Nginxで配信します。

## 目的

- 人間が読みやすいプラットフォームドキュメントサイトを作る。
- 依存ライブラリのインストールとビルドをコンテナ内に閉じる。
- 将来のMCP/RAG連携に備え、Markdown構造とfrontmatterを整理しておく。

## ローカルでの使い方

ホストにMkDocsやPythonパッケージを入れないでください。Docker経由でビルドして実行します。

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

- `http://localhost:8080/`

## 執筆フロー

1. `docs/` 配下のMarkdownを編集する。
2. 必須frontmatterを更新する。
3. チェックリスト項目は、正本となる制約ページまたは手順ページへリンクする。
4. イメージをビルドして、サイトを再生成する。

frontmatter検証、AI/RAG向けartifact生成、MCP serverは次の検討事項です。

## 主要ドキュメント

- [要件とアーキテクチャ](docs/design/requirements-and-architecture.md)
- [ドキュメント運用ルール](docs/operations/document-operations.md)
- [ページテンプレート](docs/authoring/page-template.md)
