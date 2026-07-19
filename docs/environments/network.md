---
id: environments.network
title: ネットワーク
description: platform workload向けのネットワークルール、ingress class、接続前提。
type: environment
owner: platform-team
status: draft
review_cycle: quarterly
last_reviewed: 2026-07-19
platform_versions:
  - v1
audience:
  - app-team
  - sre-team
tags:
  - network
  - ingress
canonical_url: /environments/network/
---

# ネットワーク

## Ingress class

| class | 用途 | 使用可能環境 |
| --- | --- | --- |
| `internal` | 社内向けHTTP/HTTPS | dev, production |
| `public` | インターネット公開 | productionのみ |

## Serviceルール

- Service typeは原則 `ClusterIP` を使用します。
- `LoadBalancer` はplatform-team管理コンポーネントのみ使用できます。
- アプリ間通信はservice DNS名を使用します。

## DNS形式

```text
{service}.{namespace}.svc.cluster.local
```

## 関連ページ

- [セキュリティポリシー](../constraints/security-policy.md)
- [アプリケーションのデプロイ](../procedures/deploy-application.md)
