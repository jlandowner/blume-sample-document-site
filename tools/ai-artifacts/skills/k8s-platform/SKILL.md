---
name: k8s-platform-docs
description: K8sプラットフォームの環境、制約、手順、API、ツール、チェックリスト、ランブックを調べる。
---

# K8s Platform Docs Skill

## WHEN

次の話題が出たらこのskillを使います。

- Kubernetes platform
- deploy / rollback
- Secret管理
- ingress / network
- quota / limit
- production readiness
- platform API / CRD
- platformctl
- troubleshooting / runbook

## HOW

1. まず `search_docs` で関連pageを探します。
2. 正本が必要な場合は `get_page` にrouteを渡してpage全体を取得します。
3. production releaseやreviewでは、検索結果からchecklist pageを選び、`get_page` で正本を取得します。
4. 回答では `canonical_url` とpage titleを添えます。

## MCP

このskillは、Blume内蔵MCP serverが提供する次のtoolsを前提にします。

- `search_docs`
- `get_page`
- `list_pages`
- `get_navigation`
