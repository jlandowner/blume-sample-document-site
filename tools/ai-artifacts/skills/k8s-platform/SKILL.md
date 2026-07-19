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

1. まず `docs.search` で関連pageとmatched sectionsを探します。
2. 正本が必要な場合は `docs.get_page` でpage全体を取得します。
3. production releaseやreviewでは、検索結果からchecklist pageを選び、`docs.get_page` で正本を取得します。
4. 回答では `canonical_url` とpage titleを添えます。

## MCP

このskillは、MCP Docs Serverが提供する次のtools/resourcesを前提にします。

- `docs.search`
- `docs.get_page`
- `docs://index`
- `docs://llms`
