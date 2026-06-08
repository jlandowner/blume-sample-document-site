---
id: constraints.security-policy
title: セキュリティポリシー
description: プラットフォーム上で動くworkloadのセキュリティ要件。
type: constraint
owner: security-team
status: reviewed
review_cycle: quarterly
last_reviewed: 2026-06-07
platform_versions:
  - v1
audience:
  - app-team
  - security-team
tags:
  - security
  - constraint
canonical_url: /constraints/security-policy/
---

# セキュリティポリシー

## 必須設定

| 項目 | 要件 |
| --- | --- |
| runAsNonRoot | `true` |
| readOnlyRootFilesystem | 原則 `true` |
| allowPrivilegeEscalation | `false` |
| image registry | approved registryのみ |
| secret storage | Kubernetes Secretまたはexternal secret |

## Public ingress

public ingressを作成する場合は、次の条件をすべて満たしてください。

- security reviewが完了している。
- WAF policyが割り当てられている。
- TLSが有効。
- health check endpointが認証なしで公開されている。

## Secretの扱い

- Secret値をGitにcommitしてはいけません。
- production Secretの更新はchange requestに紐付けます。
- Secret名には用途を含めます。

## 関連ページ

- [Secret管理手順](../procedures/secrets.md)
- [本番準備チェックリスト](../app-checklists/production-readiness.md)
