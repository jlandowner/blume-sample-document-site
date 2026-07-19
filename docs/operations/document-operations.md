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

ドキュメント検証の仕様は `tools/document-validator/validate_docs.py` に直接実装しています。ホストにPython packageを入れず、DockerまたはPodmanのbuild内で実行します。

検出対象:

- 必須frontmatterの不足。
- `id`、`type`、`owner`、`status`、`review_cycle` の不正値。
- `id` とMarkdown pathの不一致。
- `canonical_url` とMarkdown pathの不一致。
- `id` または `canonical_url` の重複。
- `last_reviewed` の形式不正、未来日、review期限切れ。
- pageが `mkdocs.yml` の `nav` に含まれていない状態。
- H1がない、H1が複数ある、H1とfrontmatter `title` が一致しない状態。
- checklist pageの各行が正本ドキュメントへlinkしていない状態。
- 存在しないMarkdown link。
- deprecated pageに `replaced_by` がない状態。

検証できないもの:

- コマンドが実際に成功するか。
- 設計判断や制約内容が業務的に正しいか。
- 外部URLが到達可能か。
- RAG検索品質が十分か。

## Pull requestチェックリスト

- 必須frontmatterがある。
- page titleとdescriptionが明確である。
- ページがnavigationに含まれている。
- linkが解決できる。
- commandがcopy可能で、対象環境が明確である。
- checklistが正本ドキュメントへリンクしている。
- validatorが成功する。
- review dateとownerが正しい。
