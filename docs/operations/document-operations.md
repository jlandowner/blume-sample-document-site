---
id: operations.document-operations
title: ドキュメント運用ルール
description: ドキュメントサイトを継続的に保守するための運用ルール。
type: overview
owner: platform-team
status: reviewed
review_cycle: quarterly
last_reviewed: 2026-07-19
platform_versions:
  - v1
audience:
  - platform-team
  - app-team
tags:
  - documentation
  - operations
canonical_url: /operations/document-operations/
---

# ドキュメント運用ルール

## オーナーシップ

すべてのページはfrontmatterに `owner` を持ちます。ownerは、内容の正確性、レビュー、障害時の読みやすさに責任を持ちます。

推奨owner:

- `platform-team`
- `security-team`
- `sre-team`
- `developer-experience`

## レビュールール

- 制約、手順、チェックリスト、ランブックは少なくとも四半期ごとにレビューします。
- 環境ページはcluster設定が変わるたびにレビューします。
- API仕様とツール仕様はreleaseごとにレビューします。
- deprecatedになったページは、代替ページがある場合は必ずリンクします。

## 変更ルール

- platformの挙動変更と同じpull requestでドキュメントを更新します。
- 制約が変わったらチェックリストも更新します。
- コマンド、CIテンプレート、デプロイフローが変わったら手順ページも更新します。
- 規則本文を重複させず、正本となる制約ページへリンクします。
- 複数topicを詰め込んだ大きなページより、小さく焦点の合ったページを優先します。

## 自動検証ルール

ホストに依存packageを入れず、DockerまたはPodmanのbuild内で検証します。

現在の検証:

- `make validate`: Blume strict buildを実行する。
- `make test-mcp-search`: Blume MCP serverを起動し、日本語検索で期待routeが返ることを確認する。

検出対象:

- Blume build error。
- navigationに含まれるpageの解決失敗。
- Markdown/frontmatterのbuild時parse失敗。
- broken internal route。
- MCP endpointの起動失敗。
- `search_docs` の日本語queryで期待pageが返らない状態。

検証できないもの:

- コマンドが実際に成功するか。
- 設計判断や制約内容が業務的に正しいか。
- 外部URLが到達可能か。
- frontmatter policyの全項目が業務ルールに沿っているか。

frontmatter policy、review期限、チェックリストlinkの厳密検証が必要になった場合は、Blume向けvalidatorとして追加します。その場合もホストではなくコンテナbuild内で実行します。

## Pull requestチェックリスト

- 必須frontmatterがある。
- page titleとdescriptionが明確である。
- ページがnavigationに含まれている。
- linkが解決できる。
- commandがcopy可能で、対象環境が明確である。
- checklistが正本ドキュメントへリンクしている。
- `make validate` が成功する。
- `make test-mcp-search` が成功する。
- review dateとownerが正しい。
