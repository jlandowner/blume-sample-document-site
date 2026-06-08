---
id: operations.document-operations
title: ドキュメント運用ルール
description: ドキュメントサイトを継続的に保守するための運用ルール。
type: overview
owner: platform-team
status: reviewed
review_cycle: quarterly
last_reviewed: 2026-06-07
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

## Pull requestチェックリスト

- 必須frontmatterがある。
- page titleとdescriptionが明確である。
- ページがnavigationに含まれている。
- linkが解決できる。
- commandがcopy可能で、対象環境が明確である。
- checklistが正本ドキュメントへリンクしている。
- RAG artifactが手動編集なしで再生成される。
- review dateとownerが正しい。
